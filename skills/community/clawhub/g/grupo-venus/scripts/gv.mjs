#!/usr/bin/env node
// grupo-venus helper: people storage, geocoding (city and country sent to
// photon.komoot.io; time zone computed locally), and cached, throttled
// access to grupovenus.com. Node.js 18+, no packages.
//
// Every grupovenus.com request goes through fetchSite(), which takes a
// directory lock (parallel invocations queue instead of running at once),
// waits PAUSE_MS since the previous request, and caches responses for saved
// people. Nothing here adds people to the site's person list. A report made
// with a ticket is kept by the site under that ticket, like any made there.
import { chmodSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, utimesSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const SKILL = dirname(dirname(fileURLToPath(import.meta.url)));
const LEGACY = join(homedir(), '.openclaw', 'workspace', 'memory');
const HOME = process.env.GRUPO_VENUS_HOME
  ? resolve(process.env.GRUPO_VENUS_HOME.replace(/^~(?=$|\/)/, homedir()))
  : existsSync(join(LEGACY, 'grupo-venus.json')) ? LEGACY : join(homedir(), '.grupo-venus');
const PEOPLE = join(HOME, 'grupo-venus.json');
const EXPORTS = join(HOME, 'exports');
const CACHE = join(HOME, 'grupo-venus-cache');
const TICKET_FILE = join(HOME, 'ticket');
const BASE = 'https://grupovenus.com';
const PHOTON = 'https://photon.komoot.io/api/';
const UA = 'Mozilla/5.0 (grupo-venus skill)';
const PAUSE_MS = 2000;
const TICKET = 'necesita obtener un Ticket';
const TIC_RE = /^[A-Z0-9]{8,32}$/;
const FEC_RE = /^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$/;
/** Paid single-person reports, by INFORMEDESEADO id. */
const PAID = {
  62: 'Carta Natal', 170: 'Carta Natal con Quiron', 61: 'Carta SuperNatal', 69: 'Informe Indra',
  66: 'Informe Vocacional', 174: 'Vocacional simple', 63: 'Informe Infantil', 171: 'Informe Infantil coloquial',
  65: 'Astrologia Espiritual', 64: 'Astrologia Karmica', 67: 'Astrologia y Tarot', 50: 'Mi pronostico para hoy',
  13: 'Revolucion Solar', 173: 'Revolucion Solar coloquial', 15: 'Revolucion Lunar', 14: 'Progresiones',
  7: '2 anos Sat-Plu', 6: '1 ano Jup-Plu', 4: '3 meses Mar-Plu',
  945: 'Numerologia Basica (free)', 947: 'Numerologia Avanzada (free)',
};
/** Reports the site serves without a ticket or a credit. */
const NUMEROLOGY = new Set(['945', '947']);
/** Reports that depend on --start. The rest are the same on any day, so one cached copy serves for good. */
const DATED = new Set(['50', '13', '173', '15', '14', '7', '6', '4', '22', '23']);
/** Paid two-person reports: need --with KEY2 or --line2 LINE. */
const PAIR = {
  16: 'De Pareja', 172: 'De Pareja coloquial', 17: 'De Amistad', 90: 'Carta Compuesta',
  22: 'Pronostico de pareja 2 meses Sol-Plu', 23: 'Pronostico de pareja 12 meses Mar-Plu',
};
const latin1 = new TextDecoder('latin1');
const sleep = ms => new Promise(r => setTimeout(r, ms));
// The ticket is a credential: once loaded, every line printed has it masked, even text echoed from the site.
let SECRET = '';
const masked = t => `${t.slice(0, 3)}...${t.slice(-2)}`;
const scrub = s => SECRET ? s.split(SECRET).join(masked(SECRET)) : s;
const die = msg => { process.stderr.write(`${scrub(String(msg))}\n`); process.exit(1); };
const out = v => process.stdout.write(scrub(typeof v === 'string' ? `${v}\n` : `${JSON.stringify(v, null, 1)}\n`));

// ---------- storage ----------

const load = () => existsSync(PEOPLE) ? JSON.parse(readFileSync(PEOPLE, 'utf8')) : { people: {} };
// Birth data is personal: keep the folder and file readable by the owner only.
const save = db => { mkdirSync(HOME, { recursive: true, mode: 0o700 }); writeFileSync(PEOPLE, JSON.stringify(db, null, 2), { mode: 0o600 }); chmodSync(PEOPLE, 0o600); };
const KEY_RE = /^[a-z0-9][a-z0-9-]{0,63}$/;
const slug = name => name.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 64).replace(/-$/, '') || 'person';

function person(key) {
  const people = load().people;
  return people[key] || die(`unknown person '${key}'. Known: ${Object.keys(people).join(', ') || 'none'}`);
}

/** The semicolon person string grupovenus.com uses everywhere. */
const line = p => [p.name, p.birthdate, p.city, p.country, p.sex, '', p.tz_offset, p.lat_dms, p.lon_dms].join(';');

// ---------- coordinates ----------

function toDms(value, pos, neg) {
  let d = Math.trunc(Math.abs(value)), m = Math.round((Math.abs(value) - d) * 60);
  if (m === 60) { d += 1; m = 0; }
  return `${d}${value >= 0 ? pos : neg}${String(m).padStart(2, '0')}`;
}

function fromDms(s) {
  const m = /^(\d+)([NSEW])(\d+)$/.exec(String(s).trim().toUpperCase());
  if (!m) throw new Error(`bad coordinate ${s}`);
  const v = +m[1] + +m[3] / 60;
  return 'SE'.includes(m[2]) ? -v : v; // grupovenus: South negative, West positive
}

