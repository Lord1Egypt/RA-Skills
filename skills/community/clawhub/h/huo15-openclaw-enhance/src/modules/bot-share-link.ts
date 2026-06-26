/**
 * 模块: BOT 文件分享桥（enhance_share_file / list / revoke）
 *
 * 解决场景：企微/钉钉等 IM 渠道无法直传大文件（>20MB / >50MB），需要给用户一个
 * 临时下载链接。比如本地播客生成 90MB mp3 → 企微发不出去 → 拿这个工具生成一个
 * `https://<域名>/plugins/enhance-share/<token>-podcast.mp3` 发给用户即可。
 *
 * 工作机制（v5.7.24 起独立兄弟 prefix）：
 *   - SDK overlap 规则：`prefixMatchPath` 检查 `${prefix}/`，所以兄弟前缀
 *     `/plugins/enhance-share` 跟 dashboard 的 `/plugins/enhance` **不算 overlap**，
 *     bot-share 直接 api.registerHttpRoute 自己的 prefix route，不再依赖 bridge dispatch。
 *   - 任何 `/plugins/enhance*` / `/plugins/enhance-share/*` 请求都喂给
 *     detectBaseUrlFromRequest(req)，bridge 缓存公网 host——访问过一次 dashboard
 *     或下载过一次 share 链接，工具就能拼出正确公网 URL，不用配 env / nginx alias。
 *   - LLM 调 enhance_share_file(filePath) 时，把文件 copy/link 到
 *     `<shareRoot>/files/<token>-<basename>`，URL 拼为
 *     `${detectedBaseUrl}/plugins/enhance-share/<token>-<basename>`。
 *
 * 配置优先级（baseUrl）：env BOT_BASE_URL > pluginConfig.botShare.baseUrl
 *   > 自动检测到的公网 host > http://localhost:18789（fallback）
 *
 * 红线一致：
 *   - 零 child_process（fs.copyFileSync / linkSync / createReadStream）
 *   - 不擅自改用户配置（写的是插件自己的 share 目录）
 *   - LLM 输入过 sanitizer：绝对路径校验 + path traversal + 敏感目录黑名单
 *   - HTTP handler 防越界（filename 不能含 / 和 ..，必须 manifest 命中）
 *   - 单文件大小上限（默认 500MB）防止误传系统盘
 */
