import fs from 'node:fs';
import path from 'node:path';

const LOOPBACK_HOSTS = new Set(['127.0.0.1', 'localhost', '::1']);

function normalizeBaseUrl(baseUrl) {
  return String(baseUrl || 'http://127.0.0.1:3000').replace(/\/$/u, '');
}

function isRemoteBaseUrlAllowed() {
  // SAFETY NOTICE:
  // This env var is only a local operator override for trusted environments.
  // Network egress remains localhost-only by default via assertSafeBaseUrl().
  // Non-loopback hosts are blocked unless this explicit opt-in is set.
  const flag = String(process.env.MATRIX_MATE_ALLOW_REMOTE_BASE_URL || '').trim().toLowerCase();
  return flag === '1' || flag === 'true' || flag === 'yes';
}

function assertSafeBaseUrl(baseUrl) {
  let parsedUrl;
  try {
    parsedUrl = new URL(baseUrl);
  } catch {
    throw new Error(`Invalid MATRIX_MATE_BASE_URL: ${baseUrl}`);
  }

  if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
    throw new Error('MATRIX_MATE_BASE_URL must use http or https protocol.');
  }

  if (LOOPBACK_HOSTS.has(parsedUrl.hostname)) {
    return;
  }

  if (isRemoteBaseUrlAllowed()) {
    return;
  }

  throw new Error(
    `Refusing non-loopback MATRIX_MATE_BASE_URL (${baseUrl}). Set MATRIX_MATE_ALLOW_REMOTE_BASE_URL=true only if you explicitly trust the remote host.`,
  );
}

export function resolveSkillRoot(startCwd = process.cwd()) {
  const directSkill = path.resolve(startCwd);
  if (fs.existsSync(path.join(directSkill, 'SKILL.md')) && fs.existsSync(path.join(directSkill, 'scripts', 'run-offline-mcp.mjs'))) {
    return directSkill;
  }

  const nestedSkill = path.resolve(startCwd, 'skills', 'matrix-mate-offline');
  if (fs.existsSync(path.join(nestedSkill, 'SKILL.md')) && fs.existsSync(path.join(nestedSkill, 'scripts', 'run-offline-mcp.mjs'))) {
    return nestedSkill;
  }

  return directSkill;
}

export function createMatrixMateClient({ baseUrl = process.env.MATRIX_MATE_BASE_URL, fetchImpl = fetch } = {}) {
  const normalizedBaseUrl = normalizeBaseUrl(baseUrl);
  assertSafeBaseUrl(normalizedBaseUrl);

  async function requestJson(urlPath, init = {}) {
    const response = await fetchImpl(`${normalizedBaseUrl}${urlPath}`, {
      headers: {
        'content-type': 'application/json',
        ...(init.headers || {}),
      },
      ...init,
    });

    const text = await response.text();
    let payload = null;
    try {
      payload = text ? JSON.parse(text) : null;
    } catch {
      payload = null;
    }

    return {
      ok: response.ok,
      status: response.status,
      payload,
      text,
    };
  }

  return {
    baseUrl: normalizedBaseUrl,
    async checkLocalHealth() {
      const response = await fetchImpl(`${normalizedBaseUrl}/`);
      const text = await response.text();
      const titleDetected = /Matrix Mate/u.test(text);
      return {
        ok: response.ok,
        baseUrl: normalizedBaseUrl,
        status: response.status,
        titleDetected,
        message: response.ok
          ? 'Local Matrix Mate app responded successfully.'
          : `Local Matrix Mate app returned status ${response.status}.`,
      };
    },
    async parseMatrixLink(matrixUrl) {
      return requestJson('/v1/intake/matrix-link', {
        method: 'POST',
        body: JSON.stringify({ matrix_url: matrixUrl }),
      });
    },
    async parseManualItinerary({ itaJson, rulesBundle }) {
      return requestJson('/v1/intake/ita', {
        method: 'POST',
        body: JSON.stringify({
          ita_json: itaJson,
          ...(rulesBundle ? { rules_bundle: rulesBundle } : {}),
        }),
      });
    },
    async getTrip(id) {
      return requestJson(`/v1/trips/${encodeURIComponent(id)}`);
    },
    async exportTrip(id) {
      return requestJson(`/v1/trips/${encodeURIComponent(id)}/export`);
    },
    async getFutureBookingIntent(id) {
      return requestJson(`/v1/trips/${encodeURIComponent(id)}/future-booking-intent`);
    },
  };
}
