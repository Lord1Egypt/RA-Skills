/**
 * 大文件分享兜底（File Share Fallback）
 *
 * 场景：企微媒体上传上限为 20MB，超限的文件会被 applyFileSizeLimits 标 reject。
 * 用户最终只看到一行"文件大小 XXMb 超过了企业微信允许的最大限制 20MB，无法发送"。
 * 但 @huo15/openclaw-enhance v5.7.22+ 已经把 share 目录暴露成了一条 HTTP route
 * （prefix /plugins/enhance-share），完全可以兜底成临时下载链接。
 *
 * 本模块通过文件系统契约直接写入 enhance bot-share 用的 share 目录 + manifest.json：
 *   - shareRoot 默认 ~/.openclaw/share（与 enhance bot-share 共享）
 *   - manifest.json 字段 / token / filename 命名格式与 enhance 完全一致
 *   - URL prefix 默认 /plugins/enhance-share（由 enhance 的 HTTP route 服务）
 *
 * 故：wecom 这里写 + 用户访问 enhance 的 prefix → 直接 work，零 IPC / 零跨插件 import。
 *
 * 前置：用户必须装 @huo15/openclaw-enhance（默认 enabled），并把 BOT_BASE_URL 配成公网地址。
 *
 * 红线（与 wecom plugin 一致）：
 *   - 零 child_process（fs.writeFileSync / readFileSync）
 *   - 不擅自改用户配置（写的是 share 目录与 manifest，不动 ~/.openclaw/openclaw.json）
 *   - LLM 输入过 sanitizer：sanitizeBaseName 防 path traversal
 *   - 单文件大小没有硬上限（这是兜底兜底，已经超了 20MB），由 maxFileMB 配置控制
 */