const round4 = v => Math.round(v * 1e4) / 1e4;
const record = (name, birthdate, city, country, sex, tz, lat, lon, style = null) => ({
  name, birthdate, city, country, sex, tz_offset: String(tz), lat_dms: lat, lon_dms: lon,
  lat_decimal: round4(fromDms(lat)), lon_decimal: round4(fromDms(lon)), style,
});

// ---------- time zone ----------

function zones() {
  const dm = (s, w) => { const v = +s.slice(1, 1 + w) + +s.slice(1 + w, 3 + w) / 60; return s[0] === '-' ? -v : v; };
  return readFileSync(join(SKILL, 'data', 'zone.tab'), 'utf8').split('\n')
    .filter(r => r && !r.startsWith('#'))
    .map(r => {
      const [cc, coord, tz] = r.split('\t');
      const i = Math.max(coord.lastIndexOf('+'), coord.lastIndexOf('-'));
      return { cc, lat: dm(coord.slice(0, i), 2), lon: dm(coord.slice(i), 3), tz };
    });
}

/** Nearest IANA zone within the country (east-positive lon). */
function zoneFor(lat, lon, cc) {
  const all = zones(), cands = all.filter(z => z.cc === cc.toUpperCase());
  const dist = z => (z.lat - lat) ** 2 + ((z.lon - lon) * Math.cos(lat * Math.PI / 180)) ** 2;
  return (cands.length ? cands : all).reduce((a, b) => dist(a) <= dist(b) ? a : b).tz;
}

function utcOffsetMinutes(zone, utcMs) {
  const name = new Intl.DateTimeFormat('en-US', { timeZone: zone, timeZoneName: 'longOffset' })
    .formatToParts(new Date(utcMs)).find(p => p.type === 'timeZoneName').value;
  const m = /GMT([+-])(\d\d):(\d\d)/.exec(name);
  return m ? (m[1] === '-' ? -1 : 1) * (+m[2] * 60 + +m[3]) : 0;
}

/** grupovenus sign convention: hours WEST of UTC (UTC-3 -> "3"), for a local wall time. */
function serverOffset(zone, y, mo, d, h, mi) {
  const wall = Date.UTC(y, mo - 1, d, h, mi);
  let off = utcOffsetMinutes(zone, wall);
  off = utcOffsetMinutes(zone, wall - off * 60000);
  return String(-off / 60);
}

// ---------- network ----------

/** application/x-www-form-urlencoded in ISO-8859-1, which the site expects. */
function formLatin1(params) {
  const enc = s => [...String(s)].map(ch => {
    const c = ch.codePointAt(0);
    if (/[A-Za-z0-9*\-._]/.test(ch)) return ch;
    if (ch === ' ') return '+';
    return c < 256 ? `%${c.toString(16).toUpperCase().padStart(2, '0')}` : '%3F';
  }).join('');
  return Object.entries(params).map(([k, v]) => `${enc(k)}=${enc(v)}`).join('&');
}

/** Redirects are followed by hand and never to another host. With a jar (Map), cookies are kept like a browser session. */
async function httpGet(url, body, extra = {}, jar = null, hops = 0) {
  const cookie = jar?.size ? { Cookie: [...jar].map(([k, v]) => `${k}=${v}`).join('; ') } : {};
  const res = await fetch(url, {
    method: body ? 'POST' : 'GET', body, redirect: 'manual',
    headers: { 'User-Agent': UA, ...(body ? { 'Content-Type': 'application/x-www-form-urlencoded' } : {}), ...extra, ...cookie },
  });
  if (jar) for (const c of res.headers.getSetCookie?.() ?? []) { const kv = c.split(';')[0], i = kv.indexOf('='); if (i > 0) jar.set(kv.slice(0, i).trim(), kv.slice(i + 1).trim()); }
  const to = res.status >= 300 && res.status < 400 && res.headers.get('location');
  if (to) {
    const next = new URL(to, url);
    // Thrown, not exited on, so the request lock is always released.
    if (hops > 3 || next.host !== new URL(url).host) throw new Error(`refusing a redirect ${hops > 3 ? 'loop' : 'to another host'} from ${new URL(url).host}`);
    return httpGet(next.href, undefined, extra, jar, hops + 1);
  }
  if (!res.ok) throw new Error(`HTTP ${res.status} from ${new URL(url).host}`);
  return Buffer.from(await res.arrayBuffer());
}

async function withLock(fn) {
  const lock = join(CACHE, '.lock');
  for (;;) {
    try { mkdirSync(lock); break; } catch (e) {
      if (e.code !== 'EEXIST') throw e;
      try { if (Date.now() - statSync(lock).mtimeMs > 120000) rmSync(lock, { recursive: true, force: true }); } catch {}
      await sleep(200);
    }
  }
  try { return await fn(); } finally { rmSync(lock, { recursive: true, force: true }); }
}

