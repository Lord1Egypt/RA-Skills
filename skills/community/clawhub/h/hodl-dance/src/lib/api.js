const BASE_URL = 'https://hodl.dance/api';

async function apiFetch(path, params = {}) {
  const url = new URL(BASE_URL + path);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, v);
  });
  const res = await fetch(url.toString(), { headers: { 'Accept': 'application/json' } });
  const json = await res.json();
  if (!res.ok || !json.success) {
    throw new Error(json.message || json.error || `HTTP ${res.status}`);
  }
  return json.data;
}

module.exports = { apiFetch };
