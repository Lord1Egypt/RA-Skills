#!/usr/bin/env node
// HelloFresh token helper for the hellofresh-fpx skill. Dependency-free.
//
//   node hf-token.mjs load  <dir>   <dir>/cookie.json (the `fpx cookies apiV2Auth` output)
//                                   → <dir>/auth.json + <dir>/auth.header
//   node hf-token.mjs store <dir>   <dir>/refreshed.json (the POST /gw/refresh response)
//                                   → <dir>/auth.json + <dir>/auth.header + <dir>/cookie.txt
//                                     (cookie.txt = the value to write back with
//                                     `fpx write-cookies apiV2Auth=@<dir>/cookie.txt`)
//
// auth.header is one line, `Authorization: Bearer <token>`, for `curl -H @file`,
// so the token never sits on a command line. Every file is mode 600. Nothing is
// printed to stdout and no token value is ever printed: status goes to stderr.
// Exit codes: 0 ok · 4 signed out / refresh refused · 64 usage.

import { chmodSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const SIGN_IN = 'Sign in at https://www.hellofresh.com in the browser running ContextMint Bridge, then run load again.';

// The cookie JSON's key order, as the web app writes it.
const KEY_ORDER = ['access_token', 'expires_in', 'refresh_token', 'token_type', 'user_data', 'refresh_expires_in', 'issued_at'];

function fail(code, message) {
  process.stderr.write(`hf-token: ${message}\n`);
  process.exit(code);
}

function writePrivate(path, text) {
  writeFileSync(path, text, { mode: 0o600 });
  chmodSync(path, 0o600);
}

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return undefined;
  }
}

const isTokenSet = (v) =>
  typeof v === 'object' && v !== null && typeof v.access_token === 'string' && v.access_token !== '' &&
  typeof v.refresh_token === 'string' && v.refresh_token !== '';

// js-cookie v3 read: decode %XX runs.
function decodeCookie(raw) {
  const unquoted = raw.startsWith('"') ? raw.slice(1, -1) : raw;
  return JSON.parse(unquoted.replace(/(%[\dA-F]{2})+/gi, decodeURIComponent));
}

// js-cookie v3 write: encodeURIComponent, then DE-code # $ & + / : < = > ? @ [ ] ^ ` { | }.
function encodeCookie(set) {
  const ordered = {};
  for (const k of KEY_ORDER) if (set[k] !== undefined) ordered[k] = set[k];
  for (const [k, v] of Object.entries(set)) if (!(k in ordered)) ordered[k] = v;
  return encodeURIComponent(JSON.stringify(ordered)).replace(/%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g, decodeURIComponent);
}

function save(dir, set) {
  writePrivate(join(dir, 'auth.json'), JSON.stringify(set));
  writePrivate(join(dir, 'auth.header'), `Authorization: Bearer ${set.access_token}\n`);
}

function reportExpiry(set) {
  const left = Math.round((set.issued_at + set.expires_in - Date.now() / 1000) / 60);
  process.stderr.write(
    left > 1
      ? `hf-token: access token valid for ${left} min\n`
      : 'hf-token: access token expired — reload the hellofresh.com tab and run load again, or refresh (references/requests.md)\n',
  );
}

const [cmd, dir] = process.argv.slice(2);
if (!dir || (cmd !== 'load' && cmd !== 'store')) fail(64, 'usage: hf-token.mjs load|store <dir>');

if (cmd === 'load') {
  const raw = readJson(join(dir, 'cookie.json'))?.apiV2Auth;
  let set;
  try {
    set = typeof raw === 'string' && raw !== '' ? decodeCookie(raw) : undefined;
  } catch {
    set = undefined;
  }
  if (!isTokenSet(set)) fail(4, `no HelloFresh session in the apiV2Auth cookie. ${SIGN_IN}`);
  save(dir, set);
  reportExpiry(set);
} else {
  const fresh = readJson(join(dir, 'refreshed.json'));
  if (!isTokenSet(fresh)) {
    const error = typeof fresh?.error === 'string' ? fresh.error : 'no token set in the response';
    fail(4, `refresh refused (${error}). ${SIGN_IN}`);
  }
  const old = readJson(join(dir, 'auth.json')) ?? {};
  const set = { ...fresh };
  if (set.user_data === undefined && old.user_data !== undefined) set.user_data = old.user_data;
  if (typeof set.issued_at !== 'number') set.issued_at = Math.floor(Date.now() / 1000);
  save(dir, set);
  writePrivate(join(dir, 'cookie.txt'), encodeCookie(set));
  reportExpiry(set);
}