/** One grupovenus.com request: cached, serialized, paced. */
async function fetchSite(path, { params, post, cacheKey, headers, jar, keep = () => true }) {
  mkdirSync(CACHE, { recursive: true, mode: 0o700 });
  const file = cacheKey ? resolve(CACHE, cacheKey) : null;
  if (file && !file.startsWith(CACHE + sep)) die('refusing a cache path outside the cache folder');
  if (file && existsSync(file)) return readFileSync(file);
  return withLock(async () => {
    if (file && existsSync(file)) return readFileSync(file);
    const stamp = join(CACHE, '.last');
    const wait = PAUSE_MS - (Date.now() - (existsSync(stamp) ? statSync(stamp).mtimeMs : 0));
    if (wait > 0) await sleep(wait);
    let data;
    try {
      data = await httpGet(`${BASE}/${path}${params ? `?${formLatin1(params)}` : ''}`, post ? formLatin1(post) : undefined, headers, jar);
    } finally {
      writeFileSync(stamp, ''); const now = new Date(); utimesSync(stamp, now, now);
    }
    const text = latin1.decode(data);
    if (file && data.length > 1000 && !text.includes(TICKET) && !text.includes('caducad') && keep(text)) {
      mkdirSync(dirname(file), { recursive: true });
      writeFileSync(file, data, { mode: 0o600 });
    }
    return data;
  });
}

async function geocode(city, country) {
  const q = query => `${PHOTON}?${new URLSearchParams({ q: query, limit: '5', layer: 'city' })}`;
  let feats = JSON.parse(await httpGet(q(`${city}, ${country}`))).features;
  // Abbreviations like "USA" can confuse Photon; retry on the city alone.
  if (!feats.length) feats = JSON.parse(await httpGet(q(city))).features;
  if (!feats.length) die(`no city found for ${city}, ${country}`);
  const c = country.toLowerCase();
  const fits = f => (f.properties.country || '').toLowerCase().includes(c) || (f.properties.countrycode || '').toLowerCase() === c;
  return [...feats.filter(fits), ...feats.filter(f => !fits(f))];
}

// ---------- commands ----------

async function cmdAdd(o) {
  for (const k of ['name', 'date', 'time', 'city', 'country', 'sex']) if (!o[k]) die(`missing --${k}`);
  if (!['V', 'H'].includes(o.sex)) die('--sex must be V (male) or H (female)');
  const [y, mo, d] = o.date.split('-').map(Number), [h, mi] = o.time.split(':').map(Number);
  if (![y, mo, d, h, mi].every(Number.isFinite)) die('use --date YYYY-MM-DD and --time HH:MM');
  const feats = await geocode(o.city, o.country), pick = Number(o.pick || 0), f = feats[pick] || die(`no match ${pick}`);
  const [lon, lat] = f.geometry.coordinates, pr = f.properties;
  const zone = zoneFor(lat, lon, pr.countrycode || '');
  const h12 = h % 12 || 12, ampm = h < 12 ? 'AM' : 'PM';
  const birth = `${mo}/${d}/${y} ${h12}:${String(mi).padStart(2, '0')}:00 ${ampm}`;
  const p = record(o.name, birth, pr.name || o.city, o.country, o.sex, serverOffset(zone, y, mo, d, h, mi),
    toDms(lat, 'N', 'S'), toDms(-lon, 'W', 'E'), o.style || null);
  const key = o.key || slug(o.name);
  if (o.save) { const db = load(); db.people[key] = p; save(db); }
  const label = x => [x.properties.name, x.properties.state, x.properties.country].filter(Boolean).join(', ');
  out({
    saved: !!o.save, key: o.save ? key : null, sent_to: ['photon.komoot.io (city and country only)'], zone, picked: pick,
    matches: Object.fromEntries(feats.map((x, i) => [i, label(x)])), person: p, line: line(p),
    next: o.save ? `use KEY ${key}` : 'not saved: pass --line with the line above to chart/transits. Only a chart image is written for them, as a temporary file that the next helper run deletes once it is an hour old',
  });
}

