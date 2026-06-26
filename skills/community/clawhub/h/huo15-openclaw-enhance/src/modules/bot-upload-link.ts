/**
 * 模块: BOT 文件上传桥（enhance_upload_link / check / revoke）
 *
 * 解决场景: 企微 100MB 直传上限。用户在群里转发 200MB 视频 → 企微只发系统通知文本
 * "视频/文件超过100M，无法下载" 给 bot → 没附件、没 hook 错误、什么都没。
 *
 * 解法: LLM 看到这种系统提示文本（或用户主动说要传大文件）→ 调 enhance_upload_link
 * 给 URL → 用户浏览器打开 → 拖拽上传到本机 → LLM Read 文件分析。
 *
 * v6.5.0 设计（镜像 v5.7.22 bot-share-link，反向版本）:
 *   - 兄弟 prefix /plugins/enhance-upload（跟 enhance-share、dashboard 三者独立）
 *   - GET <prefix>/<token>            → 返回拖拽上传 HTML 页（200 行原生 + 进度条）
 *   - GET <prefix>/<token>/api/list   → JSON 该 token 已收到文件列表
 *   - POST <prefix>/<token>/api/upload?name=<filename> → octet-stream，直接 stream pipe 到本地
 *     （故意不用 multipart，避免新增 npm 依赖；现代浏览器 fetch(file) 全支持）
 *   - LLM 工具 enhance_upload_link({label?, expireHours?}) / enhance_upload_check({token}) /
 *     enhance_upload_revoke({token})
 *
 * 共享 baseUrl 解析（跟 bot-share-link 完全一致 + 同一份 share/config.json）:
 *   env BOT_BASE_URL > pluginConfig.botUpload.baseUrl > pluginConfig.botShare.baseUrl
 *   > ~/.openclaw/share/config.json (locally saved) > 自动检测 > localhost 兜底
 *
 * 红线:
 *   - 零 child_process / 零新 npm 依赖（手 fs.createWriteStream 流式写）
 *   - 不擅自改用户配置（写 plugin 自己 ~/.openclaw/upload/ 目录）
 *   - LLM/HTTP 输入过 sanitizer（token = 12 hex；filename 防 path traversal）
 *   - 单文件硬上限（默认 2GB）防恶意请求打爆磁盘
 *   - Token 24h TTL，过期请求 410 Gone（lazy 清理）
 *   - HTTP handler 仅 GET/POST，HEAD/PUT/DELETE 等 405
 */
import { Type } from "@sinclair/typebox";
import {
  createWriteStream,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
  readdirSync,
} from "node:fs";
import { join, resolve as pathResolve } from "node:path";
import { randomBytes } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import {
  detectBaseUrlFromRequest,
  resolveBaseUrl as resolveBaseUrlFromBridge,
} from "../utils/http-route-bridge.js";
import type { BotUploadConfig, BotShareConfig } from "../types.js";

const DEFAULT_BASE_URL_FALLBACK = "http://localhost:18789";
const DEFAULT_URL_PREFIX = "/plugins/enhance-upload";
const DEFAULT_EXPIRE_HOURS = 24;
const DEFAULT_MAX_FILE_MB = 2048; // 2GB 防恶意大请求
const TOKEN_HEX_LEN = 12; // 6 bytes → 12 hex chars

/** 共享 share/config.json 里的 baseUrl，跟 bot-share-link 用同一份 */
function readSharedBaseUrl(api: OpenClawPluginApi): string | undefined {
  const sharePath = join(resolveOpenClawHome(api), "share", "config.json");
  if (!existsSync(sharePath)) return undefined;
  try {
    const j = JSON.parse(readFileSync(sharePath, "utf-8")) as { baseUrl?: string };
    return j?.baseUrl?.trim() || undefined;
  } catch {
    return undefined;
  }
}

interface UploadEntry {
  token: string;
  label?: string;
  ownerAgent?: string;
  createdAt: string;
  expireAt: string;
  files: Array<{
    name: string;
    sizeBytes: number;
    receivedAt: string;
  }>;
}

interface Manifest {
  version: 1;
  entries: UploadEntry[];
}

function resolveUploadRoot(api: OpenClawPluginApi, config: BotUploadConfig | undefined): string {
  if (config?.uploadRoot && config.uploadRoot.trim()) return config.uploadRoot.trim();
  return join(resolveOpenClawHome(api), "upload");
}

