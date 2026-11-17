// Pure helpers for openmeteo-daybrief. Input is an Open-Meteo /v1/forecast response requested
// with the hourly/daily fields listed in daybrief and timezone=<IANA zone> (local wall-clock times).

const WMO = {
  0: 'clear', 1: 'mainly clear', 2: 'partly cloudy', 3: 'overcast', 45: 'fog', 48: 'freezing fog',
  51: 'light drizzle', 53: 'drizzle', 55: 'heavy drizzle', 56: 'freezing drizzle', 57: 'freezing drizzle',
  61: 'light rain', 63: 'moderate rain', 65: 'heavy rain', 66: 'freezing rain', 67: 'freezing rain',
  71: 'light snow', 73: 'snow', 75: 'heavy snow', 77: 'snow grains', 80: 'rain showers', 81: 'rain showers',
  82: 'violent rain showers', 85: 'snow showers', 86: 'snow showers', 95: 'thunderstorm', 96: 'thunderstorm with hail', 99: 'thunderstorm with hail',
};

export const describeCode = (code) => WMO[code] ?? 'unknown';

const toMin = (hhmm) => {
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m;
};
const fmt = (min) => `${String(Math.floor(min / 60)).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;
const wet = (precip, code) => precip >= 30 || code >= 51;

function hoursOf(fx, date) {
  const h = fx.hourly;
  return h.time
    .map((t, i) => ({ t, hour: Number(t.slice(11, 13)), temp: h.temperature_2m[i], precip: h.precipitation_probability[i], code: h.weather_code[i] }))
    .filter((x) => x.t.startsWith(date));
}

function dayIndex(fx, date) {
  const i = fx.daily.time.indexOf(date);
  if (i < 0) throw new Error(`date ${date} not in forecast`);
  return i;
}

function ranges(hours) {
  const out = [];
  for (const h of hours) {
    const last = out.at(-1);
    if (last && last[1] === h * 60) last[1] = h * 60 + 60;
    else out.push([h * 60, h * 60 + 60]);
  }
  return out;
}

export function summarizeDay(fx, date) {
  const i = dayIndex(fx, date);
  const d = fx.daily;
  const rain = ranges(hoursOf(fx, date).filter((x) => x.precip >= 50).map((x) => x.hour));
  return {
    date,
    condition: describeCode(d.weather_code[i]),
    high: d.temperature_2m_max[i],
    low: d.temperature_2m_min[i],
    unit: fx.daily_units?.temperature_2m_max || '°C',
    precipChanceMax: d.precipitation_probability_max[i],
    rainHours: rain.length ? rain.map(([s, e]) => `${fmt(s)}-${fmt(e - 1)}`).join(', ') : null,
    sunrise: d.sunrise[i].slice(11, 16),
    sunset: d.sunset[i].slice(11, 16),
  };
}

/** Dry daylight windows (local time), optionally intersected with calendar gaps ({local:"HH:MM-HH:MM"}). */
export function outdoorWindows(fx, date, { minHours = 1, gaps, startHour = 8, endHour = 20 } = {}) {
  const i = dayIndex(fx, date);
  const sunrise = toMin(fx.daily.sunrise[i].slice(11, 16));
  const sunset = toMin(fx.daily.sunset[i].slice(11, 16));
  const dryHours = hoursOf(fx, date)
    .filter((x) => x.hour >= startHour && x.hour < endHour && !wet(x.precip, x.code))
    .filter((x) => x.hour * 60 >= sunrise && x.hour * 60 + 60 <= sunset)
    .map((x) => x.hour);
  let windows = ranges(dryHours);
  if (gaps) {
    const g = gaps.map((x) => x.local.split('-').map(toMin));
    windows = windows.flatMap(([s, e]) => g.map(([gs, ge]) => [Math.max(s, gs), Math.min(e, ge)]).filter(([a, b]) => b > a));
  }
  return windows.filter(([s, e]) => e - s >= minHours * 60).map(([s, e]) => ({ start: fmt(s), end: fmt(e) }));
}

/** GET JSON with a per-attempt timeout; retries network errors, 429 and 5xx, never other 4xx. */
export async function fetchJsonRetry(url, { fetchImpl = fetch, attempts = 3, delayMs = 1500, timeoutMs = 8000 } = {}) {
  let last;
  for (let i = 1; i <= attempts; i += 1) {
    try {
      const r = await fetchImpl(url, { signal: AbortSignal.timeout(timeoutMs) });
      if (r.ok) return await r.json();
      last = new Error(`open-meteo HTTP ${r.status}`);
      if (r.status < 500 && r.status !== 429) throw Object.assign(last, { final: true });
    } catch (e) {
      if (e.final) throw e;
      last = e;
    }
    if (i < attempts) await new Promise((res) => setTimeout(res, delayMs * i));
  }
  throw last;
}

// Last good forecast, kept so a short Open-Meteo outage does not blank the brief.
import fs from 'node:fs';
import path from 'node:path';
const cacheFile = (dir, k) => path.join(dir, `daybrief-${k.lat}_${k.lon}_${k.units}_${String(k.tz).replace(/[^A-Za-z0-9]/g, '-')}.json`);

export function saveForecast(dir, key, fx, nowMs = Date.now()) {
  fs.mkdirSync(dir, { recursive: true });
  const f = cacheFile(dir, key);
  fs.writeFileSync(`${f}.tmp`, JSON.stringify({ fetchedAt: new Date(nowMs).toISOString(), fx }));
  fs.renameSync(`${f}.tmp`, f);
}

/** { fx, fetchedAt } when a forecast for this place was saved within maxAgeHours, else null. */
export function loadForecast(dir, key, nowMs = Date.now(), maxAgeHours = 24) {
  try {
    const c = JSON.parse(fs.readFileSync(cacheFile(dir, key), 'utf8'));
    const age = nowMs - Date.parse(c.fetchedAt);
    return age >= 0 && age <= maxAgeHours * 3600000 && c.fx ? c : null;
  } catch {
    return null;
  }
}