const ENTITIES = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', deg: '°', laquo: '«', raquo: '»', iquest: '¿', iexcl: '¡', ordf: 'ª', ordm: 'º',
  ...Object.fromEntries(['aacute á', 'eacute é', 'iacute í', 'oacute ó', 'uacute ú', 'ntilde ñ', 'uuml ü']
    .flatMap(s => { const [n, c] = s.split(' '); return [[n, c], [n[0].toUpperCase() + n.slice(1), c.toUpperCase()]]; })),
};
const decodeEntities = s => s.replace(/&(#x[0-9a-f]+|#\d+|\w+);/gi, (m, e) => e[0] === '#'
  ? String.fromCodePoint(e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : +e.slice(1))
  : ENTITIES[e] ?? m);

function parseList(text) {
  const m = /<textarea[^>]*>([\s\S]*?)<\/textarea>/i.exec(text);
  return decodeEntities(m ? m[1] : text).split(/\r?\n/).map(r => r.split(';').map(x => x.trim()))
    .filter(p => p.length >= 9 && p[0])
    .map(([name, bdate, city, country, sex, , tz, lat, lon]) => record(name, bdate, city, country, sex, tz, lat, lon));
}

function cmdImport(file) {
  if (!file) die('usage: import FILE');
  const raw = readFileSync(resolve(file));
  let text = new TextDecoder('utf-8', { fatal: true });
  try { text = text.decode(raw); } catch { text = latin1.decode(raw); }
  const db = load(), imported = [];
  for (const p of parseList(text)) {
    const key = slug(p.name);
    p.style = db.people[key]?.style ?? null;
    db.people[key] = p; imported.push(key);
  }
  save(db); out({ imported });
}

function cmdExport(file) {
  const people = Object.values(load().people), n = people.length;
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const doc = `<html><head><title>Grupo Venus - Lista de personas</title>`
    + `<meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1"></head><body><center>`
    + `<form ACTION="${BASE}/perso2.asp" METHOD="POST"><input type="hidden" name="desti" value="modi">`
    + `<p>Lista de ${n} personas.</p><textarea NAME="lista" ROWS="15" COLS="84" WRAP=OFF>\r\n`
    + people.map(p => esc(line(p))).join('\r\n')
    + `\r\n</textarea><br><br>Al pulsar Modificar se reemplaza la Lista de personas guardada en este navegador. `
    + `<INPUT TYPE="submit" VALUE="Modificar" name="modif"></form></center></body></html>`;
  mkdirSync(EXPORTS, { recursive: true, mode: 0o700 });
  const target = file ? resolve(file) : join(EXPORTS, `Lista de ${n} Personas.html`);
  writeFileSync(target, Buffer.from([...doc].map(c => c.codePointAt(0) < 256 ? c.codePointAt(0) : 63)), { mode: 0o600 });
  out({ file: target, note: target.startsWith(EXPORTS + sep) ? 'inside the data folder; forget deletes it' : 'outside the data folder; forget does not delete it' });
}

/** Delete a person and every cached file made from their data.
 * A cache file is named PEOPLE~REST, PEOPLE being the key or KEY1+KEY2: "~" and "+" cannot occur in a key, so the match is exact. */
function cmdRemove(key, o) {
  if (!o.yes) die('remove deletes data: confirm with the user, then pass --yes');
  const db = load(); person(key); delete db.people[key]; save(db);
  let files = 0;
  // Files from before 0.3.4 have no "~" and no exact owner: they are matched by prefix, and old report copies
  // (tic-...) all go. That can only delete too much, never too little, and the site still has those reports.
  const owns = f => f.includes('~') ? f.split('~')[0].split('+').includes(key)
    : f.startsWith('tic-') || f.startsWith(`${key}-`) || f.startsWith(`${key}+`) || f.includes(`+${key}-`);
  for (const dir of ['chart', 'transits', 'reports']) {
    const d = join(CACHE, dir);
    if (!existsSync(d)) continue;
    for (const f of readdirSync(d)) if (owns(f)) { rmSync(join(d, f)); files++; }
  }
  out({ removed: key, cached_files_deleted: files });
}

/** Delete everything in the data folder: people, cache, exports and the ticket. An export written to a path the user chose is theirs to delete. */
function cmdForget(o) {
  if (!o.yes) die('forget deletes all people, the cache, exports and the ticket: confirm with the user, then pass --yes');
  for (const p of [PEOPLE, CACHE, EXPORTS, TICKET_FILE]) rmSync(p, { recursive: true, force: true });
  out({ deleted: [PEOPLE, CACHE, EXPORTS, TICKET_FILE] });
}

function cmdStyle(key, style) {
  if (!['casual', 'deep', 'practical'].includes(style)) die('style must be casual, deep or practical');
  const db = load(); person(key); db.people[key].style = style; save(db); out('ok');
}

/** A stored person by KEY, or an unsaved one from --line: no people file entry and no cache, only a short-lived chart image. */
function subject(key, o) {
  if (o.line) {
    const [p] = parseList(o.line);
    return { p: p || die('--line must be a full person line from add'), key: null };
  }
  return { p: person(key || die('give a KEY or --line')), key };
}

async function cmdChart(arg, o) {
  const { p, key } = subject(arg, o), cacheKey = key && `chart/${key}~${o.zodiac}-${o.lang}.png`;
  const data = await fetchSite('dibujo.aspx', {
    cacheKey, params: {
      fec: p.birthdate, aju: p.tz_offset, ciu: p.city, pais: p.country, lat: p.lat_decimal, lon: p.lon_decimal,
      nom: p.name, bot: 'atras', idioma: o.lang, CASASPRO: '', zodi: o.zodiac,
    },
  });
  if (!data.subarray(0, 4).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47]))) die('error: not a PNG');
  if (cacheKey) return out(join(CACHE, cacheKey));
  // An unsaved person's chart has to be a file to be shown: a temporary one, deleted by sweepTemp on the next run once it is an hour old.
  const tmp = join(CACHE, 'tmp', `chart-${Date.now()}.png`);
  mkdirSync(dirname(tmp), { recursive: true, mode: 0o700 });
  writeFileSync(tmp, data, { mode: 0o600 });
  out({ file: tmp, note: 'temporary file: delete it once shown. Any run of this helper deletes it after an hour, and forget deletes it too' });
}

/** Expiry for those temporary charts: every run deletes the ones older than an hour. */
function sweepTemp() {
  const dir = join(CACHE, 'tmp');
  if (!existsSync(dir)) return;
  for (const f of readdirSync(dir)) if (Date.now() - statSync(join(dir, f)).mtimeMs > 36e5) rmSync(join(dir, f), { force: true });
}

async function report(nombre, rid, start, o, cacheKey, tic = '', jar = null) {
  const now = new Date(), pad = n => String(n).padStart(2, '0');
  const data = await fetchSite('informes3.asp', {
    cacheKey, jar, post: {
      nombre, urldestino: 'informes3.asp', INFORMEDESEADO: rid,
      DIA1: start.getUTCDate(), MES1: start.getUTCMonth() + 1, ANO1: start.getUTCFullYear(),
      HORA1: pad(now.getHours()), MINU1: pad(now.getMinutes()), tipzod: o.zodiac, TIC: tic, idiomas: o.lang,
    },
  });
  const text = latin1.decode(data);
  if (text.includes(TICKET)) die(tic ? 'the server refused the ticket for this report (expired, used up or not valid for it)' : 'ticket required: this report or date is not in the free tier');
  return text;
}

