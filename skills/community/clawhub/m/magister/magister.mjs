#!/usr/bin/env node
/**
 * Magister CLI wrapper — reads credentials from environment variables:
 *   MAGISTER_HOST, MAGISTER_USER, MAGISTER_PASSWORD
 *
 * Usage: node magister.mjs <command> [args]
 *
 * Commands:
 *   students                        list students (works for both parent and child credentials)
 *   schedule <id> <from> <to>       schedule, dates YYYY-MM-DD
 *   grades <aanmelding_id> [top]    grades (default top=50)
 *   infractions <id> <from> <to>    absences/infractions
 */

import { fileURLToPath } from 'url';

// Normalize host: strip protocol and trailing slash so it is just the FQDN
const HOST = (process.env.MAGISTER_HOST || '').replace(/^https?:\/\//, '').replace(/\/$/, '');
const USER = process.env.MAGISTER_USER;
const PASS = process.env.MAGISTER_PASSWORD;

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  if (!HOST || !USER || !PASS) {
    console.error('Set MAGISTER_HOST, MAGISTER_USER, MAGISTER_PASSWORD before running.');
    process.exit(1);
  }
  if (!HOST.endsWith('.magister.net') && HOST !== 'magister.net') {
    console.error('MAGISTER_HOST must be a *.magister.net domain.');
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Token acquisition (OIDC implicit flow against accounts.magister.net)
// ---------------------------------------------------------------------------

export async function acquireToken(host, user, pass) {
  const rand = () =>
    Buffer.from(Array.from({ length: 16 }, () => Math.random() * 256 | 0)).toString('base64url');

  const jar = new Map();

  function saveCookies(r) {
    for (const sc of r.headers.getSetCookie()) {
      const [kv] = sc.split(';');
      const eq   = kv.indexOf('=');
      jar.set(kv.slice(0, eq).trim(), kv.slice(eq + 1).trim());
    }
  }
  const cookies = () => [...jar].map(([k, v]) => `${k}=${v}`).join('; ');

  async function follow(url, init = {}) {
    const r = await fetch(url, {
      ...init,
      redirect: 'manual',
      headers: { ...init.headers, Cookie: cookies() },
    });
    saveCookies(r);
    const loc = r.headers.get('location');
    if (!loc) return r;
    const next = new URL(loc, url);
    if (next.pathname.endsWith('redirect_callback.html')) return r;
    return follow(next.href);
  }

  const qs = new URLSearchParams({
    client_id:     `M6-${host}`,
    state:         rand(),
    redirect_uri:  `https://${host}/oidc/redirect_callback.html`,
    response_type: 'id_token token',
    acr_values:    `tenant:${host}`,
    nonce:         rand(),
    scope:         'openid profile attendance.overview calendar.user grades.read',
  });

  const login     = await follow(`https://accounts.magister.net/connect/authorize?${qs}`);
  const sessionId = login.url.match(/sessionId=([a-f0-9A-F-]+)/)[1];
  const returnUrl = decodeURIComponent(login.url.match(/returnUrl=([^&]+)/)[1]);
  const xsrf      = decodeURIComponent(jar.get('XSRF-TOKEN') ?? '');

  const challenge = async (path, body) => {
    const r = await fetch(`https://accounts.magister.net/challenges/${path}`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json', 'X-XSRF-TOKEN': xsrf, Cookie: cookies() },
      body:    JSON.stringify({ sessionId, returnUrl, ...body }),
    });
    saveCookies(r);
    return r.json();
  };

  await challenge('username', { username: user });
  const { redirectURL } = await challenge('password', { password: pass });

  const r     = await follow(`https://accounts.magister.net${redirectURL}`);
  const token = new URLSearchParams(new URL(r.headers.get('location')).hash.slice(1)).get('access_token');
  if (!token) throw new Error('Token not found in OIDC redirect');
  return token;
}

// ---------------------------------------------------------------------------
// Token getter (uses module-level HOST/USER/PASS by default)
// ---------------------------------------------------------------------------

export async function getToken(host = HOST, user = USER, pass = PASS) {
  return acquireToken(host, user, pass);
}

// ---------------------------------------------------------------------------
// Authenticated GET
// ---------------------------------------------------------------------------

export async function apiGet(path, host = HOST) {
  const token = await getToken();
  const url   = `https://${host}${path}`;
  const r     = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  if (!r.ok) throw new Error(`HTTP ${r.status} for ${url}`);
  return r.json();
}

// ---------------------------------------------------------------------------
// CLI (only when run directly)
// ---------------------------------------------------------------------------

const toLocal = iso => new Date(iso).toLocaleString('sv', {
  timeZone: 'Europe/Amsterdam',
  year: 'numeric', month: '2-digit', day: '2-digit',
  hour: '2-digit', minute: '2-digit',
}).replace(' ', 'T');

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [cmd, ...rest] = process.argv.slice(2);

  async function run() {
    switch (cmd) {
      case 'token': case 'account': case 'get': case 'children': {
        console.error('Commands: students | schedule <id> <from> <to> | grades <id> [top] | infractions <id> <from> <to>');
        process.exit(1);
      }
      case 'students': {
        const account = await apiGet('/api/account');
        const id      = account.Persoon?.Id;
        const role    = account.Groep?.[0]?.Naam;
        let students;
        if (role === 'Leerling') {
          const aanmeldingen = await apiGet(`/api/leerlingen/${id}/aanmeldingen`);
          students = aanmeldingen.items
            .filter(a => a.isHoofdAanmelding)
            .map(a => ({
              id,
              name:          `${account.Persoon.Roepnaam} ${account.Persoon.Achternaam}`.trim(),
              aanmelding_id: a.id,
            }));
        } else {
          const raw = await apiGet(`/api/ouders/${id}/kinderen`);
          students = raw.items.map(c => ({
            id:            c.id,
            name:          `${c.roepnaam} ${c.achternaam}`.trim(),
            aanmelding_id: +((c.actieveAanmeldingen?.[0]?.links?.self?.href ?? '').split('/').at(-1)),
          }));
        }
        console.log(JSON.stringify(students));
        break;
      }
      case 'schedule': {
        const [id, from, to] = rest;
        const raw = await apiGet(`/api/personen/${id}/afspraken?van=${from}&tot=${to}`);
        console.log(JSON.stringify(
          raw.Items
            .filter(i => i.Status !== 5)
            .map(i => ({
              start:   toLocal(i.Start),
              end:     toLocal(i.Einde),
              subject: i.Vakken?.[0]?.Naam ?? i.Omschrijving,
              teacher: i.Docenten?.[0]?.Naam ?? null,
              room:    i.Lokatie ?? null,
            }))
        ));
        break;
      }
      case 'grades': {
        const [id, top = '50'] = rest;
        const raw = await apiGet(`/api/aanmeldingen/${id}/cijfers?top=${top}`);
        console.log(JSON.stringify(raw.items.map(g => ({
          subject:     g.kolom.naam,
          description: g.kolom.omschrijving,
          grade:       g.waarde,
          weight:      g.kolom.weegfactor,
          passing:     g.isVoldoende,
          type:        g.kolom.type,
        }))));
        break;
      }
      case 'infractions': {
        const [id, from, to] = rest;
        const raw = await apiGet(`/api/personen/${id}/absenties?van=${from}&tot=${to}`);
        console.log(JSON.stringify(raw.Items.map(i => ({
          type:    i.Omschrijving,
          code:    i.Code,
          excused: i.Geoorloofd,
          lesson:  i.Afspraak?.Omschrijving ?? null,
        }))));
        break;
      }
      default:
        console.error('Commands: students | schedule <id> <from> <to> | grades <id> [top] | infractions <id> <from> <to>');
        process.exit(1);
    }
  }

  run().catch(e => { console.error(e.message); process.exit(1); });
}