function resolveUrlPrefix(config: BotUploadConfig | undefined): string {
  const raw = (config?.urlPrefix ?? DEFAULT_URL_PREFIX).trim();
  if (!raw) return DEFAULT_URL_PREFIX;
  return "/" + raw.replace(/^\/+/, "").replace(/\/+$/, "");
}

function safeReadManifest(path: string): Manifest {
  if (!existsSync(path)) return { version: 1, entries: [] };
  try {
    const parsed = JSON.parse(readFileSync(path, "utf-8")) as Manifest;
    if (!parsed || typeof parsed !== "object" || !Array.isArray(parsed.entries)) {
      return { version: 1, entries: [] };
    }
    return parsed;
  } catch {
    return { version: 1, entries: [] };
  }
}

function safeWriteManifest(path: string, m: Manifest): void {
  writeFileSync(path, JSON.stringify(m, null, 2), "utf-8");
}

function pruneExpired(uploadRoot: string, manifest: Manifest, now: Date): number {
  const fresh: UploadEntry[] = [];
  let pruned = 0;
  for (const e of manifest.entries) {
    if (new Date(e.expireAt).getTime() <= now.getTime()) {
      const tokenDir = pathResolve(join(uploadRoot, e.token));
      if (
        existsSync(tokenDir) &&
        tokenDir.startsWith(pathResolve(uploadRoot) + "/")
      ) {
        try {
          rmSync(tokenDir, { recursive: true, force: true });
        } catch {
          // ignore
        }
      }
      pruned++;
      continue;
    }
    fresh.push(e);
  }
  manifest.entries = fresh;
  return pruned;
}