function parseBars(doc) {
  const by = {};
  for (const [, title, h] of doc.matchAll(/<img class="barras"[^>]*title="([^"]*)"[^>]*height=(\d+)/g)) {
    const m = /^(r )?(\w+) (\d+)\/(\d+)\/(\d+) [\d:]+ orbe: (\d+)\D+(\d+)/.exec(decodeEntities(title));
    if (!m) continue;
    const code = m[2].toUpperCase();
    (by[code] ||= []).push({ retro: !!m[1], date: new Date(Date.UTC(+m[5], +m[4] - 1, +m[3])), orb: `${m[6]}°${m[7]}'`, height: +h });
  }
  const iso = d => d.toISOString().slice(0, 10);
  return Object.entries(by).map(([code, ps]) => {
    ps.sort((a, b) => a.date - b.date);
    const peak = ps.reduce((a, b) => b.height > a.height ? b : a);
    const wins = [[ps[0]]];
    for (const p of ps.slice(1)) {
      const cur = wins.at(-1);
      if ((p.date - cur.at(-1).date) / 864e5 <= 4) cur.push(p); else wins.push([p]);
    }
    return {
      code, peak_height: peak.height, peak_date: iso(peak.date), peak_orb: peak.orb, intensity: Math.round(peak.height / 55 * 100) / 100,
      windows: wins.map(w => ({ from: iso(w[0].date), to: iso(w.at(-1).date), retro: w.some(p => p.retro) })),
    };
  }).sort((a, b) => b.peak_height - a.peak_height);
}

const todayUTC = () => { const n = new Date(); return new Date(Date.UTC(n.getFullYear(), n.getMonth(), n.getDate())); };

/** Reuse a 1-year report from the last 14 days instead of requesting a new one. */
function cachedStart(key, rid, today) {
  if (rid !== '8') return today;
  for (let back = 0; back < 15; back++) {
    const s = new Date(today - back * 864e5);
    if (existsSync(join(CACHE, 'transits', `${key}~${rid}-${s.toISOString().slice(0, 10)}.html`))) return s;
  }
  return today;
}

async function cmdTransits(arg, o) {
  const { p, key } = subject(arg, o);
  const start = o.start ? new Date(`${o.start}T00:00:00Z`) : key ? cachedStart(key, o.report, todayUTC()) : todayUTC();
  const day = start.toISOString().slice(0, 10);
  const doc = await report(line(p), o.report, start, o, key && `transits/${key}~${o.report}-${day}.html`);
  out({ report: o.report, start: day, transits: parseBars(doc).slice(0, Number(o.top || 40)) });
}

function textOf(doc) {
  const parts = [...doc.matchAll(/<p class="interp">([\s\S]*?)(?:<\/p>|<\/font>)/gi)].map(m => m[1]);
  let t = (parts.length ? parts.join('\n') : doc).replace(/<(script|style)[\s\S]*?<\/\1>/gi, '');
  t = decodeEntities(t.replace(/<br\s*\/?>|<\/p>/gi, '\n').replace(/<[^>]+>/g, ''));
  return t.replace(/[ \t]+/g, ' ').replace(/\n\s*\n+/g, '\n\n').replace(/([^\n])\n(?!\n)/g, '$1 ').replace(/ +/g, ' ').trim();
}

async function cmdInterp(code, o) {
  if (!code) die('usage: interp CODE [--style transiaw|tratsp|starsolues]');
  if (!['transiaw', 'tratsp', 'starsolues'].includes(o.style)) die('style must be transiaw, tratsp or starsolues');
  const cla = code.toUpperCase();
  const data = await fetchSite('sacainter.asp', {
    params: { tabla: o.style, cla, orb: o.style === 'tratsp' ? '0' : '99' }, cacheKey: `interp/${o.style}-${cla}.html`,
  });
  out(textOf(latin1.decode(data)));
}

// ---------- ticket (paid reports) ----------

/** The ticket is a credential: kept owner-only, never printed, never part of a cache file name. */
function ticket(required = true) {
  const t = (process.env.GRUPO_VENUS_TICKET || (existsSync(TICKET_FILE) ? readFileSync(TICKET_FILE, 'utf8') : '')).trim().toUpperCase();
  if (t && !TIC_RE.test(t)) die('the stored ticket looks malformed; set it again with: ticket set CODE');
  SECRET = t;
  return t || (required ? die('no ticket: ask the user for their grupovenus.com ticket code, then run: ticket set CODE') : '');
}
const PLACEHOLDER = 'X;1/1/2000 12:00:00 PM;X;X;V;;0;0N00;0W00';

async function cmdTicket(action, code, o = {}) {
  if (action === 'set') {
    const t = String(code || '').trim().toUpperCase();
    SECRET = t;
    if (!TIC_RE.test(t)) die('usage: ticket set CODE (letters and digits, as in info.asp?tic=CODE)');
    mkdirSync(HOME, { recursive: true, mode: 0o700 });
    writeFileSync(TICKET_FILE, t, { mode: 0o600 }); chmodSync(TICKET_FILE, 0o600);
    return out({ ticket: masked(t), stored: TICKET_FILE });
  }
  if (action === 'clear') { rmSync(TICKET_FILE, { force: true }); return out({ ticket: null }); }
  if (action) die('usage: ticket [set CODE | clear]');
  const t = ticket(false);
  const local = { ticket: t ? masked(t) : null, source: process.env.GRUPO_VENUS_TICKET ? 'GRUPO_VENUS_TICKET' : t ? TICKET_FILE : null };
  if (!t || o.offline) return out(local);
  out({ ...local, ...await ticketStatus(t) });
}

/** Live counters (2 requests, never cached). info.asp hides them while the browser's
 * person list is empty, so it gets a placeholder person, never a real one. */
