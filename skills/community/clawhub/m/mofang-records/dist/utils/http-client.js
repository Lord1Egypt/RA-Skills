/**
 * 统一 HTTP 请求封装
 * 负责 Token 管理、请求发送、错误处理和自动重试
 */
const TOKEN_VALIDITY_MS = 25 * 60 * 1000; // 25分钟，比30分钟有效期提前刷新
let cachedToken = null;
function normalizeBaseUrl(baseUrl) {
    return baseUrl.replace(/\/+$/, '');
}
function getFetchTimeoutMs() {
    const n = Number(process.env.FETCH_TIMEOUT_MS);
    if (Number.isFinite(n) && n > 0)
        return n;
    return 120_000;
}
export async function fetchWithTimeout(url, init = {}) {
    const ms = getFetchTimeoutMs();
    try {
        return await fetch(url, { ...init, signal: AbortSignal.timeout(ms) });
    }
    catch (err) {
        if (err?.name === 'TimeoutError' || err?.name === 'AbortError') {
            throw new Error(`请求超时（${Math.round(ms / 1000)}s 内无响应），请检查 BASE_URL、网络或 VPN：${url}`);
        }
        throw err;
    }
}
/** BOM/空白或非 application/json 但正文为 JSON 时的兼容解析 */
function parseResponseJson(text) {
    const trimmed = text.replace(/^\uFEFF/, '').trim();
    if (!trimmed)
        return {};
    return JSON.parse(trimmed);
}
function isTokenExpired() {
    if (!cachedToken)
        return true;
    return Date.now() - cachedToken.obtainedAt > TOKEN_VALIDITY_MS;
}
export async function obtainToken(config) {
    const url = `${normalizeBaseUrl(config.baseUrl)}/magicflu/jwt`;
    const body = `j_username=${encodeURIComponent(config.username)}&j_password=${encodeURIComponent(config.password)}`;
    const response = await fetchWithTimeout(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
    });
    if (!response.ok) {
        throw new Error(`Token 获取失败: HTTP ${response.status}`);
    }
    const raw = await response.text();
    let data;
    try {
        data = parseResponseJson(raw);
    }
    catch {
        const preview = raw.length > 160 ? `${raw.slice(0, 160)}…` : raw;
        throw new Error(`Token 获取失败: 响应非 JSON。${preview.replace(/\s+/g, ' ')}`);
    }
    if (!data.token) {
        throw new Error(`Token 获取失败: ${JSON.stringify(data)}`);
    }
    cachedToken = {
        token: data.token,
        obtainedAt: Date.now(),
        nickname: data.nickname || '',
        username: data.username || '',
        userId: data.id || '',
    };
    return cachedToken;
}
export async function getToken(config) {
    if (isTokenExpired()) {
        await obtainToken(config);
    }
    return cachedToken.token;
}
export function clearTokenCache() {
    cachedToken = null;
}
export function getTokenInfo() {
    return cachedToken;
}
export async function apiRequest(config, method, path, body, isRetry = false) {
    const token = await getToken(config);
    const url = `${normalizeBaseUrl(config.baseUrl)}${path.startsWith('/') ? path : `/${path}`}`;
    const headers = {
        Authorization: `Bearer ${token}`,
    };
    if (body !== undefined && (method === 'POST' || method === 'PUT')) {
        headers['Content-Type'] = 'application/json';
    }
    const fetchOptions = { method, headers };
    if (body !== undefined && (method === 'POST' || method === 'PUT')) {
        fetchOptions.body = JSON.stringify(body);
    }
    let response;
    try {
        response = await fetchWithTimeout(url, fetchOptions);
    }
    catch (err) {
        return { success: false, message: `网络请求失败: ${err.message}` };
    }
    if (response.status === 500 && !isRetry) {
        clearTokenCache();
        return apiRequest(config, method, path, body, true);
    }
    const raw = await response.text();
    let data;
    try {
        data = parseResponseJson(raw);
    }
    catch {
        const preview = raw.length > 160 ? `${raw.slice(0, 160)}…` : raw;
        return {
            success: false,
            message: `响应解析失败: HTTP ${response.status}，正文非合法 JSON。片段: ${preview.replace(/\s+/g, ' ')}`,
        };
    }
    if (!response.ok) {
        const errMsg = data?.errmsg || data?.message || `HTTP ${response.status}`;
        return { success: false, message: `请求失败: ${errMsg}`, data };
    }
    return { success: true, data, message: 'ok' };
}
/** URL-Safe Base64，与 Java Base64.encodeBase64URLSafeString(utf8(userId)) 对齐 */
export function currentUserDigitalIdCookie(userId) {
    return Buffer.from(userId, 'utf8').toString('base64url');
}
/**
 * Activiti / BPM 相关请求：Bearer + Cookie CURRENT_USER_DIGITALID（与前端、Java RESTCaller 一致）。
 * 兼容 204、正文为纯文本 ok、非 JSON。
 */
