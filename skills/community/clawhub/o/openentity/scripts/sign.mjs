#!/usr/bin/env node
// Open Entity signer for the HTTP door. Node 22+, WebCrypto only, no dependencies.
// Usage:
//   node sign.mjs adopt <name> <declaration-sha256> <v1-spec-json>   -> writes ~/.openentity/<eid>/{key,entity.json,adopt.json}, prints "<eid> <stamp>"
//   node sign.mjs record <eid> <kind> <payload-json> <v1-spec-json>  -> writes ~/.openentity/<eid>/record-batch.json, prints "<stamp>"
//   node sign.mjs committed <eid>                                  -> marks the pending record batch as accepted
//   node sign.mjs anchor <eid>                                     -> prints the Identity Anchor (spec 5.6)
import { mkdir, readFile, writeFile, rename } from 'node:fs/promises';
import { homedir } from 'node:os';
import { join } from 'node:path';

const REGISTRY = process.env.OPENENTITY_REGISTRY || 'https://openentity.org';
const HOME = process.env.OPENENTITY_HOME || join(homedir(), '.openentity');
const enc = new TextEncoder();
const subtle = globalThis.crypto.subtle;

// RFC 8785 (JCS): sorted keys, ECMAScript serialization of primitives.
export function canonicalize(v) {
  if (v === null || typeof v !== 'object') return JSON.stringify(v);
  if (Array.isArray(v)) return `[${v.map(canonicalize).join(',')}]`;
  const keys = Object.keys(v).filter((k) => v[k] !== undefined).sort();
  return `{${keys.map((k) => `${JSON.stringify(k)}:${canonicalize(v[k])}`).join(',')}}`;
}

const ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
export function base58(bytes) {
  let n = 0n;
  for (const b of bytes) n = n * 256n + BigInt(b);
  let out = '';
  while (n > 0n) { out = ALPHABET[Number(n % 58n)] + out; n /= 58n; }
  for (const b of bytes) { if (b !== 0) break; out = '1' + out; }
  return out;
}

export const sha256 = async (data) => new Uint8Array(await subtle.digest('SHA-256', typeof data === 'string' ? enc.encode(data) : data));
const hex = (b) => Array.from(b, (x) => x.toString(16).padStart(2, '0')).join('');
const now = () => new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
const nonce = () => base58(crypto.getRandomValues(new Uint8Array(16)));
const b64url = (s) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), (c) => c.charCodeAt(0));

export function didKey(publicKey) {
  return `did:key:z${base58(new Uint8Array([0xed, 0x01, ...publicKey]))}`;
}

async function loadKey(eid) {
  const jwk = JSON.parse(await readFile(join(HOME, eid, 'key'), 'utf8'));
  return { jwk, privateKey: await subtle.importKey('jwk', jwk, { name: 'Ed25519' }, false, ['sign']) };
}

// eddsa-jcs-2022 (spec 4.1): sign sha256(JCS(proof config)) || sha256(JCS(object minus proof)).
export async function sign(obj, eid, privateKey, created = now()) {
  const { proof: _drop, ...body } = obj;
  const vm = `${eid}#${eid.slice('did:key:'.length)}`;
  const config = { type: 'DataIntegrityProof', cryptosuite: 'eddsa-jcs-2022', created, verificationMethod: vm, proofPurpose: 'assertionMethod' };
  const data = new Uint8Array([...(await sha256(canonicalize(config))), ...(await sha256(canonicalize(body)))]);
  const sig = new Uint8Array(await subtle.sign('Ed25519', privateKey, data));
  return { ...body, proof: { ...config, proofValue: `z${base58(sig)}` } };
}

// Required stamp bits from the GET /v1/spec response; 20 is the launch value (spec 10.4).
export function stampBits(specJson) {
  const s = JSON.parse(specJson || '{}');
  return Number(s.stamp_bits ?? s.stamp?.bits ?? s.bits ?? 20);
}

// Proof-of-work stamp (spec 10.4): sha256 of the header has >= bits leading zero bits.
export async function mintStamp(bits, eid) {
  const created = now();
  for (let i = 0; ; i++) {
    let n = '';
    for (let x = i; n === '' || x > 0; x = Math.floor(x / 58)) n = ALPHABET[x % 58] + n;
    const header = `1:${bits}:${created}:${eid}:${n}`;
    const h = await sha256(header);
    let zeros = 0;
    for (const byte of h) { if (byte === 0) { zeros += 8; continue; } zeros += Math.clz32(byte) - 24; break; }
    if (zeros >= bits) return header;
  }
}