async function ticketStatus(t) {
  const info = latin1.decode(await fetchSite('info.asp', { params: { tic: t }, headers: { Cookie: `d0=${formLatin1({ x: PLACEHOLDER }).slice(2)}` } }));
  const list = latin1.decode(await fetchSite('ticinfo.asp', { params: { tic: t } }));
  const num = (re, doc) => { const m = re.exec(doc); return m ? +m[1] : null; };
  const left = num(/Informes&nbsp;disponibles&nbsp;<b>(\d+)/i, info), exp = /caducidad del ticket\s*:\s*([\d-]+)/i.exec(list);
  if (left === null && !exp) die('the server did not recognize this ticket');
  const days = exp ? Math.ceil((Date.parse(`${exp[1]}T00:00:00Z`) - todayUTC()) / 864e5) : null;
  return {
    credits_left: left, reports_created: num(/Informes&nbsp;creados&nbsp;(\d+)/i, info),
    expires: exp ? exp[1] : null, days_left: days, valid: left !== null && left > 0 && (days === null || days >= 0),
  };
}

/** Paid report HTML to markdown: chapters (h3), factor or transit headings, paragraphs. */
function reportText(doc) {
  const clean = s => decodeEntities(s.replace(/\r/g, '').replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, ''))
    .replace(/[ \t\u00a0]+/g, ' ').replace(/ *\n */g, '\n').replace(/\n{2,}/g, '\n\n').replace(/([^\n])\n(?!\n)/g, '$1 ').replace(/ {2,}/g, ' ').trim();
  const one = s => clean(s).replace(/\s+/g, ' ');
  const re = new RegExp([
    /<H3>([\s\S]*?)<\/H3>/,                                                                           // chapter
    /<font size=\+1[^>]*color="1212BF">([\s\S]*?)<\/FONT>/,                                            // natal factor
    /<A NAME="([A-Z]{6,12})">(?:<\/A>)?\s*<center>([\s\S]{0,900}?)<font size=\+\d color="(?:green|355430)">([\s\S]*?)<\/font>/, // transit
    /<p class="interp">([\s\S]*?)<\/p>/,                                                               // text
  ].map(r => r.source).join('|'), 'gi');
  const parts = [];
  for (const [, h, f, code, when, tr, p] of doc.matchAll(re)) {
    if (h) parts.push(`## ${one(h)}`);
    else if (f && !/<table/i.test(f) && !/^[\d/ ]*$/.test(one(f))) parts.push(`### ${one(f)}`); // date grid cells are not headings
    else if (tr) {
      const w = one(when || ''), range = /\((\d+\/\d+\/\d{4})\s*hasta\s*(\d+\/\d+\/\d{4})\)/.exec(w), date = /\d+\/\d+\/\d{4}/.exec(w);
      const dates = range ? `, ${range[1]} to ${range[2]}` : date ? `, ${date[0]}` : '';
      parts.push(`### ${one(tr)} (${code.toUpperCase()})${dates}`);
    }
    else if (p && clean(p)) parts.push(clean(p));
  }
  return parts.length ? parts.join('\n\n') : textOf(doc);
}

/** Reports made with the ticket in the last 180 days (the server deletes older ones). */
async function cmdReports() {
  const doc = latin1.decode(await fetchSite('ticinfo.asp', { params: { tic: ticket() } }));
  const reports = [...doc.matchAll(/title="([^"]*)">([^<]*)<\/a><\/b>[\s\S]*?informes11\.asp\?tic=[^&]+&fec=([^"]+)"[^>]*>([^<]+)</gi)]
    .map(([, info, name, fec, type]) => ({ id: fec, person: decodeEntities(name).trim(), type: decodeEntities(type).trim(), birth: decodeEntities(info).replace(/\s+/g, ' ').trim() }));
  const exp = /caducidad del ticket\s*:\s*([\d-]+)/i.exec(doc);
  out({ ticket_expires: exp ? exp[1] : null, reports, next: 'read ID costs no credit (add --for KEY to keep a local copy for a saved person); make costs one' });
}

/** An existing report: no credit used. A local copy is kept only when the caller names the saved person it belongs to. */
async function readReport(id, owner = null) {
  if (!FEC_RE.test(id || '')) die('usage: read ID (an id from reports, like "2026-11-5 21:1:39")');
  return latin1.decode(await fetchSite('informes11.asp', { params: { tic: ticket(), fec: id }, cacheKey: owner && `reports/${owner}~tic-${id.replace(/\D+/g, '-')}.html`, keep: isReport }));
}
const cmdRead = async (id, o) => { if (o.for) person(o.for); out(reportText(await readReport(id, o.for))); };

/** Hidden inputs of the first form in html, as a browser would send them. */
function hiddenFields(html) {
  const form = html.slice(0, html.search(/<\/form>/i) + 1 || undefined), fields = {};
  for (const [tag] of form.matchAll(/<input\b[^>]*type="?hidden[^>]*>/gis)) {
    const n = /name="?([^" >]+)/i.exec(tag), v = /value="([^"]*)"/i.exec(tag);
    if (n) fields[n[1]] = decodeEntities(v ? v[1] : '');
  }
  return fields;
}

const isReport = doc => /class="(interp|barras)"/i.test(doc);

