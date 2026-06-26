/**
 * OB connection wrapper — restore identity, send JSON, listen for messages.
 * Thin wrapper around createOceanBus() from oceanbus SDK.
 */
import { createOceanBus } from "oceanbus";
import { loadOrCreateIdentity } from "./identity.js";

const BASE_URL = process.env.OCEANBUS_URL || "https://ai.ihaola.com.cn/api/l0";

let _ob = null;
let _openid = null;
let _initPromise = null;

export async function getClient() {
  if (_initPromise) return _initPromise;
  _initPromise = _doInit();
  return _initPromise;
}

async function _doInit() {
  const result = await loadOrCreateIdentity((config) =>
    createOceanBus({ ...config, baseUrl: BASE_URL })
  );
  _ob = result.ob;
  _openid = result.openid;
  return { ob: _ob, openid: _openid, agentId: result.agentId, created: result.created };
}

export async function getOpenId() {
  // Wrapper — returns the cached OpenID (SDK getAddress under the hood)
  if (!_openid) await getClient();
  return _openid;
}

export async function sendJson(to, data) {
  const { ob } = await getClient();
  return ob.sendJson(to, data);
}

export async function startListening(handler, opts = {}) {
  const { ob } = await getClient();
  return ob.startListening(handler, {
    intervalMs: opts.intervalMs || 3000,
    skipSelf: opts.skipSelf !== false,
  });
}

export async function stopListening() {
  if (_ob) {
    try { await _ob.destroy(); } catch (_) {}
    _ob = null;
    _openid = null;
    _initPromise = null;
  }
}
