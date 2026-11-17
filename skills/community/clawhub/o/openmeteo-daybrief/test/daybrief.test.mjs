import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { summarizeDay, outdoorWindows, describeCode } from '../scripts/lib.mjs';

const fx = JSON.parse(fs.readFileSync(new URL('./forecast.json', import.meta.url)));

test('describeCode maps WMO codes', () => {
  assert.equal(describeCode(0), 'clear');
  assert.equal(describeCode(63), 'moderate rain');
  assert.equal(describeCode(999), 'unknown');
});

test('summarizeDay reports high/low/rain for the requested date', () => {
  const s = summarizeDay(fx, '2026-11-16');
  assert.equal(s.date, '2026-11-16');
  assert.equal(s.high, 19.5);
  assert.equal(s.low, 12);
  assert.equal(s.precipChanceMax, 80);
  assert.equal(s.condition, 'moderate rain');
  assert.equal(s.rainHours, '14:00-16:59');
  assert.equal(s.sunset, '16:49');
});

test('outdoorWindows avoids rain and darkness', () => {
  const w = outdoorWindows(fx, '2026-11-16', { minHours: 1 });
  assert.deepEqual(w, [{ start: '08:00', end: '14:00' }]); // sunset 16:49 cuts the post-rain hour
});

test('outdoorWindows intersects with calendar gaps', () => {
  const gaps = [{ local: '08:00-09:00' }, { local: '12:00-20:00' }];
  assert.deepEqual(outdoorWindows(fx, '2026-11-16', { minHours: 1, gaps }), [
    { start: '08:00', end: '09:00' },
    { start: '12:00', end: '14:00' },
  ]);
});

test('unknown date is an error', () => {
  assert.throws(() => summarizeDay(fx, '2030-01-01'), /not in forecast/);
});

test('fetchJsonRetry retries transient failures and returns the first good body', async () => {
  const { fetchJsonRetry } = await import('../scripts/lib.mjs');
  let n = 0;
  const flaky = async () => {
    n += 1;
    if (n === 1) throw new Error('fetch failed');
    if (n === 2) return { ok: false, status: 503 };
    return { ok: true, json: async () => ({ fine: true }) };
  };
  assert.deepEqual(await fetchJsonRetry('http://x', { fetchImpl: flaky, attempts: 3, delayMs: 1 }), { fine: true });
  assert.equal(n, 3);
});

test('fetchJsonRetry gives up after the attempts and does not retry a 4xx', async () => {
  const { fetchJsonRetry } = await import('../scripts/lib.mjs');
  let n = 0;
  const down = async () => { n += 1; throw new Error('fetch failed'); };
  await assert.rejects(fetchJsonRetry('http://x', { fetchImpl: down, attempts: 3, delayMs: 1 }), /fetch failed/);
  assert.equal(n, 3);
  let m = 0;
  const bad = async () => { m += 1; return { ok: false, status: 400 }; };
  await assert.rejects(fetchJsonRetry('http://x', { fetchImpl: bad, attempts: 3, delayMs: 1 }), /HTTP 400/);
  assert.equal(m, 1);
});

test('forecast cache: a saved forecast is reused for the same place while fresh, and only then', async () => {
  const { saveForecast, loadForecast } = await import('../scripts/lib.mjs');
  const os = await import('node:os');
  const path = await import('node:path');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'daybrief-'));
  const key = { lat: 34.02, lon: -118.29, tz: 'America/Los_Angeles', units: 'fahrenheit' };
  const t0 = Date.parse('2026-11-16T08:00:00Z');
  assert.equal(loadForecast(dir, key, t0), null);
  saveForecast(dir, key, fx, t0);
  const hit = loadForecast(dir, key, t0 + 6 * 3600000);
  assert.deepEqual(hit.fx, fx);
  assert.equal(hit.fetchedAt, '2026-11-16T08:00:00.000Z');
  assert.equal(loadForecast(dir, key, t0 + 25 * 3600000), null); // too old
  assert.equal(loadForecast(dir, { ...key, lat: 40 }, t0), null); // other place
  assert.equal(loadForecast(dir, { ...key, units: 'celsius' }, t0), null);
  fs.rmSync(dir, { recursive: true, force: true });
});

test('daybrief script: unreachable API falls back to the cached forecast, or errors without one', async () => {
  const { saveForecast } = await import('../scripts/lib.mjs');
  const os = await import('node:os');
  const path = await import('node:path');
  const { spawnSync } = await import('node:child_process');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'daybrief-'));
  const script = new URL('../scripts/daybrief', import.meta.url).pathname;
  const run = () => {
    const r = spawnSync(process.execPath, [script, '--lat', '34.02', '--lon', '-118.29', '--tz', 'America/Los_Angeles', '--date', '2026-11-16', '--units', 'celsius'], {
      env: { ...process.env, DAYBRIEF_CACHE_DIR: dir, DAYBRIEF_API_URL: 'http://127.0.0.1:9/v1/forecast', DAYBRIEF_RETRY_DELAY_MS: '1' },
      encoding: 'utf8',
    });
    return { code: r.status, json: JSON.parse(r.stdout) };
  };
  const miss = run();
  assert.equal(miss.code, 1);
  assert.match(miss.json.error, /weather unavailable/);
  saveForecast(dir, { lat: 34.02, lon: -118.29, tz: 'America/Los_Angeles', units: 'celsius' }, fx);
  const hit = run();
  assert.equal(hit.code, 0);
  assert.equal(hit.json.cached, true);
  assert.equal(hit.json.condition, 'moderate rain');
  fs.rmSync(dir, { recursive: true, force: true });
});