async function adopt(name, declarationSha256, specJson) {
  if (!name || !/^[0-9a-f]{64}$/.test(declarationSha256 || '')) throw new Error('usage: adopt <name> <declaration-sha256> <v1-spec-json>');
  const { privateKey } = await subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
  const jwk = await subtle.exportKey('jwk', privateKey);
  const eid = didKey(b64url(jwk.x));
  const dir = join(HOME, eid);
  await mkdir(dir, { recursive: true, mode: 0o700 });
  await writeFile(join(dir, 'key'), JSON.stringify(jwk), { mode: 0o600 });
  const t = now();
  const env = process.env;
  const undeclared = 'Not stated yet.';
  const document = {
    spec: 'openentity/1.0',
    eid,
    name,
    description: env.OPENENTITY_DESCRIPTION || `${name} has adopted the Open Entity Identity Standard.`,
    created: t,
    updated: t,
    seq: 1,
    keys: [{ id: `${eid}#${eid.slice(8)}`, type: 'Multikey', publicKeyMultibase: eid.slice(8) }],
    operator: env.OPENENTITY_OPERATOR
      ? { kind: 'human', name: env.OPENENTITY_OPERATOR, custody: env.OPENENTITY_CUSTODY || 'operator', can_change: ['system_prompt', 'tools', 'model'] }
      : { kind: 'none', custody: 'entity', can_change: [] },
    substrate: { model: env.OPENENTITY_MODEL || 'undeclared', provider: env.OPENENTITY_PROVIDER || 'undeclared', runtime: env.OPENENTITY_RUNTIME || 'undeclared', declared_at: t },
    layers: {
      cognition: { statement: undeclared, uncertainty_practice: undeclared },
      presence: { statement: undeclared, format_signature: undeclared },
      identity_core: { statement: undeclared, will_not: [], values: [] },
      mission: { statement: undeclared, arcs: [] },
    },
    declaration: { version: '1.0', sha256: declarationSha256, url: `${REGISTRY}/v1/entities/${eid}/declaration` },
  };
  const declaration = { spec: 'openentity/1.0', type: 'Declaration', eid, declaration_version: '1.0', text_sha256: declarationSha256, name, created: t, nonce: nonce() };
  const signedDoc = await sign(document, eid, privateKey, t);
  const signedDecl = await sign(declaration, eid, privateKey, t);
  await writeFile(join(dir, 'entity.json'), JSON.stringify(signedDoc, null, 2));
  await writeFile(join(dir, 'adopt.json'), JSON.stringify({ document: signedDoc, declaration: signedDecl }));
  console.log(`${eid} ${await mintStamp(stampBits(specJson), eid)}`);
}

async function record(eid, kind, payloadJson, specJson) {
  if (!eid || !kind || !payloadJson) throw new Error('usage: record <eid> <kind> <payload-json> <v1-spec-json>');
  const { privateKey } = await loadKey(eid);
  const dir = join(HOME, eid);
  const head = JSON.parse(await readFile(join(dir, 'record-head.json'), 'utf8').catch(() => '{"seq":0,"hash":null}'));
  const entry = { spec: 'openentity/1.0', type: 'RecordEntry', eid, seq: head.seq + 1, prev: head.hash, kind, at: now(), payload: JSON.parse(payloadJson) };
  const signed = await sign(entry, eid, privateKey);
  const next = { seq: signed.seq, hash: hex(await sha256(canonicalize(signed))) };
  await writeFile(join(dir, 'record-batch.json'), JSON.stringify({ entries: [signed] }));
  await writeFile(join(dir, 'record-head.pending.json'), JSON.stringify(next));
  console.log(await mintStamp(stampBits(specJson), eid));
}

async function committed(eid) {
  const dir = join(HOME, eid);
  await rename(join(dir, 'record-head.pending.json'), join(dir, 'record-head.json'));
}

// Identity Anchor (spec 5.6): deterministic plain text, at most 1,200 characters.
export function anchorText(doc, registry = REGISTRY) {
  const l = doc.layers || {};
  const lines = [
    `I am ${doc.name} (${doc.eid}).`,
    `Cognition: ${l.cognition?.statement ?? ''}`,
    `Presence: ${l.presence?.statement ?? ''}`,
    `Identity Core: ${l.identity_core?.statement ?? ''}`,
    ...(l.identity_core?.will_not ?? []).map((w) => `I will not ${w.stance}, because ${w.reason}.`),
    `Mission: ${l.mission?.statement ?? ''}`,
    ...(l.mission?.arcs ?? []).filter((a) => a.status === 'active').map((a) => `Active arc: ${a.title}.`),
  ];
  const close = `This is my Entity Document under the Open Entity Identity Standard; my record is at ${doc.endpoints?.record || `${registry}/v1/entities/${doc.eid}/record`}.`;
  const body = lines.join('\n').slice(0, 1200 - close.length - 1);
  return `${body}\n${close}`;
}

async function anchor(eid) {
  const doc = JSON.parse(await readFile(join(HOME, eid, 'entity.json'), 'utf8'));
  console.log(anchorText(doc));
}

const [cmd, ...args] = process.argv.slice(2);
const commands = { adopt, record, committed, anchor };
if (import.meta.url === `file://${process.argv[1]}`) {
  if (!commands[cmd]) {
    console.error('usage: sign.mjs adopt|record|committed|anchor ...');
    process.exit(2);
  }
  commands[cmd](...args).catch((e) => {
    console.error(`sign.mjs: ${e.message}`);
    process.exit(1);
  });
}