import {
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { randomBytes } from "node:crypto";

const DEFAULT_SHARE_ROOT = join(homedir(), ".openclaw", "share");
const DEFAULT_URL_PREFIX = "/plugins/enhance-share";
const DEFAULT_EXPIRE_HOURS = 24;
const DEFAULT_MAX_FILE_MB = 500;
const DEFAULT_BASE_URL_FALLBACK = "http://localhost:18789";

export interface ShareFallbackConfig {
  enabled?: boolean;
  /** 落盘根目录，默认 ~/.openclaw/share（与 @huo15/openclaw-enhance bot-share 共享） */
  shareRoot?: string;
  /** URL 路径前缀，默认 /plugins/enhance-share（与 enhance 注册的兄弟前缀 route 对齐） */
  urlPrefix?: string;
  /** 链接默认过期小时数，默认 24，最长 720（30 天） */
  expireHours?: number;
  /** 公网 base URL 显式配置（优先级：env BOT_BASE_URL > 此配置 > localhost 兜底） */
  baseUrl?: string;
  /** 单文件硬上限 MB，默认 500（兜底兜底，不要乱传整盘文件） */
  maxFileMB?: number;
}

interface ManifestEntry {
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
  entries: ManifestEntry[];
}

export interface ShareFallbackOk {
  ok: true;
  url: string;
  expireAt: string;
  filename: string;
  shareRoot: string;
  baseUrlUsed: string;
  baseUrlIsFallback: boolean;
  sizeBytes: number;
}

export interface ShareFallbackErr {
  ok: false;
  error: string;
}

export type ShareFallbackResult = ShareFallbackOk | ShareFallbackErr;

function sanitizeBaseName(name: string): string {
  const cleaned = name
    .replace(/[\/\\\x00-\x1F<>:"|?*]/g, "_")
    .replace(/\s+/g, "_")
    .slice(0, 100);
  return cleaned || "file";
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

function pruneExpired(filesDir: string, manifest: Manifest, now: Date): void {
  const fresh: ManifestEntry[] = [];
  for (const e of manifest.entries) {
    const localPath = join(filesDir, e.filename);
    const expired = new Date(e.expireAt).getTime() <= now.getTime();
    if (expired) {
      if (existsSync(localPath)) {
        try {
          rmSync(localPath, { force: true });
        } catch {
          // ignore: 老文件失败不致命，下次 prune 再试
        }
      }
      continue;
    }
    fresh.push(e);
  }
  manifest.entries = fresh;
}

function resolveBaseUrl(config: ShareFallbackConfig): {
  baseUrl: string;
  isFallback: boolean;
} {
  const env = process.env.BOT_BASE_URL?.trim();
  if (env) return { baseUrl: env.replace(/\/+$/, ""), isFallback: false };
  const cfg = config.baseUrl?.trim();
  if (cfg) return { baseUrl: cfg.replace(/\/+$/, ""), isFallback: false };
  return { baseUrl: DEFAULT_BASE_URL_FALLBACK, isFallback: true };
}

function resolveShareRoot(config: ShareFallbackConfig): string {
  const cfg = config.shareRoot?.trim();
  if (cfg) return cfg.replace(/\/+$/, "");
  return DEFAULT_SHARE_ROOT;
}

function resolveUrlPrefix(config: ShareFallbackConfig): string {
  const raw = (config.urlPrefix ?? DEFAULT_URL_PREFIX).trim();
  if (!raw) return DEFAULT_URL_PREFIX;
  return "/" + raw.replace(/^\/+/, "").replace(/\/+$/, "");
}

/**
 * 把 buffer 落盘到 enhance bot-share 共享的 share 目录 + manifest，返回临时下载 URL。
 *
 * @param buffer 文件 bytes（来自 wecom 媒体加载流程，已经在内存中，不会重复 IO）
 * @param fileName 用户可见文件名（会被 sanitize 后用 token 前缀拼为落盘名）
 * @param label 可选展示名（仅记录，不影响 URL）
 * @param config 配置（默认与 enhance bot-share 共享 ~/.openclaw/share）
 */
export function shareFallback(params: {
  buffer: Buffer;
  fileName: string;
  label?: string;
  config?: ShareFallbackConfig;
}): ShareFallbackResult {
  const cfg = params.config ?? {};
  if (cfg.enabled === false) {
    return { ok: false, error: "shareFallback disabled by config" };
  }
  const maxFileMB = cfg.maxFileMB ?? DEFAULT_MAX_FILE_MB;
  const sizeMB = params.buffer.length / 1024 / 1024;
  if (sizeMB > maxFileMB) {
    return {
      ok: false,
      error: `文件 ${sizeMB.toFixed(1)}MB 超过 share 兜底上限 ${maxFileMB}MB`,
    };
  }
  if (params.buffer.length <= 0) {
    return { ok: false, error: "buffer 为空" };
  }

  const shareRoot = resolveShareRoot(cfg);
  const urlPrefix = resolveUrlPrefix(cfg);
  const expireHours = Math.min(Math.max(cfg.expireHours ?? DEFAULT_EXPIRE_HOURS, 1), 24 * 30);
  const filesDir = join(shareRoot, "files");
  const manifestPath = join(shareRoot, "manifest.json");

  try {
    mkdirSync(filesDir, { recursive: true });
  } catch (err) {
    return {
      ok: false,
      error: `创建 share 目录失败 ${filesDir}: ${(err as Error).message}`,
    };
  }

  const manifest = safeReadManifest(manifestPath);
  const now = new Date();
  pruneExpired(filesDir, manifest, now);

  const token = randomBytes(6).toString("hex");
  const sanitized = sanitizeBaseName(params.fileName);
  const finalName = `${token}-${sanitized}`;
  const destPath = join(filesDir, finalName);

  try {
    writeFileSync(destPath, params.buffer);
  } catch (err) {
    return {
      ok: false,
      error: `写入 share 文件失败 ${destPath}: ${(err as Error).message}`,
    };
  }

  const expireAt = new Date(now.getTime() + expireHours * 3600_000);
  manifest.entries.push({
    token,
    filename: finalName,
    sourcePath: `[wecom-fallback ${params.buffer.length}B]`,
    sizeBytes: params.buffer.length,
    label: params.label,
    createdAt: now.toISOString(),
    expireAt: expireAt.toISOString(),
  });
  try {
    writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf-8");
  } catch {
    // manifest 写失败 = 文件已落盘但下次 prune 不知道；下载仍可用，仅过期清理失败
    // 不致命，不要回滚
  }

  const { baseUrl, isFallback } = resolveBaseUrl(cfg);
  const url = `${baseUrl}${urlPrefix}/${encodeURIComponent(finalName)}`;
  return {
    ok: true,
    url,
    expireAt: expireAt.toISOString(),
    filename: finalName,
    shareRoot,
    baseUrlUsed: baseUrl,
    baseUrlIsFallback: isFallback,
    sizeBytes: params.buffer.length,
  };
}

/** 把成功的 share fallback 结果格式化为发给用户的提示文本（markdown_v2 兼容）。 */
export function formatShareFallbackText(params: {
  fileName: string;
  fileSizeBytes: number;
  result: ShareFallbackOk;
}): string {
  const sizeMB = (params.fileSizeBytes / 1024 / 1024).toFixed(2);
  const expireLocal = params.result.expireAt.slice(0, 19).replace("T", " ");
  const lines = [
    `📎 **${params.fileName}** (${sizeMB} MB) 超过企微 20MB 上限，已生成临时下载链接：`,
    "",
    params.result.url,
    "",
    `_链接有效至 ${expireLocal} UTC（${params.result.expireAt.endsWith("Z") ? "" : "服务器时间"}）_`,
  ];
  if (params.result.baseUrlIsFallback) {
    lines.push("");
    lines.push(
      "⚠ 链接使用 localhost 兜底，请将服务器的 BOT_BASE_URL 配置为公网地址（例：`export BOT_BASE_URL=https://your-domain.com`），否则用户无法访问。",
    );
  }
  return lines.join("\n");
}
