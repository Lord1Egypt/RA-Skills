#!/usr/bin/env node
const https = require('https');

function fetchJson(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'openclaw-ip-lookup/1.0 (+local skill)',
        'Accept': 'application/json',
        ...headers
      }
    }, (res) => {
      let data = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (err) {
          reject(err);
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(8000, () => req.destroy(new Error('Request timeout')));
  });
}

async function reverseGeocodeZh(loc) {
  if (!loc || typeof loc !== 'string' || !loc.includes(',')) return null;
  const [lat, lon] = loc.split(',').map((x) => x.trim());
  if (!lat || !lon) return null;

  // OpenStreetMap Nominatim reverse geocoding (best-effort, may be rate-limited)
  const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}&zoom=10&addressdetails=1`;
  const data = await fetchJson(url, {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.3'
  });

  const addr = data && data.address ? data.address : {};
  const cityZh = addr.city || addr.town || addr.village || addr.county || null;
  const countryCode = addr.country_code ? String(addr.country_code).toUpperCase() : null;
  return { cityZh, countryCode, raw: data };
}

async function queryIp() {
  const sources = [
    { url: 'https://ipinfo.io/json', source: 'ipinfo.io' },
    { url: 'https://ifconfig.co/json', source: 'ifconfig.co' },
    { url: 'https://api.ip.sb/geoip', source: 'ip.sb' }
  ];

  const errors = [];
  for (const s of sources) {
    try {
      const data = await fetchJson(s.url);
      return { raw: data, source: s.source };
    } catch (err) {
      errors.push({ source: s.source, error: err.message || String(err) });
    }
  }

  const error = new Error('All IP info sources failed');
  error.details = errors;
  throw error;
}

async function normalize(result) {
  const { raw, source } = result;
  const now = new Date().toISOString();

  // Try to map common fields across providers
  const ip = raw.ip || raw.query || raw.address || null;
  const city = raw.city || raw.regionName || raw.city_name || null;
  const region = raw.region || raw.regionName || raw.region_name || null;
  const country = raw.country || raw.country_code || raw.countryCode || null;
  const org = raw.org || raw.as || raw.organization || null;
  const loc = raw.loc || (raw.latitude && raw.longitude ? `${raw.latitude},${raw.longitude}` : null);

  // Best-effort: fetch Chinese city name from coordinates (optional)
  let cityZh = null;
  try {
    if (loc) {
      const r = await reverseGeocodeZh(loc);
      if (r && r.cityZh) cityZh = r.cityZh;
    }
  } catch (_) {
    // ignore; keep cityZh null
  }

  return {
    ip,
    city,
    cityZh,
    region,
    country,
    org,
    loc,
    source,
    fetchedAt: now,
    raw
  };
}

function formatHuman(info) {
  if (!info || !info.ip) {
    return '暂时无法获取公网 IP，请稍后重试或检查网络连接。';
  }

  const locationParts = [];
  if (info.city) locationParts.push(info.city);
  if (info.country) locationParts.push(info.country);
  const cityEn = locationParts.length ? locationParts.join(', ') : '未知';

  const cityLine = info.cityZh ? `${info.cityZh}（${cityEn}）` : cityEn;

  const parts = [];
  parts.push(`公网 IP：${info.ip}`);
  parts.push(`城市：${cityLine}`);
  if (info.org) parts.push(`运营商：${info.org}`);
  return parts.join('\n');
}

async function main() {
  const wantJson = process.argv.slice(2).includes('--json');
  try {
    const result = await queryIp();
    const info = await normalize(result);
    if (wantJson) {
      process.stdout.write(JSON.stringify(info, null, 2));
    } else {
      process.stdout.write(formatHuman(info));
    }
  } catch (err) {
    if (wantJson) {
      process.stdout.write(JSON.stringify({ error: err.message || String(err), details: err.details || null }, null, 2));
    } else {
      process.stderr.write(`获取公网 IP 失败：${err.message || String(err)}\n`);
    }
    process.exit(1);
  }
}

main();