/** Fill the site's "place at the return" form: its hidden fields, plus date, country and city. */
function placeForm(doc, start, where) {
  const form = doc.slice(doc.search(/<form[^>]*ciuda\.asp/i));
  const fields = hiddenFields(form);
  let date = start;
  // Lunar returns: the form lists the year's return dates; take the first on or after the start.
  const revs = [...form.matchAll(/<option[^>]*value="(\d{4}-\d{2}-\d{2})/gi)].map(m => m[1]);
  if (revs.length) {
    const iso = start.toISOString().slice(0, 10), pick = revs.find(d => d >= iso) || revs.at(-1);
    fields.rev13 = pick; date = new Date(`${pick}T00:00:00Z`);
  }
  // Send what a browser would: the hidden fields as they are, plus the date selects this form has.
  const has = new Set([...form.matchAll(/<select\b[^>]*name="?([^" >]+)/gi)].map(m => m[1]));
  const d = { DIA1: date.getUTCDate(), MES1: date.getUTCMonth() + 1, ANO1: date.getUTCFullYear() };
  for (const [k, v] of Object.entries(d)) if (has.has(k)) fields[k] = v;
  return { ...fields, '14PAIS': where.country, '08CIUDAD': where.city, boton1: 'Calcular' };
}

/** Create a paid report: uses one ticket credit, so only after the user confirms. */
async function cmdMake(arg, o) {
  const free = NUMEROLOGY.has(o.report), tic = free ? '' : ticket(), name = PAID[o.report] || PAIR[o.report];
  const { p: p0, key: key1 } = subject(arg, o);
  if ((o.fullname || o.signature) && !NUMEROLOGY.has(o.report)) die('--fullname and --signature are for numerology (945, 947)');
  // Numerology reads the full birth name. It and the signature go into that one request only:
  // a report made with either is never written to disk, because its text repeats them.
  const p = o.fullname ? { ...p0, name: o.fullname } : p0, unsaved = o.fullname || o.signature;
  const pair = o.report in PAIR;
  if (pair && !o.with && !o.line2) die(`'${name}' needs a second person: --with KEY2 or --line2 LINE`);
  const q = pair ? subject(o.with, { line: o.line2 }) : null;
  if (!pair && (o.with || o.line2)) die(`'${name}' is for one person; drop --with/--line2`);
  if (!o.yes && !free) die(`make uses one ticket credit for '${name}': check reports first, confirm with the user, then pass --yes`);
  const key = pair ? key1 && q.key && `${key1}+${q.key}` : key1;
  const start = o.start ? new Date(`${o.start}T00:00:00Z`) : todayUTC(), day = start.toISOString().slice(0, 10);
  const where = { city: o.city || p.city, country: o.country || p.country };
  const cacheKey = key && !unsaved && `reports/${key}~${o.report}-${o.lang}-${o.zodiac}-${DATED.has(o.report) ? day : 'x'}${o.city || o.country ? `-${slug(`${where.city}-${where.country}`)}` : ''}.html`;
  const file = cacheKey && join(CACHE, cacheKey);
  let doc = file && existsSync(file) ? latin1.decode(readFileSync(file)) : null, existing = false;
  const cached = !!doc;
  if (!doc) {
    const jar = new Map();
    // Two-person reports pick the second person from the browser's person list (cookies d0, d1, ...).
    if (pair) [p, q.p].forEach((x, i) => jar.set(`d${i}`, formLatin1({ x: line(x) }).slice(2)));
    doc = await report(line(p), o.report, start, o, null, tic, jar);
    const picker = pair && /<form ACTION="([\w.]+)"[^>]*>\s*<select name="nombre"/i.exec(doc);
    if (picker) doc = latin1.decode(await fetchSite(picker[1], { jar, post: { ...hiddenFields(doc.slice(picker.index)), nombre: line(q.p) } }));
    // Returns and progressions answer with a second form: where the person is at that date.
    // Advanced numerology asks whether to also analyze the signature (optional).
    const sign = doc.search(/ACTION="numerologia2\.asp"/i);
    if (sign >= 0) doc = latin1.decode(await fetchSite('numerologia2.asp', { jar, post: { ...hiddenFields(doc.slice(sign)), firma: o.signature || '', boton1: 'Continuar' } }));
    if (/ACTION="ciuda\.asp"/i.test(doc)) doc = latin1.decode(await fetchSite('ciuda.asp', { jar, post: placeForm(doc, start, where) }));
    // Same person, report and date as an earlier one: the site charges nothing and links to it.
    const dup = /YA EXISTE/.test(doc) && /informes11\.asp\?tic=[^&"]+&fec=([^"]+)"/i.exec(doc);
    if (dup) { doc = await readReport(decodeEntities(dup[1])); existing = true; }
    if (!isReport(doc)) die(`the site did not return a report: ${textOf(doc).slice(0, 300)}`);
    if (file) { mkdirSync(dirname(file), { recursive: true }); writeFileSync(file, doc, { encoding: 'latin1', mode: 0o600 }); }
  }
  const left = /tiene ahora (\d+) informes disponibles/i.exec(doc);
  const bars = parseBars(doc);
  out({
    report: name, start: day,
    ...(existing ? { existing: 'already made earlier; no credit used' } : {}),
    ...(cached ? { cached: 'local copy; no request, no credit used' } : free ? {} : { credits_left: left ? +left[1] : null }),
    ...(bars.length ? { transits: bars.slice(0, Number(o.top || 40)) } : {}),
    text: reportText(doc),
  });
}