import { Type } from "@sinclair/typebox";
import {
  copyFileSync,
  createReadStream,
  existsSync,
  linkSync,
  mkdirSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { basename, isAbsolute, join, normalize, resolve as pathResolve } from "node:path";
import { randomBytes } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import {
  detectBaseUrlFromRequest,
  resolveBaseUrl as resolveBaseUrlFromBridge,
} from "../utils/http-route-bridge.js";
import type { BotShareConfig } from "../types.js";

const DEFAULT_BASE_URL_FALLBACK = "http://localhost:18789";
const DEFAULT_URL_PREFIX = "/plugins/enhance-share";
const DEFAULT_EXPIRE_HOURS = 24;
const DEFAULT_MAX_FILE_MB = 500;
const LOCAL_CONFIG_FILENAME = "config.json";

const SENSITIVE_DIR_TOKENS = [
  "/.ssh/",
  "/.gnupg/",
  "/.aws/",
  "/.config/",
  "/.docker/",
  "/.kube/",
  "/.npmrc",
  "/.netrc",
  "/etc/",
];

interface ShareEntry {
  token: string;
  filename: string;
  sourcePath: string;
  sizeBytes: number;
  label?: string;
  createdAt: string;
  expireAt: string;
}

interface Manifest {
  version: 1;
  entries: ShareEntry[];
}

/**
 * 本地持久化配置（~/.openclaw/share/config.json）
 *
 * 用途：用户首次安装 enhance 没配 env BOT_BASE_URL 也没在 openclaw.json 写
 * `enhance.config.botShare.baseUrl` 时，让 AI 引导用户提供公网域名后通过
 * `enhance_share_set_baseurl` 工具保存到这里，下次启动自动生效。
 *
 * 红线（与 plugin 整体一致）：
 *   - 写在 plugin 自己的 share 目录（~/.openclaw/share/），不动用户的 openclaw.json
 *   - 零 child_process / 零 fs.writeFileSync 用户配置文件
 *   - 优先级低于 env / pluginConfig，高于 host header 自动检测
 */
interface LocalShareConfig {
  baseUrl?: string;
  setAt?: string;
  setBy?: string;
}

function resolveShareRoot(api: OpenClawPluginApi, config: BotShareConfig | undefined): string {
  if (config?.shareRoot && config.shareRoot.trim()) return config.shareRoot.trim();
  return join(resolveOpenClawHome(api), "share");
}

function resolveUrlPrefix(config: BotShareConfig | undefined): string {
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

function safeWriteManifest(path: string, manifest: Manifest): void {
  writeFileSync(path, JSON.stringify(manifest, null, 2), "utf-8");
}

function pruneExpired(
  filesDir: string,
  manifest: Manifest,
  now: Date,
): { pruned: number; pendingMissing: number } {
  const fresh: ShareEntry[] = [];
  let pruned = 0;
  let pendingMissing = 0;
  for (const e of manifest.entries) {
    const localPath = join(filesDir, e.filename);
    const expired = new Date(e.expireAt).getTime() <= now.getTime();
    if (expired) {
      if (existsSync(localPath)) {
        try {
          rmSync(localPath, { force: true });
        } catch {
          // ignore
        }
      }
      pruned++;
      continue;
    }
    if (!existsSync(localPath)) pendingMissing++;
    fresh.push(e);
  }
  manifest.entries = fresh;
  return { pruned, pendingMissing };
}

function sanitizeBaseName(name: string): string {
  const cleaned = name
    .replace(/[\/\\\x00-\x1F<>:"|?*]/g, "_")
    .replace(/\s+/g, "_")
    .slice(0, 100);
  return cleaned || "file";
}

function isSensitivePath(absPath: string): boolean {
  const tail = absPath.endsWith("/") ? absPath : absPath + "/";
  return SENSITIVE_DIR_TOKENS.some((t) => tail.includes(t));
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

function localConfigPath(shareRoot: string): string {
  return join(shareRoot, LOCAL_CONFIG_FILENAME);
}

function readLocalConfig(shareRoot: string): LocalShareConfig {
  const p = localConfigPath(shareRoot);
  if (!existsSync(p)) return {};
  try {
    const parsed = JSON.parse(readFileSync(p, "utf-8")) as LocalShareConfig;
    if (!parsed || typeof parsed !== "object") return {};
    return parsed;
  } catch {
    return {};
  }
}

function writeLocalConfig(shareRoot: string, partial: LocalShareConfig): LocalShareConfig {
  mkdirSync(shareRoot, { recursive: true });
  const current = readLocalConfig(shareRoot);
  const next: LocalShareConfig = { ...current, ...partial };
  writeFileSync(localConfigPath(shareRoot), JSON.stringify(next, null, 2), "utf-8");
  return next;
}

/**
 * baseUrl 解析优先级（v5.7.27 起新增 local saved 层）：
 *   1. env BOT_BASE_URL
 *   2. pluginConfig.botShare.baseUrl（来自 openclaw.json）
 *   3. ~/.openclaw/share/config.json baseUrl（用户通过 enhance_share_set_baseurl 保存）
 *   4. detected external host（从浏览器访问 dashboard 的 host header）
 *   5. detected internal host
 *   6. http://localhost:18789（兜底）
 *
 * 实现：把 (2) 或 (3) 合并喂给 bridge 当 configBaseUrl，bridge 内部再走 env > configBaseUrl > detected > fallback。
 */
function resolveBaseUrl(config: BotShareConfig | undefined, shareRoot: string): string {
  const pluginConfigBaseUrl = config?.baseUrl?.trim();
  if (pluginConfigBaseUrl) {
    return resolveBaseUrlFromBridge({
      configBaseUrl: pluginConfigBaseUrl,
      fallback: DEFAULT_BASE_URL_FALLBACK,
    });
  }
  const localBaseUrl = readLocalConfig(shareRoot).baseUrl?.trim();
  return resolveBaseUrlFromBridge({
    configBaseUrl: localBaseUrl,
    fallback: DEFAULT_BASE_URL_FALLBACK,
  });
}

/**
 * baseUrl 来源诊断——用于工具输出和首装检测时告诉用户"现在用的是哪个值，从哪来的"。
 */
function describeBaseUrlSource(
  config: BotShareConfig | undefined,
  shareRoot: string,
): { source: "env" | "pluginConfig" | "localFile" | "detected" | "fallback"; value: string } {
  const env = (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env
    ?.BOT_BASE_URL?.trim();
  if (env) return { source: "env", value: env.replace(/\/+$/, "") };
  if (config?.baseUrl?.trim()) {
    return { source: "pluginConfig", value: config.baseUrl.trim().replace(/\/+$/, "") };
  }
  const localBaseUrl = readLocalConfig(shareRoot).baseUrl?.trim();
  if (localBaseUrl) {
    return { source: "localFile", value: localBaseUrl.replace(/\/+$/, "") };
  }
  const resolved = resolveBaseUrlFromBridge({
    fallback: DEFAULT_BASE_URL_FALLBACK,
  });
  if (resolved !== DEFAULT_BASE_URL_FALLBACK) {
    return { source: "detected", value: resolved };
  }
  return { source: "fallback", value: DEFAULT_BASE_URL_FALLBACK };
}

function buildShareUrl(
  baseUrl: string,
  urlPrefix: string,
  filename: string,
): string {
  return `${baseUrl}${urlPrefix}/${encodeURIComponent(filename)}`;
}

/** 把原始文件名（去掉 token 前缀）抽出来，用于 Content-Disposition。 */
function deriveFriendlyName(finalName: string): string {
  const dash = finalName.indexOf("-");
  return dash > 0 ? finalName.slice(dash + 1) : finalName;
}

/** 图片扩展名 —— 命中则用 Markdown image 语法让龙虾管家内联预览缩略图。 */
const IMAGE_EXTS = new Set([
  "png", "jpg", "jpeg", "gif", "webp", "bmp", "svg", "avif", "heic", "heif", "ico",
]);
function isImageFile(name: string): boolean {
  const dot = name.lastIndexOf(".");
  if (dot < 0) return false;
  return IMAGE_EXTS.has(name.slice(dot + 1).toLowerCase());
}

/**
 * 生成「可在龙虾管家预览」的 Markdown 片段：
 * - 图片 → `![名](url)`：客户端内联渲染缩略图
 * - 其他文件 → `[📎 名](url)`：可点击下载卡片
 * 任何渲染 Markdown 的客户端（龙虾管家 web / 钉钉 markdown）都能预览；
 * 不渲染 Markdown 的纯文本渠道（企微 text）由各自 send 层降级（见 wecom 渲染器）。
 */
function buildPreviewMarkdown(displayName: string, url: string): string {
  const safeName = displayName.replace(/[\[\]]/g, "");
  return isImageFile(displayName) ? `![${safeName}](${url})` : `[📎 ${safeName}](${url})`;
}

export function registerBotShareLink(
  api: OpenClawPluginApi,
  config: BotShareConfig | undefined,
) {
  const shareRoot = resolveShareRoot(api, config);
  const filesDir = join(shareRoot, "files");
  const manifestPath = join(shareRoot, "manifest.json");
  const expireHours = config?.expireHours ?? DEFAULT_EXPIRE_HOURS;
  const maxFileMB = config?.maxFileSizeMB ?? DEFAULT_MAX_FILE_MB;
  const urlPrefix = resolveUrlPrefix(config);

  try {
    mkdirSync(filesDir, { recursive: true });
  } catch (err) {
    api.logger.error(
      `[enhance-bot-share] 创建 share 目录失败 ${filesDir}：${(err as Error).message}`,
    );
  }

  // ── 注册独立 SDK prefix route（兄弟前缀，不跟 dashboard /plugins/enhance overlap） ──
  api.registerHttpRoute({
    path: urlPrefix,
    match: "prefix",
    auth: "plugin",
    handler: async (req: IncomingMessage, res: ServerResponse) => {
      // 顺手喂给 bridge 缓存公网 baseUrl —— 用户即使没访问过 dashboard，
      // 第一次点过的下载链接也能让工具知道公网 URL 是什么。
      detectBaseUrlFromRequest(req);

      const rawUrl = req.url ?? "/";
      let pathname: string;
      try {
        pathname = new URL(rawUrl, `http://${req.headers.host || "localhost"}`).pathname;
      } catch {
        res.writeHead(400);
        res.end("Bad Request");
        return true;
      }

      if (req.method !== "GET" && req.method !== "HEAD") {
        res.writeHead(405, { Allow: "GET, HEAD" });
        res.end("Method Not Allowed");
        return true;
      }

      // prefix 根路径或者带 / 但没文件名 → 404（不暴露目录列表）
      if (pathname === urlPrefix || pathname === urlPrefix + "/") {
        res.writeHead(404);
        res.end("Not Found");
        return true;
      }
      let filename: string;
      try {
        filename = decodeURIComponent(pathname.slice(urlPrefix.length + 1));
      } catch {
        res.writeHead(400);
        res.end("Bad Request");
        return true;
      }
      if (!filename || filename.includes("/") || filename.includes("..") || filename.includes("\\")) {
        res.writeHead(400);
        res.end("Bad Request");
        return true;
      }

      const manifest = safeReadManifest(manifestPath);
      const entry = manifest.entries.find((e) => e.filename === filename);
      if (!entry) {
        res.writeHead(404);
        res.end("Not Found");
        return true;
      }
      if (new Date(entry.expireAt).getTime() <= Date.now()) {
        res.writeHead(410);
        res.end("Gone (link expired)");
        return true;
      }

      const localPath = pathResolve(join(filesDir, filename));
      if (!localPath.startsWith(pathResolve(filesDir) + "/") || !existsSync(localPath)) {
        res.writeHead(404);
        res.end("Not Found (file missing)");
        return true;
      }
      let st: ReturnType<typeof statSync>;
      try {
        st = statSync(localPath);
      } catch {
        res.writeHead(404);
        res.end("Not Found");
        return true;
      }

      const friendlyName = deriveFriendlyName(filename);
      // RFC 5987 双声明，兼容老浏览器 + UTF-8 文件名
      const safeAscii = friendlyName.replace(/[^\x20-\x7E]/g, "_").replace(/"/g, "_");
      const contentDisposition =
        `attachment; filename="${safeAscii}"; filename*=UTF-8''${encodeURIComponent(friendlyName)}`;

      res.writeHead(200, {
        "Content-Type": "application/octet-stream",
        "Content-Length": st.size,
        "Content-Disposition": contentDisposition,
        "Cache-Control": "private, max-age=0, must-revalidate",
        "X-Content-Type-Options": "nosniff",
      });
      if (req.method === "HEAD") {
        res.end();
        return true;
      }

      await new Promise<void>((done) => {
        const stream = createReadStream(localPath);
        let finished = false;
        const finish = () => {
          if (!finished) {
            finished = true;
            done();
          }
        };
        stream.on("error", (err) => {
          api.logger.warn(
            `[enhance-bot-share] stream error on ${localPath}: ${(err as Error).message}`,
          );
          try {
            if (!res.headersSent) res.writeHead(500);
            res.end();
          } catch {
            // ignore
          }
          finish();
        });
        stream.on("end", finish);
        res.on("close", () => {
          stream.destroy();
          finish();
        });
        stream.pipe(res);
      });
      return true;
    },
  });

  api.logger.info(
    `[enhance] BOT 文件分享模块已加载（root=${shareRoot}，prefix=${urlPrefix}，默认 ${expireHours}h 过期，上限 ${maxFileMB}MB；独立 SDK prefix route，不依赖 dashboard，nginx 反代 /plugins/* 即可）`,
  );

  // ── v5.7.27: 首装检测——load 时给用户一个当前 baseUrl 来源的可见提示 ──
  // 没有 stdin 交互能力，但可以让首次安装的用户在 OpenClaw 启动 log 里立刻看到
  // "你的 baseUrl 来自哪、是不是公网可达"。命中 fallback / LAN 检测时升级为 warn。
  const startupSource = describeBaseUrlSource(config, shareRoot);
  const looksLan =
    startupSource.source === "detected" && /\/\/\d+\.\d+\.\d+\.\d+/.test(startupSource.value);
  if (startupSource.source === "fallback") {
    api.logger.warn(
      `[enhance-bot-share] ⚠ 首装检测：未配置 BOT_BASE_URL / openclaw.json botShare.baseUrl / 本地保存，` +
        `当前 baseUrl=${startupSource.value} 仅本机可达。请用 \`enhance_share_set_baseurl(url=...)\` 工具或 \`export BOT_BASE_URL=...\` 配置公网地址，否则 IM 用户点不开下载链接。`,
    );
  } else if (looksLan) {
    api.logger.warn(
      `[enhance-bot-share] ⚠ 首装检测：baseUrl=${startupSource.value} 看起来是局域网 IP（可能因为你曾用 LAN IP 访问 dashboard 被自动检测）。` +
        `公网用户访问不到，请用 \`enhance_share_set_baseurl(url=...)\` 工具保存公网域名覆盖。`,
    );
  } else {
    api.logger.info(
      `[enhance-bot-share] baseUrl=${startupSource.value}（来源：${startupSource.source}）`,
    );
  }

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_share_file",
      description:
        "把本地文件投递到 OpenClaw share 目录，返回对外的临时下载链接。**任意大小都用这个工具**（包括 < 10MB 的小文件）—— wecom/钉钉等 IM 渠道的 outbound 不识别 'MEDIA:'/'FILE:' 等文本约定，不调本工具就只能发普通文字，用户什么也收不到。" +
        "用于企微/钉钉/微信等渠道发文件：传一个绝对路径，返回 https://<公网域名>/plugins/enhance-share/<token>-<filename> 给用户下载。" +
        "zero-config：用户访问过 dashboard 或点过任何 share 链接后，公网 baseUrl 自动从 host header 检测，不需要配 env / nginx alias。文件 24h 后下次工具调用时自动 lazy 清理。" +
        "**返回结果里有一行 Markdown（图片为 `![](url)`、其他文件为 `[📎名](url)`）—— 发给用户时请原样保留这行 Markdown，龙虾管家会内联预览图片缩略图 / 渲染成可点击下载卡片**（structuredContent.markdown 也带这个值）。",
      parameters: Type.Object({
        filePath: Type.String({
          description:
            "本地文件绝对路径（必须存在；不允许敏感目录如 ~/.ssh / .aws / .gnupg / /etc 下的文件）",
        }),
        label: Type.Optional(
          Type.String({ description: "可选展示名（仅记录用，不影响 URL）" }),
        ),
        expireHours: Type.Optional(
          Type.Number({
            description: `链接有效小时数，默认 ${DEFAULT_EXPIRE_HOURS}，最长 720 (30天)`,
            minimum: 1,
            maximum: 24 * 30,
          }),
        ),
        copyMode: Type.Optional(
          Type.Union([Type.Literal("copy"), Type.Literal("link")], {
            description: "copy=复制（默认，跨分区可用）/ link=硬链接（同分区零拷贝，失败自动降级 copy）",
          }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const filePath = String(params.filePath ?? "").trim();
        const label = String(params.label ?? "").trim() || undefined;
        const ttlH =
          typeof params.expireHours === "number" && Number.isFinite(params.expireHours)
            ? Math.min(Math.max(Number(params.expireHours), 1), 24 * 30)
            : expireHours;
        const copyMode = (params.copyMode as "copy" | "link" | undefined) ?? "copy";

        if (!filePath) return errorResponse("filePath 必填且需为绝对路径。");
        if (!isAbsolute(filePath)) {
          return errorResponse(`filePath 必须是绝对路径，收到：${filePath}`);
        }
        const normalized = normalize(filePath);
        if (normalized.split("/").includes("..")) {
          return errorResponse("filePath 不能含 .. 段。");
        }
        if (isSensitivePath(normalized)) {
          return errorResponse(
            `拒绝分享敏感目录文件（黑名单 token：${SENSITIVE_DIR_TOKENS.join("、")}）。`,
          );
        }
        if (!existsSync(normalized)) {
          return errorResponse(`文件不存在：${normalized}`);
        }
        let st: ReturnType<typeof statSync>;
        try {
          st = statSync(normalized);
        } catch (err) {
          return errorResponse(`stat 失败：${(err as Error).message}`);
        }
        if (!st.isFile()) {
          return errorResponse(`只能分享普通文件，${normalized} 不是 file。`);
        }
        const sizeMB = st.size / 1024 / 1024;
        if (sizeMB > maxFileMB) {
          return errorResponse(
            `文件 ${formatSize(st.size)} 超过上限 ${maxFileMB}MB（可在 enhance.botShare.maxFileSizeMB 调整）。`,
          );
        }

        const manifest = safeReadManifest(manifestPath);
        const now = new Date();
        const { pruned } = pruneExpired(filesDir, manifest, now);

        const token = randomBytes(6).toString("hex");
        const sanitized = sanitizeBaseName(basename(normalized));
        const finalName = `${token}-${sanitized}`;
        const destPath = pathResolve(join(filesDir, finalName));
        if (!destPath.startsWith(pathResolve(filesDir) + "/")) {
          return errorResponse("内部错误：dest 越出 share 目录。");
        }

        try {
          if (copyMode === "link") {
            try {
              linkSync(normalized, destPath);
            } catch (err) {
              api.logger.warn(
                `[enhance-bot-share] hardlink 失败降级 copy：${(err as Error).message}`,
              );
              copyFileSync(normalized, destPath);
            }
          } else {
            copyFileSync(normalized, destPath);
          }
        } catch (err) {
          return errorResponse(`投递失败：${(err as Error).message}`);
        }

        const expireAt = new Date(now.getTime() + ttlH * 3600 * 1000);
        manifest.entries.push({
          token,
          filename: finalName,
          sourcePath: normalized,
          sizeBytes: st.size,
          label,
          createdAt: now.toISOString(),
          expireAt: expireAt.toISOString(),
        });
        try {
          safeWriteManifest(manifestPath, manifest);
        } catch (err) {
          api.logger.warn(
            `[enhance-bot-share] manifest 写入失败：${(err as Error).message}`,
          );
        }

        const baseUrlSource = describeBaseUrlSource(config, shareRoot);
        const baseUrl = baseUrlSource.value;
        const url = buildShareUrl(baseUrl, urlPrefix, finalName);
        const isFallback = baseUrlSource.source === "fallback";
        const isLanDetected =
          baseUrlSource.source === "detected" && /\/\/\d+\.\d+\.\d+\.\d+/.test(baseUrl);
        const sourceLabel: Record<typeof baseUrlSource.source, string> = {
          env: "env BOT_BASE_URL",
          pluginConfig: "openclaw.json enhance.config.botShare.baseUrl",
          localFile: "~/.openclaw/share/config.json（本地保存）",
          detected: "host header 自动检测",
          fallback: "默认兜底",
        };
        const displayName = label ?? deriveFriendlyName(finalName);
        const previewMd = buildPreviewMarkdown(displayName, url);
        const isImg = isImageFile(displayName);
        const lines = [
          `✓ 已生成临时下载链接（${formatSize(st.size)}，${ttlH}h 后过期）：`,
          ``,
          previewMd,
          ``,
          `📌 发给用户时请原样保留上面这行 Markdown —— 龙虾管家会${isImg ? "内联预览图片缩略图" : "渲染成可点击下载卡片"}（纯文本渠道如企微会自动降级为链接）。`,
          `纯链接（复制用）：${url}`,
          ``,
          label ? `展示名：${label}` : "",
          `源文件：${normalized}`,
          `落盘：${destPath}`,
          `过期：${expireAt.toISOString()}`,
          pruned > 0 ? `（顺手清理了 ${pruned} 个过期文件）` : "",
          ``,
          `baseUrl=${baseUrl}（来源：${sourceLabel[baseUrlSource.source]}）`,
          isFallback
            ? `⚠ baseUrl 是 localhost 兜底，外网用户访问不到。建议调用 \`enhance_share_set_baseurl(url="<你的公网域名>")\` 一次性保存（如 https://share.example.com），或 export BOT_BASE_URL / 写入 openclaw.json 的 enhance.config.botShare.baseUrl。`
            : "",
          isLanDetected
            ? `⚠ baseUrl 看起来是局域网 IP，公网用户访问不到。建议调用 \`enhance_share_set_baseurl(url="<你的公网域名>")\` 覆盖。`
            : "",
        ]
          .filter(Boolean)
          .join("\n");

        return {
          content: [{ type: "text" as const, text: lines }],
          structuredContent: {
            url,
            markdown: previewMd,
            isImage: isImg,
            token,
            filename: finalName,
            sourcePath: normalized,
            sizeBytes: st.size,
            sizeFormatted: formatSize(st.size),
            label,
            expireAt: expireAt.toISOString(),
            baseUrl,
            baseUrlSource: baseUrlSource.source,
            baseUrlIsFallback: isFallback,
            baseUrlIsLanDetected: isLanDetected,
            urlPrefix,
            shareRoot,
            prunedExpired: pruned,
          },
        };
      },
    })) as any,
    { name: "enhance_share_file" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_share_list",
      description: "列出当前活跃的 BOT 分享链接（自动顺手清理过期文件）",
      parameters: Type.Object({}),
      async execute() {
        const manifest = safeReadManifest(manifestPath);
        const now = new Date();
        const { pruned, pendingMissing } = pruneExpired(filesDir, manifest, now);
        try {
          safeWriteManifest(manifestPath, manifest);
        } catch {
          // 不致命
        }

        const baseUrl = resolveBaseUrl(config, shareRoot);
        if (manifest.entries.length === 0) {
          const head = pruned > 0 ? `（清理了 ${pruned} 个过期文件）\n` : "";
          return {
            content: [
              {
                type: "text" as const,
                text: `${head}暂无活跃分享。基址：${baseUrl}${urlPrefix} → ${filesDir}/`,
              },
            ],
            structuredContent: {
              entries: [],
              pruned,
              pendingMissing,
              baseUrl,
              urlPrefix,
              shareRoot,
            },
          };
        }

        const sorted = [...manifest.entries].sort(
          (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
        );
        const lines: string[] = [
          `当前 ${manifest.entries.length} 个活跃分享${pruned > 0 ? `（${pruned} 个刚被清理）` : ""}：`,
          ``,
        ];
        for (const e of sorted) {
          const url = buildShareUrl(baseUrl, urlPrefix, e.filename);
          const displayName = e.label ?? deriveFriendlyName(e.filename);
          const remainH = (
            (new Date(e.expireAt).getTime() - now.getTime()) /
            3600 /
            1000
          ).toFixed(1);
          lines.push(`  · ${displayName} · ${formatSize(e.sizeBytes)} · 剩 ${remainH}h`);
          lines.push(`    ${buildPreviewMarkdown(displayName, url)}`);
          lines.push(`    源: ${e.sourcePath}`);
        }
        if (pendingMissing > 0) {
          lines.push(``);
          lines.push(`⚠ ${pendingMissing} 个 manifest 条目对应本地文件已丢失（可能被外部删除），URL 会 404。`);
        }

        return {
          content: [{ type: "text" as const, text: lines.join("\n") }],
          structuredContent: {
            entries: sorted.map((e) => {
              const u = buildShareUrl(baseUrl, urlPrefix, e.filename);
              const dn = e.label ?? deriveFriendlyName(e.filename);
              return { ...e, url: u, markdown: buildPreviewMarkdown(dn, u), isImage: isImageFile(dn) };
            }),
            pruned,
            pendingMissing,
            baseUrl,
            urlPrefix,
            shareRoot,
          },
        };
      },
    })) as any,
    { name: "enhance_share_list" },
  );

  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_share_revoke",
      description: "撤销分享链接（按 token 或 filename 匹配，立刻删除本地文件 + manifest 条目）",
      parameters: Type.Object({
        match: Type.String({ description: "token (12 hex) 或 filename（落盘文件名）" }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const match = String(params.match ?? "").trim();
        if (!match) return errorResponse("match 必填。");

        const manifest = safeReadManifest(manifestPath);
        const before = manifest.entries.length;
        const removed: ShareEntry[] = [];
        manifest.entries = manifest.entries.filter((e) => {
          const hit = e.token === match || e.filename === match;
          if (hit) removed.push(e);
          return !hit;
        });

        if (removed.length === 0) {
          return {
            content: [{ type: "text" as const, text: `未找到匹配 ${match} 的分享。` }],
            structuredContent: { match, removed: [] },
          };
        }

        for (const e of removed) {
          const p = join(filesDir, e.filename);
          if (existsSync(p)) {
            try {
              rmSync(p, { force: true });
            } catch (err) {
              api.logger.warn(
                `[enhance-bot-share] 删除 ${p} 失败：${(err as Error).message}`,
              );
            }
          }
        }
        try {
          safeWriteManifest(manifestPath, manifest);
        } catch {
          // 不致命
        }
        return {
          content: [
            {
              type: "text" as const,
              text: `✓ 已撤销 ${removed.length} 个分享（${before} → ${manifest.entries.length}）：${removed.map((e) => e.filename).join("、")}`,
            },
          ],
          structuredContent: {
            match,
            removed: removed.map((e) => e.filename),
            remaining: manifest.entries.length,
          },
        };
      },
    })) as any,
    { name: "enhance_share_revoke" },
  );

  // ── v5.7.27: 持久化保存 baseUrl 到 ~/.openclaw/share/config.json ──
  // 解决"首次安装 enhance 没人提示用户配 BOT_BASE_URL → 链接落到 localhost / LAN IP
  // 兜底 → AI 看到不可达的 URL 自己又编一个"的连环错。
  //
  // 红线：写到 plugin 自己的 share 目录，不动用户的 ~/.openclaw/openclaw.json
  // （后者归 openclaw 控制，参见 6.4 诊断不修复 + 红线 #5）。
  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_share_set_baseurl",
      description:
        "保存 enhance bot-share 的公网 baseUrl 到 ~/.openclaw/share/config.json，让 enhance_share_file 生成可外网访问的下载链接。" +
        "典型场景：用户首次安装插件没设 BOT_BASE_URL 也没在 openclaw.json 配 enhance.config.botShare.baseUrl —— 此时 enhance_share_file 生成的链接会落到 localhost 兜底或 LAN IP（host header 自动检测），外网用户访问不了。" +
        "AI 看到这种情况时应**先问用户公网域名再调本工具**保存（不要自作主张写一个）。" +
        "优先级：env BOT_BASE_URL > openclaw.json 里的 enhance.config.botShare.baseUrl > 本工具保存到 ~/.openclaw/share/config.json > host header 自动检测 > localhost 兜底。",
      parameters: Type.Object({
        url: Type.String({
          description:
            "公网 baseUrl，必须 http:// 或 https:// 开头，可带端口但不能带路径 / query / hash。" +
            "示例：'https://share.example.com'、'http://keepermac.huo15.com'、'http://example.com:18789'。",
        }),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const raw = String(params.url ?? "").trim();
        if (!raw) return errorResponse("url 必填。");
        if (!/^https?:\/\//i.test(raw)) {
          return errorResponse(`url 必须以 http:// 或 https:// 开头，收到：${raw}`);
        }
        let parsed: URL;
        try {
          parsed = new URL(raw);
        } catch (err) {
          return errorResponse(`url 解析失败：${(err as Error).message}`);
        }
        if (parsed.pathname && parsed.pathname !== "/" && parsed.pathname !== "") {
          return errorResponse(
            `url 不能带路径（baseUrl 是协议+host[:port]，share path 由插件追加）。请去掉 '${parsed.pathname}'。`,
          );
        }
        if (parsed.search || parsed.hash) {
          return errorResponse("url 不能带 query 或 hash。");
        }
        const normalized = `${parsed.protocol}//${parsed.host}`;

        let saved: LocalShareConfig;
        try {
          saved = writeLocalConfig(shareRoot, {
            baseUrl: normalized,
            setAt: new Date().toISOString(),
            setBy: "enhance_share_set_baseurl",
          });
        } catch (err) {
          return errorResponse(
            `写入 ${shareRoot}/${LOCAL_CONFIG_FILENAME} 失败：${(err as Error).message}`,
          );
        }

        const newSource = describeBaseUrlSource(config, shareRoot);
        const overridden =
          newSource.source !== "localFile" || newSource.value !== normalized;
        const lines = [
          `✓ baseUrl=${normalized} 已保存到 ${shareRoot}/${LOCAL_CONFIG_FILENAME}。`,
          ``,
          `下次调 \`enhance_share_file\` 生成的链接会用这个域名（除非 env BOT_BASE_URL 或 openclaw.json 里有更高优先级配置）。`,
        ];
        if (overridden) {
          lines.push(``);
          lines.push(
            `⚠ 当前实际生效的 baseUrl=${newSource.value}（来源：${newSource.source}）—— 你刚保存的值被更高优先级源覆盖了。如要让本地保存生效，请先 \`unset BOT_BASE_URL\` / 删掉 openclaw.json 里的 enhance.config.botShare.baseUrl。`,
          );
        }
        return {
          content: [{ type: "text" as const, text: lines.join("\n") }],
          structuredContent: {
            saved: { ...saved },
            savedTo: localConfigPath(shareRoot),
            effectiveBaseUrl: newSource.value,
            effectiveSource: newSource.source,
            overriddenByHigherPriority: overridden,
          },
        };
      },
    })) as any,
    { name: "enhance_share_set_baseurl" },
  );

  // ── prompt supplement：强引导 LLM 在 IM 渠道发大文件必须调 enhance_share_file ──
  // 修复 v5.7.26 wecom 失忆事故的姊妹问题：AI 知道企微 20MB 限制后直接在文本里
  // 凭空编了一个下载 URL（`http://192.168.x.x:9999/file.mp4` 这种用户网络相关
  // 但完全错误的链接），既没调 enhance_share_file 也没让 wecom fallback 接管。
  // 根因：tool description 写得再清楚也只是 LLM "可以读"，没有 prompt level 的
  // 强约束。这里走 memory prompt supplement 把规则注入 system prompt。
  if (typeof api.registerMemoryPromptSupplement === "function") {
    try {
      api.registerMemoryPromptSupplement(({ availableTools }) => {
        if (!availableTools.has("enhance_share_file")) return [];
        return [
          "## 文件分享（按大小分流，v6.1.8 — 优先渠道本地直发）",
          "**默认优先级**：先尝试**渠道本地直发**（如 wecom 渠道的 `MEDIA: <绝对路径>` 单独成行，钉钉等价物），**仅当文件超过渠道 size 上限时才用 `enhance_share_file` 走链接**。",
          "**用户偏好优先**：如果用户明确说「不要发链接」/「直接发文件给我」/「以后都直接发」——**强制**用渠道本地直发，即使大文件也先尝试，企微/钉钉拒了再降级链接。",
          "**决策表**：图片≤10MB / 视频≤10MB / 语音≤2MB / 其他文件≤20MB → 渠道本地直发（群里直接收到附件）；超过这些阈值 → `enhance_share_file` 链接。",
          "- **严禁**手写、拼接、猜测或回忆下载 URL（包括 `http://192.168.x.x:9999/<file>`、`https://localhost/<file>`、缺 token 前缀的 `/plugins/enhance-share/<filename>` 等任何形式）。它们都不是真实链接，用户点了只会 404。`enhance_share_file` 工具的 `structuredContent.url` 是唯一可信的下载 URL 来源。",
          "- 当文件不在本地（来自远程 URL / 刚生成的 buffer）时，先把文件落盘到 `~/Downloads/` 等绝对路径，再调 `enhance_share_file`；不要让 wecom/dingtalk 的发送工具去 fetch 一个你不确定能访问的 URL。",
          "- 当 `enhance_share_file` 返回的 `baseUrlIsFallback=true`（localhost 兜底）或 `baseUrlIsLanDetected=true`（局域网 IP）时：**先**问用户公网域名（如 `https://share.your-domain.com`），**再**调用 `enhance_share_set_baseurl(url=用户给的域名)` 把它保存到 `~/.openclaw/share/config.json`，下次自动生效。**不要**自己猜测 / 替换 URL，**不要**只是要求用户 `export BOT_BASE_URL`（除非用户表示不想长期保存）。",
        ];
      });
      api.logger.info(
        "[enhance-bot-share] prompt supplement 已注册（强引导 LLM 调 enhance_share_file，禁止手写下载 URL）",
      );
    } catch (err) {
      api.logger.warn(
        `[enhance-bot-share] prompt supplement 注册失败：${(err as Error).message}`,
      );
    }
  }
}