export async function bpmRequest(config, method, path, body, extraCookie, isRetry = false) {
    await obtainToken(config);
    const info = getTokenInfo();
    if (!info) {
        return { success: false, message: '未获取到 Token 信息。' };
    }
    const url = `${normalizeBaseUrl(config.baseUrl)}${path.startsWith('/') ? path : `/${path}`}`;
    const headers = {
        Authorization: `Bearer ${info.token}`,
        Accept: 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
    };
    const parts = [];
    const digitalLogin = (info.username || info.userId || '').trim();
    if (digitalLogin) {
        parts.push(`CURRENT_USER_DIGITALID=${currentUserDigitalIdCookie(digitalLogin)}`);
    }
    if (extraCookie) {
        parts.push(extraCookie);
    }
    if (parts.length > 0) {
        headers.Cookie = parts.join('; ');
    }
    const init = { method, headers };
    if (body !== undefined && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        headers['Content-Type'] = 'application/json';
        init.body = JSON.stringify(body);
    }
    let response;
    try {
        response = await fetchWithTimeout(url, init);
    }
    catch (err) {
        return { success: false, message: `网络请求失败: ${err.message}` };
    }
    if (response.status === 500 && !isRetry) {
        clearTokenCache();
        return bpmRequest(config, method, path, body, extraCookie, true);
    }
    if (response.status === 204) {
        return { success: true, data: null, message: 'ok' };
    }
    const raw = await response.text();
    const trimmed = raw.replace(/^\uFEFF/, '').trim();
    if (response.ok && (trimmed === '' || trimmed === 'ok')) {
        return { success: true, data: trimmed === 'ok' ? { ok: true } : null, message: 'ok' };
    }
    if (response.ok && trimmed === 'success') {
        return { success: true, data: { success: true }, message: 'ok' };
    }
    if (response.ok && trimmed.startsWith('<')) {
        return { success: true, data: { xml: trimmed }, message: 'ok' };
    }
    let data;
    if (trimmed && (trimmed.startsWith('{') || trimmed.startsWith('['))) {
        try {
            data = parseResponseJson(trimmed);
        }
        catch {
            if (!response.ok) {
                return {
                    success: false,
                    message: `HTTP ${response.status}，正文非 JSON: ${trimmed.slice(0, 200)}`,
                };
            }
            return { success: true, data: { raw: trimmed }, message: 'ok' };
        }
        if (!response.ok) {
            const errMsg = data?.message || data?.exception || data?.errmsg || `HTTP ${response.status}`;
            return { success: false, message: `请求失败: ${errMsg}`, data };
        }
        return { success: true, data, message: 'ok' };
    }
    if (!response.ok) {
        return {
            success: false,
            message: `请求失败: HTTP ${response.status} ${trimmed.slice(0, 240)}`,
        };
    }
    return { success: true, data: trimmed ? { raw: trimmed } : null, message: 'ok' };
}
/**
 * 与 bpmRequest 相同鉴权，可发 JSON 或原始正文（如 `updateDesc` 的空 body）。
 */
export async function bpmFetch(config, method, path, options, isRetry = false) {
    await obtainToken(config);
    const info = getTokenInfo();
    if (!info) {
        return { success: false, message: '未获取到 Token 信息。' };
    }
    const url = `${normalizeBaseUrl(config.baseUrl)}${path.startsWith('/') ? path : `/${path}`}`;
    const headers = {
        Authorization: `Bearer ${info.token}`,
        Accept: 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
    };
    const parts = [];
    const digitalLogin = (info.username || info.userId || '').trim();
    if (digitalLogin) {
        parts.push(`CURRENT_USER_DIGITALID=${currentUserDigitalIdCookie(digitalLogin)}`);
    }
    if (options?.extraCookie) {
        parts.push(options.extraCookie);
    }
    if (parts.length > 0) {
        headers.Cookie = parts.join('; ');
    }
    const init = { method, headers };
    if (options?.jsonBody !== undefined) {
        headers['Content-Type'] = 'application/json';
        init.body = JSON.stringify(options.jsonBody);
    }
    else if (options?.textBody !== undefined) {
        headers['Content-Type'] = 'application/json';
        init.body = options.textBody;
    }
    let response;
    try {
        response = await fetchWithTimeout(url, init);
    }
    catch (err) {
        return { success: false, message: `网络请求失败: ${err.message}` };
    }
    if (response.status === 500 && !isRetry) {
        clearTokenCache();
        return bpmFetch(config, method, path, options, true);
    }
    if (response.status === 204) {
        return { success: true, data: null, message: 'ok' };
    }
    const raw = await response.text();
    const trimmed = raw.replace(/^\uFEFF/, '').trim();
    if (response.ok && (trimmed === '' || trimmed === 'ok')) {
        return { success: true, data: trimmed === 'ok' ? { ok: true } : null, message: 'ok' };
    }
    if (response.ok && trimmed === 'success') {
        return { success: true, data: { success: true }, message: 'ok' };
    }
    if (response.ok && trimmed.startsWith('<')) {
        return { success: true, data: { xml: trimmed }, message: 'ok' };
    }
    let data;
    if (trimmed && (trimmed.startsWith('{') || trimmed.startsWith('['))) {
        try {
            data = parseResponseJson(trimmed);
        }
        catch {
            if (!response.ok) {
                return {
                    success: false,
                    message: `HTTP ${response.status}，正文非 JSON: ${trimmed.slice(0, 200)}`,
                };
            }
            return { success: true, data: { raw: trimmed }, message: 'ok' };
        }
        if (!response.ok) {
            const errMsg = data?.message || data?.exception || data?.errmsg || `HTTP ${response.status}`;
            return { success: false, message: `请求失败: ${errMsg}`, data };
        }
        return { success: true, data, message: 'ok' };
    }
    if (!response.ok) {
        return {
            success: false,
            message: `请求失败: HTTP ${response.status} ${trimmed.slice(0, 240)}`,
        };
    }
    return { success: true, data: trimmed ? { raw: trimmed } : null, message: 'ok' };
}
//# sourceMappingURL=http-client.js.map