function sanitizeBaseName(name: string): string {
  const cleaned = name
    .replace(/[\/\\\x00-\x1F<>:"|?*]/g, "_")
    .replace(/\s+/g, "_")
    .slice(0, 200);
  return cleaned || `file-${Date.now()}`;
}

function isValidToken(t: string): boolean {
  return /^[0-9a-f]{12}$/.test(t);
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
  return `${(bytes / 1024 / 1024 / 1024).toFixed(2)}GB`;
}

function errorResponse(msg: string) {
  return { content: [{ type: "text" as const, text: `✗ ${msg}` }] };
}

function resolveBaseUrl(
  config: BotUploadConfig | undefined,
  shareConfig: BotShareConfig | undefined,
  api: OpenClawPluginApi,
): string {
  const explicit =
    config?.baseUrl?.trim() ||
    shareConfig?.baseUrl?.trim() ||
    readSharedBaseUrl(api);
  return resolveBaseUrlFromBridge({
    configBaseUrl: explicit,
    fallback: DEFAULT_BASE_URL_FALLBACK,
  });
}

function buildUploadPageUrl(baseUrl: string, urlPrefix: string, token: string): string {
  return `${baseUrl}${urlPrefix}/${token}`;
}

/**
 * 拖拽上传 HTML 页 — 200 行原生 + 浅色友好风格，跟 bot-share dashboard 同款风格。
 * 单页面用 fetch + ReadableStream 上传，进度条 + 多文件 + 拖拽。
 */
function renderUploadHtml(token: string, label: string | undefined, urlPrefix: string, expireAt: string): string {
  const safeLabel = label ? label.replace(/[<>&"']/g, (c) => `&#${c.charCodeAt(0)};`) : "";
  const expireLocal = expireAt.slice(0, 19).replace("T", " ");
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>文件上传 — 火一五增强</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,"PingFang SC","Helvetica Neue",sans-serif;background:#f5f7fa;color:#222;padding:24px;max-width:720px;margin:0 auto;min-height:100vh}
  h1{font-size:1.4em;color:#ff6b35;margin-bottom:6px}
  .meta{color:#888;font-size:0.9em;margin-bottom:24px}
  .meta b{color:#444}
  .drop{border:2px dashed #ccd;border-radius:12px;padding:48px 24px;text-align:center;background:#fff;transition:all .15s;cursor:pointer}
  .drop.hover{border-color:#ff6b35;background:#fff8f4}
  .drop p{color:#666;font-size:0.95em;line-height:1.6}
  .drop strong{color:#ff6b35}
  .drop input[type=file]{display:none}
  .pick{display:inline-block;margin-top:12px;padding:8px 24px;background:#ff6b35;color:#fff;border-radius:6px;font-size:0.9em}
  .files{margin-top:24px}
  .file{background:#fff;border:1px solid #e6eaef;border-radius:8px;padding:14px 16px;margin-bottom:10px;display:flex;align-items:center;gap:12px}
  .file .name{flex:1;font-weight:500;font-size:0.95em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .file .size{color:#999;font-size:0.85em;flex-shrink:0}
  .file .status{font-size:0.85em;flex-shrink:0;min-width:120px;text-align:right}
  .file .status.ok{color:#0a0}
  .file .status.err{color:#c33}
  .file .bar{height:3px;background:#eee;border-radius:2px;overflow:hidden;margin-top:8px;width:100%}
  .file .bar i{display:block;height:100%;background:#ff6b35;width:0%;transition:width .2s;font-style:normal}
  .footer{margin-top:32px;padding-top:16px;border-top:1px solid #e6eaef;color:#999;font-size:0.85em;line-height:1.6}
  .footer code{background:#f0f2f5;padding:2px 6px;border-radius:3px;font-size:0.85em}
  @media (prefers-color-scheme:dark){
    body{background:#0d1117;color:#e6edf3}
    .drop{background:#161b22;border-color:#30363d}
    .drop.hover{border-color:#ff6b35;background:#1f1410}
    .file{background:#161b22;border-color:#30363d}
    .footer{border-color:#30363d;color:#7d8590}
    .footer code{background:#21262d}
  }
</style>
</head>
<body>
  <h1>📤 文件上传</h1>
  <div class="meta">
    Token: <b>${token}</b>
    ${safeLabel ? `· 标签: <b>${safeLabel}</b>` : ""}
    · 有效至: <b>${expireLocal}</b>
  </div>

  <div class="drop" id="drop" onclick="document.getElementById('fi').click()">
    <p><strong>拖拽文件到此处</strong> 或 <span class="pick">点击选择</span></p>
    <p style="margin-top:8px;color:#999;font-size:0.85em">支持多文件 / 单文件最大 2GB / 直传到 AI 工作目录</p>
    <input type="file" id="fi" multiple>
  </div>

  <div class="files" id="files"></div>

  <div class="footer">
    上传完成后回到聊天告诉 AI"传完了"——AI 会调 <code>enhance_upload_check("${token}")</code> 拿到所有文件路径再 Read 分析。<br>
    本页面由 @huo15/openclaw-enhance v6.5.0 BOT 文件上传桥提供 · <code>~/.openclaw/upload/${token}/</code>
  </div>

<script>
const TOKEN = ${JSON.stringify(token)};
const PREFIX = ${JSON.stringify(urlPrefix)};
const drop = document.getElementById('drop');
const fi = document.getElementById('fi');
const filesDiv = document.getElementById('files');

['dragenter','dragover'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.add('hover')}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.remove('hover')}));
drop.addEventListener('drop',ev=>{
  ev.preventDefault();
  const files = Array.from(ev.dataTransfer.files);
  files.forEach(uploadOne);
});
fi.addEventListener('change',ev=>{
  const files = Array.from(ev.target.files);
  files.forEach(uploadOne);
});

function uploadOne(file){
  const row = document.createElement('div');
  row.className = 'file';
  row.innerHTML =
    '<div style="flex:1"><div class="name">'+escapeHtml(file.name)+'</div><div class="bar"><i></i></div></div>'+
    '<div class="size">'+fmtSize(file.size)+'</div>'+
    '<div class="status">上传中…</div>';
  filesDiv.insertBefore(row,filesDiv.firstChild);
  const bar = row.querySelector('.bar i');
  const status = row.querySelector('.status');

  const xhr = new XMLHttpRequest();
  xhr.open('POST', PREFIX+'/'+TOKEN+'/api/upload?name='+encodeURIComponent(file.name), true);
  xhr.setRequestHeader('Content-Type', file.type || 'application/octet-stream');
  xhr.upload.addEventListener('progress', e=>{
    if(e.lengthComputable){
      const pct = (e.loaded/e.total*100).toFixed(0);
      bar.style.width = pct+'%';
      status.textContent = pct+'%';
    }
  });
  xhr.addEventListener('load', ()=>{
    if(xhr.status >= 200 && xhr.status < 300){
      bar.style.width = '100%';
      status.textContent = '✓ 已上传';
      status.className = 'status ok';
    } else {
      status.textContent = '✗ '+xhr.status;
      status.className = 'status err';
    }
  });
  xhr.addEventListener('error', ()=>{
    status.textContent = '✗ 网络错误';
    status.className = 'status err';
  });
  xhr.send(file);
}

function fmtSize(b){
  if(b<1024) return b+'B';
  if(b<1024*1024) return (b/1024).toFixed(1)+'KB';
  if(b<1024*1024*1024) return (b/1024/1024).toFixed(1)+'MB';
  return (b/1024/1024/1024).toFixed(2)+'GB';
}
function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
</script>
</body>
</html>`;
}

export function registerBotUploadLink(
  api: OpenClawPluginApi,
  config: BotUploadConfig | undefined,
  shareConfig: BotShareConfig | undefined,
) {
  const uploadRoot = resolveUploadRoot(api, config);
  const manifestPath = join(uploadRoot, "manifest.json");
  const expireHours = config?.expireHours ?? DEFAULT_EXPIRE_HOURS;
  const maxFileMB = config?.maxFileSizeMB ?? DEFAULT_MAX_FILE_MB;
  const maxFileBytes = maxFileMB * 1024 * 1024;
  const urlPrefix = resolveUrlPrefix(config);

  try {
    mkdirSync(uploadRoot, { recursive: true });
  } catch (err) {
    api.logger.error(
      `[enhance-bot-upload] 创建 upload 目录失败 ${uploadRoot}：${(err as Error).message}`,
    );
  }

  // ── 注册独立 SDK prefix route ──
  api.registerHttpRoute({
    path: urlPrefix,
    match: "prefix",
    auth: "plugin",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      // 顺手喂给 bridge 缓存公网 baseUrl
      detectBaseUrlFromRequest(req);

      const rawUrl = req.url ?? "/";
      let urlObj: URL;
      try {
        urlObj = new URL(rawUrl, `http://${req.headers.host || "localhost"}`);
      } catch {
        res.writeHead(400);
        res.end("Bad Request");
        return true;
      }
      const pathname = urlObj.pathname;

      // prefix 根路径不暴露
      if (pathname === urlPrefix || pathname === urlPrefix + "/") {
        res.writeHead(404);
        res.end("Not Found");
        return true;
      }

      // 路径解析: <prefix>/<token>[/api/<action>]
      const tail = pathname.slice(urlPrefix.length + 1);
      const segments = tail.split("/").filter(Boolean);
      if (segments.length === 0) {
        res.writeHead(404);
        res.end("Not Found");
        return true;
      }
      const token = segments[0];
      if (!isValidToken(token)) {
        res.writeHead(400);
        res.end("Invalid token");
        return true;
      }

      // 查 manifest 验 token 存在 + 未过期
      const manifest = safeReadManifest(manifestPath);
      pruneExpired(uploadRoot, manifest, new Date());
      try {
        safeWriteManifest(manifestPath, manifest);
      } catch {
        /* 不致命 */
      }
      const entry = manifest.entries.find((e) => e.token === token);
      if (!entry) {
        res.writeHead(404);
        res.end("Token not found or expired");
        return true;
      }
      if (new Date(entry.expireAt).getTime() <= Date.now()) {
        res.writeHead(410);
        res.end("Gone (token expired)");
        return true;
      }

      // GET <token>           → 上传页 HTML
      // GET <token>/api/list  → JSON 已上传文件列表
      // POST <token>/api/upload?name=<fname> → 接收 octet-stream
      const action = segments.slice(1).join("/");

      if (req.method === "GET" && action === "") {
        const html = renderUploadHtml(token, entry.label, urlPrefix, entry.expireAt);
        res.writeHead(200, {
          "Content-Type": "text/html; charset=utf-8",
          "Cache-Control": "no-store",
          "X-Content-Type-Options": "nosniff",
        });
        res.end(html);
        return true;
      }

      if (req.method === "GET" && action === "api/list") {
        res.writeHead(200, {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "no-store",
        });
        res.end(JSON.stringify({
          token,
          label: entry.label ?? null,
          expireAt: entry.expireAt,
          files: entry.files,
        }));
        return true;
      }

      if (req.method === "POST" && action === "api/upload") {
        const rawName = urlObj.searchParams.get("name") ?? "";
        const fileName = sanitizeBaseName(rawName);
        if (!fileName || fileName === "_") {
          res.writeHead(400);
          res.end("Missing or invalid 'name' query parameter");
          return true;
        }

        const tokenDir = pathResolve(join(uploadRoot, token, "files"));
        if (!tokenDir.startsWith(pathResolve(uploadRoot) + "/")) {
          res.writeHead(400);
          res.end("Bad path");
          return true;
        }
        try {
          mkdirSync(tokenDir, { recursive: true });
        } catch (err) {
          res.writeHead(500);
          res.end(`Failed to create token dir: ${(err as Error).message}`);
          return true;
        }
        const filePath = pathResolve(join(tokenDir, fileName));
        if (!filePath.startsWith(tokenDir + "/")) {
          res.writeHead(400);
          res.end("Bad filename");
          return true;
        }

        // v6.7.15: stream pipe req → .partial 临时文件 → 完成后 rename 原子替换
        // Why: 上传完成但 nginx 反代超时给浏览器 408 时，用户重新上传会让
        // createWriteStream(filePath) 默认 truncate 已成功的文件 → 然后 408 触发 rmSync
        // → 留空目录但 manifest 还说"174MB 已收"（5/11 huangxuanrong 实测事故）。
        // 临时文件 + rename = 即使重传中途失败，旧的完整文件依然在。
        const partialPath = `${filePath}.partial-${Date.now()}-${randomBytes(3).toString("hex")}`;
        const uploadStartedAt = Date.now();
        api.logger.info(
          `[enhance-bot-upload] upload-start token=${token} file=${fileName} (partial=${partialPath.slice(uploadRoot.length)})`,
        );

        // Stream pipe req → file，过程中累计 bytes，超 maxFileBytes 主动 abort
        let receivedBytes = 0;
        let aborted = false;
        // v6.7.16: failed flag — req.on('error') / ws.on('error') 触发后不能走 rename 路径
        // 之前 bug：失败后 finish() done Promise，外面 if (aborted) return 不拦截 error case，
        // 继续走到 renameSync(partial, file) → ENOENT（partial 已被 rmSync 删）→ stderr 误报
        let failed = false;
        const ws = createWriteStream(partialPath);

        await new Promise<void>((done) => {
          let finished = false;
          const finish = () => {
            if (!finished) {
              finished = true;
              done();
            }
          };

          req.on("data", (chunk: Buffer) => {
            receivedBytes += chunk.length;
            if (receivedBytes > maxFileBytes) {
              aborted = true;
              try {
                req.destroy();
              } catch {
                /* ignore */
              }
              try {
                ws.destroy();
              } catch {
                /* ignore */
              }
              try {
                rmSync(partialPath, { force: true });
              } catch {
                /* ignore */
              }
              api.logger.warn(
                `[enhance-bot-upload] upload-aborted token=${token} file=${fileName} reason=too-large received=${receivedBytes} max=${maxFileBytes}`,
              );
              if (!res.headersSent) {
                res.writeHead(413);
                res.end(
                  `File too large: > ${formatSize(maxFileBytes)} (max ${maxFileMB}MB)`,
                );
              }
              finish();
            }
          });
          req.on("error", (err: Error) => {
            failed = true;
            try {
              ws.destroy();
            } catch {
              /* ignore */
            }
            // v6.7.15: 只删 .partial 临时文件，原 filePath 上的旧完整文件不动
            try {
              rmSync(partialPath, { force: true });
            } catch {
              /* ignore */
            }
            api.logger.warn(
              `[enhance-bot-upload] upload-failed token=${token} file=${fileName} reason=req-error received=${receivedBytes} error=${err.message}`,
            );
            if (!aborted && !res.headersSent) {
              res.writeHead(500);
              res.end(`Upload error: ${err.message}`);
            }
            finish();
          });
          ws.on("error", (err: Error) => {
            failed = true;
            try {
              rmSync(partialPath, { force: true });
            } catch {
              /* ignore */
            }
            api.logger.warn(
              `[enhance-bot-upload] upload-failed token=${token} file=${fileName} reason=write-error received=${receivedBytes} error=${err.message}`,
            );
            if (!aborted && !res.headersSent) {
              res.writeHead(500);
              res.end(`Write error: ${err.message}`);
            }
            finish();
          });
          ws.on("finish", finish);
          req.pipe(ws);
        });

        if (aborted || failed) return true;

        // v6.7.15: 落盘成功 → 原子 rename .partial → 真实 filePath
        // 这是核心：先写 partial，最后才"亮"出来，绝不破坏已有的成功文件
        // 同分区内 rename 是原子操作（POSIX rename(2)）
        try {
          renameSync(partialPath, filePath);
        } catch (err) {
          try {
            rmSync(partialPath, { force: true });
          } catch {
            /* ignore */
          }
          api.logger.warn(
            `[enhance-bot-upload] rename failed: ${partialPath} → ${filePath}: ${(err as Error).message}`,
          );
          if (!res.headersSent) {
            res.writeHead(500);
            res.end(`Rename failed: ${(err as Error).message}`);
          }
          return true;
        }

        // 更新 manifest
        const fresh = safeReadManifest(manifestPath);
        const idx = fresh.entries.findIndex((e) => e.token === token);
        if (idx >= 0) {
          // 同名覆盖：去掉旧条目
          fresh.entries[idx].files = fresh.entries[idx].files.filter(
            (f) => f.name !== fileName,
          );
          fresh.entries[idx].files.push({
            name: fileName,
            sizeBytes: receivedBytes,
            receivedAt: new Date().toISOString(),
          });
          try {
            safeWriteManifest(manifestPath, fresh);
          } catch (err) {
            api.logger.warn(
              `[enhance-bot-upload] manifest 写入失败：${(err as Error).message}`,
            );
          }
        }

        const durationMs = Date.now() - uploadStartedAt;
        const throughputMBs =
          durationMs > 0 ? (receivedBytes / 1024 / 1024 / (durationMs / 1000)).toFixed(2) : "?";
        api.logger.info(
          `[enhance-bot-upload] upload-ok token=${token} file=${fileName} bytes=${receivedBytes} (${formatSize(receivedBytes)}) duration=${durationMs}ms throughput=${throughputMBs}MB/s`,
        );

        res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
        res.end(
          JSON.stringify({
            ok: true,
            token,
            filename: fileName,
            sizeBytes: receivedBytes,
            sizeFormatted: formatSize(receivedBytes),
            path: filePath,
          }),
        );
        return true;
      }

      res.writeHead(405, { Allow: "GET, POST" });
      res.end("Method Not Allowed");
      return true;
    },
  });

  api.logger.info(
    `[enhance] BOT 文件上传桥已加载（root=${uploadRoot}，prefix=${urlPrefix}，默认 ${expireHours}h 过期，单文件上限 ${maxFileMB}MB）`,
  );

  // ── tools ──

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_upload_link",
      description:
        "生成一个用户上传文件给 AI 的临时 URL（拖拽上传页）。用于：" +
        "(1) 用户主动说要传大文件 / 视频 / 数据集；" +
        "(2) 用户消息含『视频/文件超过 100M，无法下载』『文件已被截断』等 IM 渠道大小拦截系统提示文本（企微 100MB / 钉钉等）；" +
        "(3) 用户尝试在 IM 直传但失败的征兆。" +
        "返回的 URL 让用户在浏览器拖拽上传，文件落到 ~/.openclaw/upload/<token>/files/<filename>。" +
        "用户传完后回聊天说『传完了』→ AI 调 enhance_upload_check(token) 拿路径再 Read 分析。",
      parameters: Type.Object({
        label: Type.Optional(
          Type.String({
            description: "可选展示标签（仅显示用，不影响 token），如『视频分析』『数据集』",
          }),
        ),
        expireHours: Type.Optional(
          Type.Number({
            description: `链接有效小时数，默认 ${DEFAULT_EXPIRE_HOURS}，最长 720 (30天)`,
            minimum: 1,
            maximum: 24 * 30,
          }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const label = String(params.label ?? "").trim() || undefined;
        const ttlH =
          typeof params.expireHours === "number" && Number.isFinite(params.expireHours)
            ? Math.min(Math.max(Number(params.expireHours), 1), 24 * 30)
            : expireHours;

        const token = randomBytes(6).toString("hex");
        const tokenDir = join(uploadRoot, token, "files");
        try {
          mkdirSync(tokenDir, { recursive: true });
        } catch (err) {
          return errorResponse(`创建 token 目录失败：${(err as Error).message}`);
        }

        const now = new Date();
        const expireAt = new Date(now.getTime() + ttlH * 3600 * 1000);
        const ownerAgent = ((ctx as unknown as { agentId?: string })?.agentId ?? "").trim() || undefined;

        const manifest = safeReadManifest(manifestPath);
        const pruned = pruneExpired(uploadRoot, manifest, now);
        manifest.entries.push({
          token,
          label,
          ownerAgent,
          createdAt: now.toISOString(),
          expireAt: expireAt.toISOString(),
          files: [],
        });
        try {
          safeWriteManifest(manifestPath, manifest);
        } catch (err) {
          return errorResponse(`manifest 写入失败：${(err as Error).message}`);
        }

        const baseUrl = resolveBaseUrl(config, shareConfig, api);
        const url = buildUploadPageUrl(baseUrl, urlPrefix, token);
        const isFallback = baseUrl === DEFAULT_BASE_URL_FALLBACK;

        const lines = [
          `✓ 已生成上传链接（${ttlH}h 后过期）：`,
          ``,
          url,
          ``,
          label ? `标签：${label}` : "",
          `落盘：${tokenDir}`,
          `过期：${expireAt.toISOString()}`,
          pruned > 0 ? `（顺手清理了 ${pruned} 个过期 token）` : "",
          ``,
          isFallback
            ? `⚠ baseUrl 是 localhost 兜底，外部用户访问不到。建议调 \`enhance_share_set_baseurl(url="<你的公网域名>")\` 一次性保存（跟 share-link 共享 baseUrl 配置）。`
            : `baseUrl=${baseUrl}`,
          ``,
          `**用户操作步骤**：把此 URL 发给用户 → 浏览器打开 → 拖拽文件上传 → 用户说"传完了" → AI 调 \`enhance_upload_check(token="${token}")\` 取路径再 Read。`,
        ]
          .filter(Boolean)
          .join("\n");

        return {
          content: [{ type: "text" as const, text: lines }],
          structuredContent: {
            url,
            token,
            label,
            uploadRoot: tokenDir,
            expireAt: expireAt.toISOString(),
            baseUrl,
            baseUrlIsFallback: isFallback,
            urlPrefix,
            prunedExpired: pruned,
          },
        };
      },
    })) as any,
    { name: "enhance_upload_link" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_upload_check",
      description:
        "查看某个 upload token 当前已收到的文件列表 + 落盘路径。LLM 在用户说『传完了』后调，拿到路径再 Read 文件分析。",
      parameters: Type.Object({
        token: Type.String({
          description: "12 位 hex token，由 enhance_upload_link 返回",
        }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const token = String(params.token ?? "").trim();
        if (!isValidToken(token)) {
          return errorResponse(`token 格式不对（要 12 hex 字符）：${token}`);
        }

        const manifest = safeReadManifest(manifestPath);
        pruneExpired(uploadRoot, manifest, new Date());
        const entry = manifest.entries.find((e) => e.token === token);
        if (!entry) {
          return errorResponse(`token ${token} 不存在或已过期`);
        }

        const tokenDir = join(uploadRoot, token, "files");
        // 同步 fs 实际文件，防 manifest 跟 fs 漂移
        let fsFiles: string[] = [];
        try {
          fsFiles = readdirSync(tokenDir);
        } catch {
          fsFiles = [];
        }
        const files = entry.files.filter((f) => fsFiles.includes(f.name));

        if (files.length === 0) {
          return {
            content: [{
              type: "text" as const,
              text:
                `📭 token ${token} 暂无文件（用户还没上传或已被清理）。\n` +
                `如果用户说传完了但这里看不到，让他们打开 ${buildUploadPageUrl(resolveBaseUrl(config, shareConfig, api), urlPrefix, token)} 重传。`,
            }],
            structuredContent: { token, files: [], expireAt: entry.expireAt },
          };
        }

        const lines = [
          `📦 token ${token}${entry.label ? ` (${entry.label})` : ""} 当前 ${files.length} 个文件：`,
          ``,
        ];
        const out: Array<{ name: string; path: string; sizeBytes: number; sizeFormatted: string; receivedAt: string }> = [];
        for (const f of files) {
          const filePath = join(tokenDir, f.name);
          lines.push(`  · ${f.name} (${formatSize(f.sizeBytes)}, ${f.receivedAt.slice(0, 19).replace("T", " ")})`);
          lines.push(`    Read: ${filePath}`);
          out.push({
            name: f.name,
            path: filePath,
            sizeBytes: f.sizeBytes,
            sizeFormatted: formatSize(f.sizeBytes),
            receivedAt: f.receivedAt,
          });
        }
        lines.push("");
        lines.push(`下一步：用 Read 工具读这些文件分析。token 还会在 ${entry.expireAt.slice(0, 19).replace("T", " ")} 过期。`);

        return {
          content: [{ type: "text" as const, text: lines.join("\n") }],
          structuredContent: { token, label: entry.label, expireAt: entry.expireAt, files: out },
        };
      },
    })) as any,
    { name: "enhance_upload_check" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_upload_revoke",
      description:
        "撤销 upload token：立刻删除 ~/.openclaw/upload/<token>/ 整个目录（含已收文件）+ 移除 manifest 条目。" +
        "用于 (1) 处理完文件不再需要保留 (2) 安全考虑提前清理。",
      parameters: Type.Object({
        token: Type.String({ description: "12 hex token" }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const token = String(params.token ?? "").trim();
        if (!isValidToken(token)) return errorResponse(`token 格式不对：${token}`);

        const manifest = safeReadManifest(manifestPath);
        const before = manifest.entries.length;
        const removed = manifest.entries.find((e) => e.token === token);
        manifest.entries = manifest.entries.filter((e) => e.token !== token);

        if (!removed) {
          return {
            content: [{ type: "text" as const, text: `未找到 token ${token}` }],
            structuredContent: { token, removed: false },
          };
        }

        const tokenDir = pathResolve(join(uploadRoot, token));
        if (
          tokenDir.startsWith(pathResolve(uploadRoot) + "/") &&
          existsSync(tokenDir)
        ) {
          try {
            rmSync(tokenDir, { recursive: true, force: true });
          } catch (err) {
            api.logger.warn(
              `[enhance-bot-upload] 删除 ${tokenDir} 失败：${(err as Error).message}`,
            );
          }
        }
        try {
          safeWriteManifest(manifestPath, manifest);
        } catch {
          /* ignore */
        }

        return {
          content: [{
            type: "text" as const,
            text:
              `✓ 已撤销 token ${token}（${before} → ${manifest.entries.length}）` +
              (removed.files.length > 0 ? `，删除 ${removed.files.length} 个文件` : ""),
          }],
          structuredContent: {
            token,
            removed: true,
            filesDeleted: removed.files.length,
            label: removed.label,
          },
        };
      },
    })) as any,
    { name: "enhance_upload_revoke" },
  );

  // ── prompt supplement: 引导 LLM 在 IM 大文件场景主动调 ──
  // 跟 bot-share-link 的 supplement 同款套路；touch 触发关键词字面写进去
  // 让 LLM 看到「视频/文件超过100M，无法下载」立即识别为"该调 enhance_upload_link"
  if (typeof api.registerMemoryPromptSupplement === "function") {
    try {
      api.registerMemoryPromptSupplement(({ availableTools }) => {
        if (!availableTools.has("enhance_upload_link")) return [];
        return [
          "## 文件上传（用户 → AI）",
          "- 触发场景任一命中就调 `enhance_upload_link`：① 用户主动说要传大文件/视频/数据集；② 用户消息含『视频/文件超过 100M，无法下载』『文件已被截断』等 IM 渠道大小拦截系统提示（企微 100MB / 钉钉等）；③ 用户尝试在 IM 直传但失败的征兆。",
          "- 返回 URL 发给用户，让其浏览器拖拽上传。用户说『传完了』→ 调 `enhance_upload_check(token)` 拿路径再 Read 分析。",
          "- 不要让用户在 IM 渠道硬上传超过 20MB 文件——必失败。",
        ];
      });
      api.logger.info(
        "[enhance-bot-upload] prompt supplement 已注册（引导 LLM 在企微 100MB 等场景主动调 enhance_upload_link）",
      );
    } catch (err) {
      api.logger.warn(
        `[enhance-bot-upload] prompt supplement 注册失败：${(err as Error).message}`,
      );
    }
  }
}
