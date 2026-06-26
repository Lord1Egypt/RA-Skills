import { getCredentials } from './credentials.js';

const BASE_URL = 'https://api.organizze.com.br/rest/v2';

function buildHeaders() {
  const { email, token, userAgent } = getCredentials();
  const basicAuth = Buffer.from(`${email}:${token}`).toString('base64');

  return {
    'Authorization': `Basic ${basicAuth}`,
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': userAgent,
  };
}

async function request(method, path, body) {
  const url = `${BASE_URL}${path}`;
  const options = {
    method,
    headers: buildHeaders(),
  };

  if (body !== undefined) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;

  if (!response.ok) {
    const message = data?.error || JSON.stringify(data) || response.statusText;
    throw new Error(`${method} ${path} failed (${response.status}): ${message}`);
  }

  return data;
}

export const client = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
  put: (path, body) => request('PUT', path, body),
  del: (path, body) => request('DELETE', path, body),
};
