/**
 * KreadoAI HTTP 客户端（零外部依赖，Node.js 18+ fetch）
 *
 * 基础 URL：https://api.kreadoai.com
 * 鉴权：HTTP 头 `apiToken: <token>`
 */
import { getApiToken, getSkillVersion } from './auth.mjs';

const API_BASE = 'https://api.kreadoai.com';

function makeHeaders(token) {
  return {
    'Content-Type': 'application/json',
    'apiToken': token,
    'User-Agent': `KreadoAI-Skill/${getSkillVersion()}`,
  };
}

function parseResponse(json) {
  const code = String(json.code || '');
  if (code !== '200') {
    const msg = json.message || '未知错误';
    throw new Error(`API 错误 (code=${code})：${msg}`);
  }
  return json.data;
}

async function safeFetch(url, init) {
  try {
    return await fetch(url, init);
  } catch (e) {
    throw new Error(
      `网络错误：${e?.message || e}\n`
      + `请求：${init.method} ${url}\n`
      + '提示：KreadoAI 服务部署在新加坡，中国用户可能速度较慢。',
    );
  }
}

/**
 * POST 请求 KreadoAI API
 * @param {string} path API 路径
 * @param {object} body 请求体
 * @param {string} [token] 可选 token
 * @returns {Promise<object>} data 字段
 */
export async function kreadoPost(path, body, token) {
  if (!token) token = getApiToken();
  const url = `${API_BASE}${path}`;
  const res = await safeFetch(url, {
    method: 'POST',
    headers: makeHeaders(token),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status}：${text}`);
  }
  const json = await res.json();
  return parseResponse(json);
}

/**
 * GET 请求 KreadoAI API
 * @param {string} path API 路径
 * @param {string} [token] 可选 token
 * @returns {Promise<object>} data 字段
 */
export async function kreadoGet(path, token) {
  if (!token) token = getApiToken();
  const url = `${API_BASE}${path}`;
  const res = await safeFetch(url, {
    method: 'GET',
    headers: makeHeaders(token),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status}：${text}`);
  }
  const json = await res.json();
  return parseResponse(json);
}

export { API_BASE };