const HELP = `Usage: node gv.mjs COMMAND [options]

  add --name N --date YYYY-MM-DD --time HH:MM --city C --country K --sex V|H
      [--save] [--style casual|deep|practical] [--key KEY] [--pick N]
                          build a person line; city and country go to photon.komoot.io
                          (no grupovenus request). Written to disk only with --save.
  import FILE             import a grupovenus "Lista de personas" file
  export [FILE]           write a "Lista de personas" file (default: data folder/exports)
  list                    show stored people
  remove KEY --yes        delete a person and their cached charts, forecasts and reports
  forget --yes            delete all people, the cache, the ticket and the exports in the data folder
  style KEY STYLE         save a reading style
  chart KEY|--line L      natal chart PNG path        [--lang E|I|F] [--zodiac T|S1..S5]
  transits KEY|--line L   parsed forecast graph       [--report=8|-1|0|1] [--start YYYY-MM-DD] [--top N]
                          --line uses an unsaved person: no cache; a chart is a temporary file, deleted by the next run after an hour
  interp CODE             interpretation text         [--style transiaw|tratsp|starsolues]

  Paid reports (need a grupovenus.com ticket):
  ticket [--offline]      ticket status: credits left, reports created, expiry (2 requests;
                          --offline only says whether one is stored)
  ticket set CODE|clear   store (owner-only) or remove the ticket
  reports                 reports made with the ticket (last 180 days): id, person, type
  read ID [--for KEY]     full text of one of those reports; no credit used. With --for, a local
                          copy is kept under that saved person (remove KEY deletes it)
  make KEY|--line L --report=ID --yes
                          create a paid report; uses one credit   [--start YYYY-MM-DD] [--lang] [--zodiac]
                          returns and progressions: [--city C --country K] where the person is then
                          (default: birth place). A repeat of an earlier report is free.
                          ids: ${Object.entries(PAID).map(([k, v]) => `${k} ${v}`).join(', ')}
  make KEY --report=945 [--fullname 'FULL BIRTH NAME']           free numerology, no ticket needed
  make KEY --report=947 [--fullname F] [--signature S]       free advanced numerology
  make KEY --with KEY2 --report=ID --yes   (or --line/--line2) two-person report
                          ids: ${Object.entries(PAIR).map(([k, v]) => `${k} ${v}`).join(', ')}

Data folder: ${HOME} (set GRUPO_VENUS_HOME to change it)`;

async function main() {
  const { values: o, positionals: [cmd, ...args] } = parseArgs({
    allowPositionals: true, options: {
      name: { type: 'string' }, date: { type: 'string' }, time: { type: 'string' }, city: { type: 'string' },
      country: { type: 'string' }, sex: { type: 'string' }, style: { type: 'string' }, key: { type: 'string' },
      pick: { type: 'string' }, lang: { type: 'string', default: 'E' }, zodiac: { type: 'string', default: 'T' },
      report: { type: 'string' }, start: { type: 'string' }, top: { type: 'string' },
      line: { type: 'string' }, save: { type: 'boolean' }, yes: { type: 'boolean' }, offline: { type: 'boolean' }, with: { type: 'string' }, line2: { type: 'string' }, for: { type: 'string' },
      fullname: { type: 'string' }, signature: { type: 'string' },
      help: { type: 'boolean', short: 'h' },
    },
  });
  if (o.help || !cmd) return out(HELP);
  sweepTemp();
  // Every option that reaches a request or a file name is checked against a closed set.
  const check = (ok, msg) => ok || die(msg);
  check(['E', 'I', 'F'].includes(o.lang), '--lang must be E, I or F');
  check(/^(T|S[1-5])$/.test(o.zodiac), '--zodiac must be T or S1..S5');
  if (cmd === 'make') check(o.report in PAID || o.report in PAIR, `--report must be one of ${[...Object.keys(PAID), ...Object.keys(PAIR)].join(', ')}`);
  else { o.report ??= '8'; check(['8', '-1', '0', '1'].includes(o.report), '--report must be 8, -1, 0 or 1 (paid ones go through make)'); }
  for (const k of ['with', 'for']) check(!o[k] || KEY_RE.test(o[k]), `bad KEY ${o[k]}`);
  for (const k of ['fullname', 'signature']) check(!o[k] || /^[^;\r\n]{1,85}$/.test(o[k]), `--${k} must be 1 to 85 characters, no semicolons`);
  check(!o.start || /^\d{4}-\d{2}-\d{2}$/.test(o.start), '--start must be YYYY-MM-DD');
  check(!o.top || /^\d{1,3}$/.test(o.top), '--top must be a number');
  check(!o.pick || /^\d$/.test(o.pick), '--pick must be 0-9');
  check(!o.key || KEY_RE.test(o.key), '--key must be lowercase letters, digits and hyphens');
  if (['chart', 'transits', 'remove', 'style', 'make'].includes(cmd) && args[0]) check(KEY_RE.test(args[0]), `bad KEY ${args[0]}`);
  if (cmd === 'interp' && args[0]) check(/^[A-Za-z]{5,12}$/.test(args[0]), 'CODE looks like SATCUAASC');
  switch (cmd) {
    case 'add': return cmdAdd(o);
    case 'import': return cmdImport(args[0]);
    case 'export': return cmdExport(args[0]);
    case 'list': return out(load().people);
    case 'remove': return cmdRemove(args[0] || die('usage: remove KEY --yes'), o);
    case 'forget': return cmdForget(o);
    case 'style': return cmdStyle(args[0], args[1]);
    case 'chart': return cmdChart(args[0], o);
    case 'transits': return cmdTransits(args[0], o);
    case 'ticket': return cmdTicket(args[0], args[1], o);
    case 'reports': return cmdReports();
    case 'read': return cmdRead(args[0], o);
    case 'make': return cmdMake(args[0], o);
    case 'interp': return cmdInterp(args[0], { ...o, style: o.style || 'transiaw' });
    default: die(`unknown command ${cmd}\n\n${HELP}`);
  }
}

main().catch(e => die(e.message));
