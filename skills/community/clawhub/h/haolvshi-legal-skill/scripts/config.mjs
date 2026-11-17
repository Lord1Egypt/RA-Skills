import os from 'node:os';
import path from 'node:path';

export const DEFAULT_CONFIG = Object.freeze({
  apiBase: 'https://front.ai.lvpin100.com/api/speed-front',
  siteBase: 'https://skill.ai.lvpin100.com',
  siteRouteBase: '',
  appId: '9BED559BDD9CE535B3E5BE25A63ED00E',
  deviceType: 1,
  userAgent: 'haolvshi-legal-skill/1.0',
  requestTimeoutMs: 30_000,
  auditTimeoutMs: 180_000,
  stateTtlMs: 24 * 60 * 60 * 1000,
  stateDir: path.join(os.tmpdir(), 'haolvshi-legal-skill')
});

function env(primary, legacy) {
  return process.env[primary] || process.env[legacy];
}

function positiveInteger(value, fallback) {
  const parsed = Number.parseInt(value ?? '', 10);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : fallback;
}

export function loadConfig(overrides = {}) {
  const config = {
    ...DEFAULT_CONFIG,
    apiBase: env('HAOLVSHI_API_BASE', 'LVPIN_API_BASE') || DEFAULT_CONFIG.apiBase,
    siteBase: env('HAOLVSHI_SITE_BASE', 'LVPIN_SITE_BASE') || DEFAULT_CONFIG.siteBase,
    siteRouteBase: env('HAOLVSHI_SITE_ROUTE_BASE', 'LVPIN_SITE_ROUTE_BASE') || DEFAULT_CONFIG.siteRouteBase,
    appId: env('HAOLVSHI_APP_ID', 'LVPIN_APP_ID') || DEFAULT_CONFIG.appId,
    deviceType: positiveInteger(env('HAOLVSHI_DEVICE_TYPE', 'LVPIN_DEVICE_TYPE'), DEFAULT_CONFIG.deviceType),
    requestTimeoutMs: positiveInteger(
      env('HAOLVSHI_REQUEST_TIMEOUT_MS', 'LVPIN_REQUEST_TIMEOUT_MS'),
      DEFAULT_CONFIG.requestTimeoutMs
    ),
    auditTimeoutMs: positiveInteger(
      env('HAOLVSHI_AUDIT_TIMEOUT_MS', 'LVPIN_AUDIT_TIMEOUT_MS'),
      DEFAULT_CONFIG.auditTimeoutMs
    ),
    stateDir: env('HAOLVSHI_STATE_DIR', 'LVPIN_STATE_DIR') || DEFAULT_CONFIG.stateDir,
    ...overrides
  };

  config.apiBase = String(config.apiBase).replace(/\/+$/, '');
  config.siteBase = String(config.siteBase).replace(/\/+$/, '');
  config.siteRouteBase = String(config.siteRouteBase || '')
    .trim()
    .replace(/^([^/])/, '/$1')
    .replace(/\/+$/, '');
  return config;
}
