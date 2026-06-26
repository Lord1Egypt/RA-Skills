function baseUrl() {
  const u = process.env.KRYPTONE_API_BASE_URL || process.env.API_BASE_URL;
  if (!u || String(u).trim() === '') {
    throw new Error('Set KRYPTONE_API_BASE_URL (e.g. http://localhost:5001)');
  }
  return String(u).replace(/\/$/, '');
}

function apiKey() {
  const k = process.env.AGENT_API_KEY;
  if (!k || String(k).trim() === '') {
    throw new Error('Set AGENT_API_KEY (must match server AGENT_API_KEY)');
  }
  return k;
}

/**
 * @param {string} method
 * @param {string} path
 * @param {object} [body]
 * @param {Record<string, string>} [extraHeaders]
 */
export async function apiRequest(method, path, body, extraHeaders = {}) {
  const root = baseUrl();
  const p = path.startsWith('/') ? path : `/${path}`;
  const url = `${root}${p}`;
  const headers = {
    'x-api-key': apiKey(),
    ...extraHeaders,
  };
  const init = { method, headers };
  if (body !== undefined && method !== 'GET' && method !== 'HEAD') {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(body);
  }
  const res = await fetch(url, init);
  const text = await res.text();
  let parsed;
  try {
    parsed = text ? JSON.parse(text) : null;
  } catch {
    parsed = { _raw: text };
  }
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status}`);
    err.status = res.status;
    err.body = parsed;
    throw err;
  }
  return parsed;
}

export function printJson(data) {
  console.log(JSON.stringify(data, null, 2));
}
