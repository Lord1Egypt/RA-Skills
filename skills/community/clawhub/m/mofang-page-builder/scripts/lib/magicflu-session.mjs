/**
 * 魔方会话：JWT + Cookie、超时 fetch（deploy / mock-jsonv2 proxy 共用）
 */

export function normalizeBaseUrl(url) {
  return String(url || '').replace(/\/+$/, '');
}

export function getFetchTimeoutMs() {
  const n = Number(process.env.FETCH_TIMEOUT_MS);
  if (Number.isFinite(n) && n > 0) return n;
  return 120_000;
}

/** 带超时的 fetch，避免对端不返回时脚本无限挂起 */
export async function fetchWithTimeout(url, init = {}) {
  const ms = getFetchTimeoutMs();
  try {
    return await fetch(url, { ...init, signal: AbortSignal.timeout(ms) });
  } catch (e) {
    if (e?.name === 'TimeoutError' || e?.name === 'AbortError') {
      throw new Error(`请求超时（${ms / 1000}s 内无响应），请检查 BASE_URL 是否可达、网络/VPN：${url}`);
    }
    throw e;
  }
}

function parseResponseJson(text) {
  const trimmed = String(text || '').replace(/^\uFEFF/, '').trim();
  if (!trimmed) return {};
  return JSON.parse(trimmed);
}

/** 从响应头取出 Set-Cookie 各行，解析为 name=value（忽略属性） */
export function pairsFromSetCookieResponse(res) {
  const pairs = [];
  const h = res.headers;
  if (typeof h.getSetCookie === 'function') {
    for (const line of h.getSetCookie()) {
      const part = line.split(';')[0].trim();
      if (part && part.includes('=')) pairs.push(part);
    }
    return pairs;
  }
  const single = h.get('set-cookie');
  if (!single) return [];
  const part = single.split(';')[0].trim();
  return part && part.includes('=') ? [part] : [];
}

/** 合并两段 Cookie 请求头（后者覆盖同名） */
export function mergeCookieHeader(a, b) {
  const jar = new Map();
  const ingest = (hdr) => {
    if (!hdr) return;
    for (const piece of hdr.split(';')) {
      const t = piece.trim();
      if (!t || !t.includes('=')) continue;
      const eq = t.indexOf('=');
      const name = t.slice(0, eq).trim();
      const val = t.slice(eq + 1).trim();
      if (name) jar.set(name, val);
    }
  };
  ingest(a);
  ingest(b);
  return [...jar.entries()].map(([n, v]) => `${n}=${v}`).join('; ');
}

/**
 * JWT 登录并尽量拿到可用于业务接口的 Cookie。
 * @returns {{ cookie: string, token: string }}
 */
export async function obtainSessionCookieFromCredentials(baseUrl, username, password) {
  const root = normalizeBaseUrl(baseUrl);
  const jwtUrl = `${root}/magicflu/jwt`;
  const body = `j_username=${encodeURIComponent(username)}&j_password=${encodeURIComponent(password)}`;

  const jwtRes = await fetchWithTimeout(jwtUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });

  if (!jwtRes.ok) {
    const t = await jwtRes.text();
    throw new Error(`JWT 登录失败 HTTP ${jwtRes.status}: ${t.slice(0, 300)}`);
  }

  const raw = await jwtRes.text();
  let data;
  try {
    data = parseResponseJson(raw);
  } catch {
    throw new Error(`JWT 响应非 JSON: ${raw.slice(0, 200)}`);
  }
  if (!data.token) {
    throw new Error(`JWT 未返回 token: ${JSON.stringify(data)}`);
  }

  let cookie = mergeCookieHeader('', pairsFromSetCookieResponse(jwtRes).join('; '));

  if (!cookie) {
    const probeUrl = `${root}/magicflu/service/json/spaces/feed?start=0&limit=1`;
    const probeRes = await fetchWithTimeout(probeUrl, {
      headers: { Authorization: `Bearer ${data.token}` },
    });
    const fromProbe = pairsFromSetCookieResponse(probeRes).join('; ');
    cookie = mergeCookieHeader(cookie, fromProbe);
  }

  if (!cookie) {
    throw new Error(
      'JWT 已成功但未能从 Set-Cookie 得到会话。请改用 --cookie 传入浏览器 Cookie，或升级 Node 至 20+ 以正确解析多 Set-Cookie。',
    );
  }

  return { cookie, token: data.token };
}
