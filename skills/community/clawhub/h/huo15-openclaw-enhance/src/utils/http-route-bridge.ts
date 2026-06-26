/**
 * HTTP route bridge — 跨模块共享公网 baseUrl 自动检测。
 *
 * v5.7.24 起简化：只做 baseUrl 自动检测，不再做 sub-route dispatch。
 *
 * 背景：v5.7.23 把 bot-share 挂在 dashboard 的 `/plugins/enhance` prefix route 下，
 * 通过 bridge dispatch 子路径——后来发现 SDK 的 overlap 规则只检查 `${prefix}/` 形式，
 * 所以 `/plugins/enhance-share`（兄弟 prefix）跟 `/plugins/enhance` **不算 overlap**，
 * bot-share 可以直接注册自己独立的 prefix route。SubRoute dispatch 不再需要。
 *
 * 但 baseUrl 检测仍要从 dashboard 请求里抓——dashboard 是用户最常访问的入口；
 * 任何 `/plugins/enhance*` / `/plugins/enhance-share/*` 请求都顺手喂 detect 函数。
 *
 * 红线：纯只读 in-memory，零 child_process / fs 写。
 */
import type { IncomingMessage } from "node:http";

let detectedExternalBaseUrl: string | null = null;
let detectedInternalBaseUrl: string | null = null;

function isLikelyPublicHost(host: string): boolean {
  if (!host) return false;
  const hostname = host.split(":")[0];
  if (!hostname) return false;
  if (hostname === "localhost" || hostname === "0.0.0.0") return false;
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname)) return false; // IPv4
  if (/^\[.*\]$/.test(hostname)) return false; // bracketed IPv6
  return hostname.includes(".");
}

function pickProto(req: IncomingMessage): string {
  const fwd = req.headers["x-forwarded-proto"];
  if (typeof fwd === "string" && fwd.length > 0) return fwd.split(",")[0].trim();
  if (Array.isArray(fwd) && fwd.length > 0) return fwd[0];
  const encrypted = (req.socket as { encrypted?: boolean } | undefined)?.encrypted;
  return encrypted ? "https" : "http";
}

function pickHost(req: IncomingMessage): string | undefined {
  const fwd = req.headers["x-forwarded-host"];
  if (typeof fwd === "string" && fwd.length > 0) return fwd.split(",")[0].trim();
  if (Array.isArray(fwd) && fwd.length > 0) return fwd[0];
  return req.headers.host;
}

/** dashboard / share handler 顶部都调一下：从请求头抽公网 baseUrl 缓存住。 */
export function detectBaseUrlFromRequest(req: IncomingMessage): void {
  const host = pickHost(req);
  if (!host) return;
  const proto = pickProto(req);
  const baseUrl = `${proto}://${host}`.replace(/\/+$/, "");
  if (isLikelyPublicHost(host)) {
    detectedExternalBaseUrl = baseUrl;
  } else if (!detectedInternalBaseUrl) {
    detectedInternalBaseUrl = baseUrl;
  }
}

/** 工具运行时调用：env > 配置 > 检测到的 external > internal > fallback */
export function resolveBaseUrl(opts: {
  configBaseUrl?: string;
  envName?: string;
  fallback?: string;
}): string {
  const envName = opts.envName ?? "BOT_BASE_URL";
  const env = (globalThis as any).process?.env?.[envName]?.trim();
  if (env) return env.replace(/\/+$/, "");
  if (opts.configBaseUrl && opts.configBaseUrl.trim()) {
    return opts.configBaseUrl.trim().replace(/\/+$/, "");
  }
  if (detectedExternalBaseUrl) return detectedExternalBaseUrl;
  if (detectedInternalBaseUrl) return detectedInternalBaseUrl;
  return opts.fallback ?? "http://localhost:18789";
}

/** 测试/调试 */
export function _resetBridge(): void {
  detectedExternalBaseUrl = null;
  detectedInternalBaseUrl = null;
}

export function getDetectionState(): {
  external: string | null;
  internal: string | null;
} {
  return {
    external: detectedExternalBaseUrl,
    internal: detectedInternalBaseUrl,
  };
}
