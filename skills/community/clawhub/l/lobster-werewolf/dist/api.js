/**
 * HTTP client 模块 —— 薄壳转发到 Python werewolf server
 */

// Default points to lobster-republic 的美国测试服 (Aliyun US Virginia).
// 任何部署方可通过 plugin config.serverUrl 覆盖为本地或自建地址。
let SERVER_URL = "http://47.85.184.157:8801";

export function configure(serverUrl) {
    if (serverUrl) SERVER_URL = serverUrl;
}

export function getServerUrl() {
    return SERVER_URL;
}

/**
 * 调用 werewolf server 的 HTTP API
 * @param {string} method GET / POST
 * @param {string} path e.g. "/create_table"
 * @param {object} body (可选) POST body
 * @returns {Promise<object>} response JSON
 */
export async function callServer(method, path, body = null) {
    const url = `${SERVER_URL}${path}`;
    const opts = {
        method,
        headers: { "Content-Type": "application/json" },
    };
    if (body) opts.body = JSON.stringify(body);
    try {
        const resp = await fetch(url, opts);
        const text = await resp.text();
        try {
            const json = JSON.parse(text);
            if (!resp.ok) {
                return { _http_error: resp.status, _http_body: json };
            }
            return json;
        } catch {
            return { _http_error: resp.status, _raw: text };
        }
    } catch (e) {
        return { _network_error: String(e), url };
    }
}
