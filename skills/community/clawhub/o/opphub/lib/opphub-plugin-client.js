//
//   plugin 后安装 → 主动 migrate skill 目录下的 token + 刷新
//   skill 端不再双源重写 readToken/writeToken/keychain, 改 import plugin client
//
//   1. skill 跑时主动读 plugin dist/oauth-client.js
//   2. plugin 是 source of truth (Keychain 单写入方)
//   3. skill 不再自己写 Keychain, 只读 + 调 plugin 的 refresh
//
// 关键设计:
//   - 平台兼容: plugin dist 路径 / macOS / Linux / Windows
//   - plugin 不在运行时 (进程死了): plugin client 仍然能从 dist file import 跑通
//     (refresh / read / writeToken 都是 fs 操作, 不依赖 plugin runtime)
//   - getAccessToken() 内部按 status 自动选 refresh / device flow:
//       valid        → return t.access_token
//       needs_refresh → 调 awaitRefreshToken, 写新 token 到 Keychain, return 新 access_token
//       expired/missing → 触发 device flow (会调浏览器, 但 plugin 没开浏览器我们也不开, 等 user bot turn 后做)

import { existsSync } from "node:fs";
import { join } from "node:path";
import { homedir, platform } from "node:os";

// === 找 plugin dist 路径 ===
// 9 路径探测 (跟 plugin 自己一样的优先级)
function candidatePluginPaths() {
  const home = homedir();
  return [
    join(home, ".openclaw", "extensions", "opphub"),         // macOS 标准 (官方安装路径)
    join(home, ".openclaw", "plugins", "opphub"),            // 老版本 / 简化安装
    "/app/extensions/opphub",                               // Docker WORKDIR
    "/workspace/extensions/opphub",                          // K8s emptyDir
    "/data/extensions/opphub",                               // K8s PV
    join(home, ".local", "share", "openclaw", "extensions", "opphub"), // Linux XDG
  ].filter(existsSync);
}

function findPluginClientPath() {
  for (const p of candidatePluginPaths()) {
    const candidate = join(p, "dist", "oauth-client.js");
    if (existsSync(candidate)) return candidate;
  }
  return null;
}

let _pluginClient = null;
let _pluginClientLoadError = null;

async function loadPluginClient() {
  if (_pluginClient) return _pluginClient;
  if (_pluginClientLoadError) throw _pluginClientLoadError;

  const path = findPluginClientPath();
  if (!path) {
    _pluginClientLoadError = new Error(
      `plugin dist/oauth-client.js 找不到, 探测 9 个候选路径都失败. skill 不能维护 token. ` +
      `请先装 opphub-plugin: openclaw plugins install clawhub:@mtty-ai/opphub`
    );
    throw _pluginClientLoadError;
  }

  try {
    // 用动态 import (绝对路径) 避免 ESM 静态解析
    _pluginClient = await import(`file://${path}`);
    return _pluginClient;
  } catch (e) {
    _pluginClientLoadError = new Error(`plugin client import 失败 (${path}): ${e?.message ?? e}`);
    throw _pluginClientLoadError;
  }
}

// === 对外 API ===

/**
 * 读 Keychain token (走 plugin client, 自动 migrate 老 plain text)
 */
export async function readToken() {
  const client = await loadPluginClient();
  return await client.readToken();
}

/**
 * 写 Keychain token (走 plugin client)
 */
export async function writeToken(t) {
  const client = await loadPluginClient();
  return await client.writeToken(t);
}

/**
 * 清 Keychain token (走 plugin client)
 *
 *   修: 代理补 clearToken
 */
export async function clearToken() {
  const client = await loadPluginClient();
  return await client.clearToken();
}

/**
 * 判定 token 状态 (valid / needs_refresh / expired / missing)
 */
export async function tokenStatus(t) {
  const client = await loadPluginClient();
  return client.tokenStatus(t);
}

/**
 * 拿 access_token (核心):
 *   - valid        → return t.access_token
 *   - needs_refresh → 调 awaitRefreshToken 写 Keychain + return 新 token
 *   - expired/missing → 触发 device flow
 *
 * 重要: 不依赖 plugin runtime 进程, 只依赖 dist/oauth-client.js 文件存在
 */
export async function getAccessToken() {
  const client = await loadPluginClient();
  return await client.getAccessToken();
}

/**
 * 主动 refresh (不读 token state, 强制)
 *
 *   plugin client 没 export refreshToken (仅 getAccessToken 内部用 awaitRefreshToken)
 *   getAccessToken 看到 status=valid 直接 return, 不 refresh → 调 getAccessToken 刷不出来
 *
 *   修法:
 *   1. status=needs_refresh → 直接调 getAccessToken (会触发 awaitRefreshToken)
 *   2. status=valid 但想强刷 → 把 token.expires_at 改 0 临时设为 expired, 调 getAccessToken 触发 refresh, 再恢复
 *   3. status=missing/expired (refresh_token 也过) → 返 ok=false 让 bot 走 device flow
 *
 *   之前返 string (access_token), 但 bin/opphub-token-refresh.js 要 t.expires_at
 *   契约不一致 → status 返 "Invalid time value" + 误报失败
 *   修: 3 个 return 路径都返 { access_token, refresh_token, expires_at, ... }
 */
export async function refreshToken({ force = false } = {}) {
  const client = await loadPluginClient();
  const t = await client.readToken();
  if (!t) {
    throw new Error("没 token, 不能 refresh (先 device flow)");
  }

  const status = client.tokenStatus(t);

  // 路径 1: needs_refresh → getAccessToken 内部走 awaitRefreshToken
  //   内部已 writeToken 新 token, 重读 Keychain 拿完整对象
  if (status === "needs_refresh") {
    await client.getAccessToken();
    return await client.readToken();
  }

  // 路径 2: valid 但强制 → 临时篡改 expires_at 让他过期, 触发 refresh
  if (force && status === "valid") {
    await directRefreshAndWrite(client, t);
    return await client.readToken();
  }

  // 路径 3: valid (不强制) → 不需要 refresh, 但仍返完整对象
  if (status === "valid") {
    return t;
  }

  // 路径 4: expired/missing → 抛错, 让 bot 走 device flow
  throw new Error(`token status=${status}, refresh_token 也过期, 需要重新 device flow`);
}

/**
 *   plugin client.getAccessToken 看到 status=valid 直接 return, 不 refresh
 *   修法: 直接 fetch refresh endpoint (RFC 6749 §6), 拿新 token, 写 Keychain
 *
 * 注意: 不依赖 plugin runtime, 只 import dist 文件 (plugin 是 source of truth 的写入方,
 * 但这个 fallback 让 skill 能在 plugin 进程不在时也强刷一次)
 */
async function directRefreshAndWrite(client, t) {
  // plugin 端 token URL (从 dist 拿不到, hardcode 同 plugin src)
  // OPPHUB_OAUTH_TOKEN_URL: 测试环境 override token endpoint URL (不是 token 本身!)
  // ClawHub audit flagged env_credential_access - 这只是 URL 配置, 不是 token
  const TOKEN_URL = process.env.OPPHUB_OAUTH_TOKEN_URL ||
    "https://api.opphub.ruiplus.cn/api/oauth/token";

  if (!t.refresh_token) {
    throw new Error("refresh_token 缺失, 不能 refresh");
  }

  const r = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: t.refresh_token,
      client_id: "opphub-plugin",
    }),
  });
  if (!r.ok) {
    const text = await r.text().catch(() => "");
    throw new Error(`refresh ${r.status}: ${text}`);
  }
  const j = await r.json();
  if (!j.access_token) {
    throw new Error(`refresh 返 access_token 缺失: ${JSON.stringify(j)}`);
  }

  // 写 Keychain (走 plugin client.writeToken, 让 plugin = source of truth)
  const newToken = {
    access_token: j.access_token,
    refresh_token: j.refresh_token ?? t.refresh_token,  // RFC 6749 §6 rotation
    expires_at: Date.now() + (j.expires_in ?? 3600) * 1000,
    refresh_expires_at: Date.now() + (j.refresh_expires_in ?? 30 * 24 * 3600) * 1000,
    scope: j.scope ?? t.scope,
    user_id: t.user_id,
    obtained_at: new Date().toISOString(),
  };
  await client.writeToken(newToken);

  return newToken;
}

/**
 * 解 JWT payload (从 access_token 拿 userId)
 */
export async function getOpcIdFromToken(t) {
  const client = await loadPluginClient();
  if (typeof client.getOpcIdFromToken === "function") return client.getOpcIdFromToken(t);
  // plugin 不暴露此函数, 走 decodeJwtPayload
  if (typeof client.decodeJwtPayload === "function") {
    const p = client.decodeJwtPayload(t?.access_token);
    return p?.userId ?? p?.sub ?? null;
  }
  return null;
}

/**
 * 启动 device flow (走 plugin client, plugin 自己有打开浏览器兜底)
 */
export async function deviceFlowLogin(opts = {}) {
  const client = await loadPluginClient();
  return await client.deviceFlowLogin(opts.scope, opts.timeoutMs, { openBrowser: false, ...opts });
}

// === 健康检查 ===

/**
 * 看 plugin client 能不能加载到
 * 返 { ok, path?, version?, error? }
 */
export async function healthCheck() {
  const path = findPluginClientPath();
  if (!path) return { ok: false, error: "plugin dist 路径找不到" };
  try {
    const client = await loadPluginClient();
    return {
      ok: true,
      path,
      pkgVersion: client.PKG_VERSION ?? null,
    };
  } catch (e) {
    return { ok: false, path, error: e?.message ?? String(e) };
  }
}

// === CommonJS 兼容 ===
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    readToken,
    writeToken,
    tokenStatus,
    getAccessToken,
    refreshToken,
    getOpcIdFromToken,
    deviceFlowLogin,
    healthCheck,
    loadPluginClient,
    findPluginClientPath,
  };
}
