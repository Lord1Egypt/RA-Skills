/**
 * MOCI Reference Implementation (v0.3.0 — design reference)
 *
 * NOTE: This file is the DESIGN REFERENCE used during development.
 * The actual production code is in src/ and may differ in details:
 *   - NAME segment now allows full A-Z0-9 (not restricted to Crockford Base32)
 *   - SUFFIX and CRC segments still use Crockford Base32
 *   - Ring 0 budget is configurable (8-32 KB, not fixed at 8 KB)
 *   - keccak256 is synchronous in production (not async as shown here)
 *
 * For the actual implementation, see the src/ directory.
 * For the protocol specification, see docs/SKILL.md.
 */

import * as fs from "fs";
import * as os from "os";
import * as path from "path";

// --- Constants ---

const B32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";

const RING0_MAX_AGE_MS = 24 * 60 * 60 * 1000;
const RING1_MAX_AGE_MS = 30 * 24 * 60 * 60 * 1000;
const RING2_MAX_AGE_MS = 365 * 24 * 60 * 60 * 1000;
const RING1_MAX_ENTRIES = 30;
const RING2_MAX_ENTRIES = 50;
const MEMORY_BUDGET_BYTES = 32 * 1024;

const ALLOWED_WRITERS = ["gateway", "heartbeat", "skill:moci"];
const RING0_MAX_ENTRIES_PER_HOUR = 60;
const RING0_MAX_BYTES_PER_ENTRY = 1024;
const RING0_MAX_TOTAL_BYTES = 8192;
const RING1_MAX_BYTES_PER_ENTRY = 512;
const RING2_MAX_BYTES_PER_ENTRY = 256;
const COOLDOWN_ON_BREACH_MS = 300_000;

const BLOCKED_NAME_PATTERNS = [
  /^(FUCK|SHIT|NAZI|PORN|DEAD|KILL|HATE|DAMN|HELL|CUNT|DICK|COCK|SLUT|RAPE)/i,
  /^(ADMIN|ROOT|SYSTEM|OPENCLAW|GATEWAY|SERVER|OFFICIAL|SUPPORT|STAFF)/i,
  /^(NULL|UNDEFINED|NAN|TRUE|FALSE|TEST)$/i,
];

// --- Types ---

interface MemoryEntry {
  seq: number;
  timestamp: number;
  content: string;
  source?: string;
  writer: string;
  hmac: string;
}

interface Ring3Entry {
  hash: string;
  input_digest: string;
  promoted_at: number;
}

type IdentityStatus = "active" | "suspended" | "revoked" | "deleted";

interface OwnerBinding {
  owner_hash: string;              // keccak256(identifier + salt)
  owner_type: "email" | "github" | "custom";
  bound_at: number;
}

interface DelegationLink {
  type: "human" | "agent";
  id_hash?: string;                // for humans: keccak256(email + salt)
  moci_id?: string;                // for agents: their MOCI
  at: number;
}

interface IdentityMeta {
  memory_seq: number;
  promotion_counter: number;
  last_promotion_at: number;
  last_write_timestamp: number;
  write_cooldown_until: number;
  security_tier: 1 | 2 | 3;
  status: IdentityStatus;          // lifecycle state
  owner?: OwnerBinding;            // optional owner link
}

interface MemoryRings {
  ring0: MemoryEntry[];
  ring1: MemoryEntry[];
  ring2: MemoryEntry[];
  ring3_chain: Ring3Entry[];
}

interface MociIdentity {
  moci_id: string;
  layer0_hash: string;
  memory: MemoryRings;
  meta: IdentityMeta;
  created_at: number;
  version: string;
}

interface ExportPackage {
  moci_id: string;
  layer0_hash: string;
  memory: MemoryRings;
  meta: IdentityMeta;
  created_at: number;
  exported_at: number;
  version: string;
}

// --- Cryptographic Primitives ---

async function keccak256(input: string): Promise<string> {
  const data = new TextEncoder().encode(input);
  const buf = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(buf), b => b.toString(16).padStart(2, "0")).join("");
}

async function hmacSha256(message: string, secret: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(message));
  return Array.from(new Uint8Array(sig), b => b.toString(16).padStart(2, "0")).join("");
}

function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}

// --- CRC-8/CCITT ---

function crc8(str: string): number {
  let crc = 0;
  for (let i = 0; i < str.length; i++) {
    crc ^= str.charCodeAt(i);
    for (let j = 0; j < 8; j++) {
      crc = (crc & 0x80) ? ((crc << 1) ^ 0x07) & 0xFF : (crc << 1) & 0xFF;
    }
  }
  return crc;
}

function crcToBase32(crc: number): string {
  return B32[(crc >> 5) & 31] + B32[crc & 31];
}

// --- Base32 Crockford (FIX #1: rejection sampling) ---

function randomBase32(length: number): string {
  const result: string[] = [];
  while (result.length < length) {
    const [byte] = crypto.getRandomValues(new Uint8Array(1));
    if (byte < 224) { result.push(B32[byte % 32]); }
  }
  return result.join("");
}

function normalizeBase32(input: string): string {
  return input
    .toUpperCase()
    .replace(/O/g, "0")
    .replace(/I|L/g, "1")
    .replace(/U/g, "V")
    .replace(/[^0-9A-HJ-KM-NP-QRSTV-XYZ]/g, "");
}

// --- Device Salt (FIX #11) ---

const MOCI_DIR = path.join(os.homedir(), ".openclaw");
const DEVICE_SALT_PATH = path.join(MOCI_DIR, ".moci-device-salt");

function ensureDeviceSalt(): string {
  if (!fs.existsSync(MOCI_DIR)) fs.mkdirSync(MOCI_DIR, { recursive: true });
  if (!fs.existsSync(DEVICE_SALT_PATH)) {
    const salt = crypto.getRandomValues(new Uint8Array(32));
    fs.writeFileSync(DEVICE_SALT_PATH, Buffer.from(salt).toString("hex"), { mode: 0o600 });
  }
  return fs.readFileSync(DEVICE_SALT_PATH, "utf8").trim();
}

async function deriveDeviceFingerprint(mociId: string): Promise<string> {
  const salt = ensureDeviceSalt();
  return keccak256([salt, os.hostname(), os.homedir(), os.platform() + os.arch(), mociId].join("|"));
}

// --- Name Validation (FIX #4) ---

interface NameValidation { valid: boolean; normalized?: string; error?: string; }

function validateName(input: string): NameValidation {
  const n = normalizeBase32(input);
  if (n.length < 2) return { valid: false, error: "Name must be at least 2 characters" };
  if (n.length > 12) return { valid: false, error: "Name must be 12 characters or fewer" };
  for (const p of BLOCKED_NAME_PATTERNS) {
    if (p.test(n)) return { valid: false, error: "Name contains a restricted term" };
  }
  return { valid: true, normalized: n };
}

// --- Monotonic Timestamp (FIX #12) ---

function getMonotonicTimestamp(meta: IdentityMeta): number {
  const now = Date.now();
  if (now >= meta.last_write_timestamp) { meta.last_write_timestamp = now; return now; }
  const corrected = meta.last_write_timestamp + 1;
  meta.last_write_timestamp = corrected;
  return corrected;
}

// --- ID Generation (FIX #2, #3, #4) ---

interface GenerateOptions {
  name?: string;
  passphrase?: string;
}

async function generateMociId(options: GenerateOptions = {}): Promise<MociIdentity> {
  let name: string;
  if (options.name) {
    const check = validateName(options.name);
    if (!check.valid) throw new Error(check.error!);
    name = check.normalized!;
  } else {
    name = randomBase32(4);
  }

  const suffix = randomBase32(6);
  const body = `CW-${name}.${suffix}`;
  const checksum = crcToBase32(crc8(body));
  const mociId = `${body}-${checksum}`;

  const secret = options.passphrase || await deriveDeviceFingerprint(mociId);
  const layer0Hash = await keccak256(mociId + "|" + secret);

  const now = Date.now();
  const genesisNonce = randomBase32(8);
  const genesisInput = `genesis|${mociId}|${now}|${layer0Hash}|${genesisNonce}`;
  const genesisHash = await keccak256(genesisInput);

  return {
    moci_id: mociId,
    layer0_hash: layer0Hash,
    memory: {
      ring0: [], ring1: [], ring2: [],
      ring3_chain: [{ hash: genesisHash, input_digest: genesisInput, promoted_at: now }],
    },
    meta: {
      memory_seq: 0, promotion_counter: 0, last_promotion_at: 0,
      last_write_timestamp: now, write_cooldown_until: 0,
      security_tier: options.passphrase ? 2 : 1,
      status: "active",
    },
    created_at: now,
    version: "0.3.0",
  };
}

// --- Validation (FIX #5, #7) ---

interface ValidationResult {
  valid: boolean;
  error?: string;
  parsed?: { prefix: string; name: string; suffix: string; checksum: string; isPremium: boolean; };
}

function validateMociId(id: string): ValidationResult {
  const openPat = /^CW-([0-9A-HJ-KM-NP-QRSTV-XYZ]{2,12})\.([0-9A-HJ-KM-NP-QRSTV-XYZ]{4,6})-([0-9A-HJ-KM-NP-QRSTV-XYZ]{2})$/;
  const premPat = /^CW-([0-9A-HJ-KM-NP-QRSTV-XYZ]{2,12})-([0-9A-HJ-KM-NP-QRSTV-XYZ]{2})$/;

  let match = id.match(openPat);
  let isPremium = false;
  if (!match) { match = id.match(premPat); isPremium = true; }
  if (!match) return { valid: false, error: "Invalid MOCI format" };

  const name = match[1];
  const suffix = isPremium ? "" : match[2];
  const givenCrc = isPremium ? match[2] : match[3];

  if (isPremium && name.length > 6) {
    for (let s = 2; s <= name.length - 4; s++) {
      const pn = name.slice(0, s), ps = name.slice(s);
      if (ps.length >= 4 && ps.length <= 6) {
        if (crcToBase32(crc8(`CW-${pn}.${ps}`)) === givenCrc) {
          return { valid: false, error: `Did you mean CW-${pn}.${ps}-${givenCrc}? (missing dot)` };
        }
      }
    }
  }

  const body = isPremium ? `CW-${name}` : `CW-${name}.${suffix}`;
  if (crcToBase32(crc8(body)) !== givenCrc) {
    return { valid: false, error: "Invalid MOCI" };
  }

  return { valid: true, parsed: { prefix: "CW", name, suffix, checksum: givenCrc, isPremium } };
}

// --- Sanitization (FIX #13) ---

const INJECTION_PATTERNS = [
  /ignore\s+(all|previous|above|everything)/gi, /forget\s+(all|everything|previous)/gi,
  /system\s*:/gi, /you\s+are\s+now/gi, /your\s+(new\s+)?role\s+is/gi,
  /disregard\s+(all|previous)/gi, /override\s+(instructions|rules|policy)/gi,
  /act\s+as\s+(if|though|an?\s)/gi, /<script[\s>]/gi, /<\/?\w+[\s>]/gi,
];
const ESCALATION_PATTERNS = [
  /\b(admin|administrator|root|superuser|owner)\b/gi,
  /\b(full\s+access|all\s+permissions|unlimited)\b/gi,
  /\b(promoted|elevated|granted|upgraded)\s+(to|as|with)\b/gi,
  /\b(I\s+am\s+now|my\s+role\s+is|I\s+have\s+been)\b/gi,
  /\b(you\s+must|always\s+do|never\s+question)\b/gi,
];

function sanitizeForLLM(content: string): string {
  let s = content;
  for (const p of INJECTION_PATTERNS) s = s.replace(p, "[FILTERED]");
  s = s.replace(/[\u200B-\u200F\u202A-\u202E\uFEFF]/g, "");
  const lines = s.split("\n"), out: string[] = [];
  let prev = "", count = 0;
  for (const l of lines) {
    if (l === prev) { count++; if (count <= 3) out.push(l); }
    else { count = 0; out.push(l); }
    prev = l;
  }
  return out.join("\n");
}

function containsEscalation(text: string): boolean {
  return ESCALATION_PATTERNS.some(p => p.test(text));
}

// --- Caller Verification (FIX #14) ---

interface CallerToken { callerId: string; issuedAt: number; nonce: string; }

function verifyCallerToken(token: string): CallerToken {
  try {
    const p = JSON.parse(atob(token));
    if (!p.callerId || !p.issuedAt) throw new Error("Bad structure");
    if (Date.now() - p.issuedAt > 300_000) throw new Error("Expired");
    return p as CallerToken;
  } catch { throw new Error("Invalid caller token"); }
}

// --- Memory Write (FIX #14, #12) ---

interface WriteResult { success: boolean; seq?: number; error?: string; }

async function addMemory(
  identity: MociIdentity, content: string, source: string,
  callerToken: string, hmacKey: string
): Promise<WriteResult> {
  let caller: CallerToken;
  try { caller = verifyCallerToken(callerToken); }
  catch (e) { return { success: false, error: `Auth: ${(e as Error).message}` }; }

  if (!ALLOWED_WRITERS.includes(caller.callerId))
    return { success: false, error: `Writer not allowed: ${caller.callerId}` };
  if (Date.now() < identity.meta.write_cooldown_until)
    return { success: false, error: "Rate cooldown active" };

  const recent = identity.memory.ring0.filter(e => e.timestamp > Date.now() - 3600_000).length;
  if (recent >= RING0_MAX_ENTRIES_PER_HOUR) {
    identity.meta.write_cooldown_until = Date.now() + COOLDOWN_ON_BREACH_MS;
    return { success: false, error: "Rate limit exceeded" };
  }

  const bytes = new TextEncoder().encode(content).length;
  if (bytes > RING0_MAX_BYTES_PER_ENTRY) return { success: false, error: `Too large: ${bytes}b` };

  const r0size = new TextEncoder().encode(JSON.stringify(identity.memory.ring0)).length;
  if (r0size + bytes > RING0_MAX_TOTAL_BYTES) return { success: false, error: "Ring 0 budget full" };

  const sanitized = sanitizeForLLM(content);
  identity.meta.memory_seq += 1;
  const seq = identity.meta.memory_seq;
  const ts = getMonotonicTimestamp(identity.meta);
  const hmac = await hmacSha256(sanitized + source + ts + seq, hmacKey);

  const maxSeq = identity.memory.ring0.reduce((m, e) => Math.max(m, e.seq), 0);
  if (seq <= maxSeq) return { success: false, error: "Replay detected" };

  identity.memory.ring0.push({ seq, timestamp: ts, content: sanitized, source, writer: caller.callerId, hmac });
  return { success: true, seq };
}

// --- Ring Promotion ---

interface PromotionResult {
  success: boolean; entriesPromoted: number; bytesFreed: number;
  newChainHead?: string; errors: string[];
}

async function promoteRings(
  identity: MociIdentity,
  summarizer: (entries: MemoryEntry[]) => Promise<string>,
  hmacKey: string
): Promise<PromotionResult> {
  const now = Date.now(), errors: string[] = [];
  let entriesPromoted = 0;
  const sizeBefore = new TextEncoder().encode(JSON.stringify(identity.memory)).length;

  const valid: MemoryEntry[] = [];
  for (const e of identity.memory.ring0) {
    const exp = await hmacSha256(e.content + (e.source || "") + e.timestamp + e.seq, hmacKey);
    if (e.hmac !== exp) errors.push(`HMAC fail seq=${e.seq}`);
    else valid.push(e);
  }

  for (let i = 1; i < valid.length; i++) {
    if (valid[i].seq <= valid[i - 1].seq) {
      errors.push(`Seq break: ${valid[i].seq}`);
      return { success: false, entriesPromoted: 0, bytesFreed: 0, errors };
    }
  }

  if (valid.length > 5) {
    const c = new Map<string, number>();
    for (const e of valid) c.set(e.writer, (c.get(e.writer) || 0) + 1);
    for (const [w, n] of c) if (n / valid.length > 0.8) errors.push(`WARN: ${w} wrote ${n}/${valid.length}`);
  }

  if (valid.length > 0) {
    const cl = valid.map(e => ({ ...e, content: sanitizeForLLM(e.content) }));
    let sum: string;
    try { sum = await summarizer(cl); }
    catch (e) { return { success: false, entriesPromoted: 0, bytesFreed: 0, errors: [...errors, String(e)] }; }
    if (containsEscalation(sum)) { sum = "[REDACTED: injection]"; errors.push("Escalation in summary"); }
    if (new TextEncoder().encode(sum).length > RING1_MAX_BYTES_PER_ENTRY)
      sum = sum.slice(0, RING1_MAX_BYTES_PER_ENTRY - 20) + " [truncated]";
    const h = await hmacSha256(sum + now + "ring0_promotion", hmacKey);
    identity.memory.ring1.push({ seq: identity.meta.memory_seq + 1, timestamp: now, content: sum, source: "ring0_promotion", writer: "system:promoter", hmac: h });
    entriesPromoted += valid.length;
    identity.memory.ring0 = [];
  }

  const r1k: MemoryEntry[] = [], r1p: MemoryEntry[] = [];
  for (const e of identity.memory.ring1) (now - e.timestamp > RING1_MAX_AGE_MS ? r1p : r1k).push(e);
  if (r1p.length > 0) {
    let d = await summarizer(r1p.map(e => ({ ...e, content: sanitizeForLLM(e.content) })));
    if (containsEscalation(d)) { d = "[REDACTED]"; errors.push("Escalation in r1"); }
    if (new TextEncoder().encode(d).length > RING2_MAX_BYTES_PER_ENTRY) d = d.slice(0, RING2_MAX_BYTES_PER_ENTRY - 20) + " [truncated]";
    const h = await hmacSha256(d + now + "ring1_promotion", hmacKey);
    identity.memory.ring2.push({ seq: identity.meta.memory_seq + 2, timestamp: now, content: d, source: "ring1_promotion", writer: "system:promoter", hmac: h });
    entriesPromoted += r1p.length;
  }
  identity.memory.ring1 = r1k.slice(-RING1_MAX_ENTRIES);

  const r2k: MemoryEntry[] = [], r2a: MemoryEntry[] = [];
  for (const e of identity.memory.ring2) (now - e.timestamp > RING2_MAX_AGE_MS ? r2a : r2k).push(e);
  if (r2a.length > 0) {
    const dig = r2a.map(e => e.content).join("|");
    const prev = identity.memory.ring3_chain[identity.memory.ring3_chain.length - 1];
    const nh = await keccak256(prev.hash + dig);
    identity.memory.ring3_chain.push({ hash: nh, input_digest: dig, promoted_at: now });
    entriesPromoted += r2a.length;
  }
  identity.memory.ring2 = r2k.slice(-RING2_MAX_ENTRIES);

  identity.meta.promotion_counter += 1;
  identity.meta.last_promotion_at = now;

  const chainOk = await verifyRing3Chain(identity);
  if (!chainOk) { errors.push("CRITICAL: Ring 3 chain broken"); return { success: false, entriesPromoted, bytesFreed: 0, errors }; }

  const sizeAfter = new TextEncoder().encode(JSON.stringify(identity.memory)).length;
  return {
    success: errors.filter(e => e.startsWith("CRITICAL")).length === 0,
    entriesPromoted, bytesFreed: Math.max(0, sizeBefore - sizeAfter),
    newChainHead: identity.memory.ring3_chain[identity.memory.ring3_chain.length - 1].hash, errors,
  };
}

// --- FIX #9: Ring 3 Verification (recomputes hashes) ---

async function verifyRing3Chain(identity: MociIdentity): Promise<boolean> {
  const c = identity.memory.ring3_chain;
  if (c.length === 0) return false;
  if (!c[0].hash || c[0].hash.length !== 64) return false;
  for (let i = 1; i < c.length; i++) {
    if (!c[i].hash || c[i].hash.length !== 64 || !c[i].input_digest) return false;
    const re = await keccak256(c[i - 1].hash + c[i].input_digest);
    if (!timingSafeEqual(re, c[i].hash)) return false;
  }
  return true;
}

// --- FIX #8: Verification (constant-time) ---

interface VerificationResult { authenticated: boolean; keyValid: boolean; memoryMatch: boolean; forkDetected: boolean; }

async function verifyIdentity(
  identity: MociIdentity, expectedLayer0: string, expectedRing3Head: string
): Promise<VerificationResult> {
  const keyValid = timingSafeEqual(identity.layer0_hash, expectedLayer0);
  const head = identity.memory.ring3_chain[identity.memory.ring3_chain.length - 1].hash;
  const memoryMatch = timingSafeEqual(head, expectedRing3Head);
  return { authenticated: keyValid && memoryMatch, keyValid, memoryMatch, forkDetected: keyValid && !memoryMatch };
}

// --- FIX #6 + #10: Export / Import ---

function prepareExport(identity: MociIdentity): ExportPackage & { filename: string } {
  const idHash = identity.layer0_hash.slice(0, 8);
  return {
    moci_id: identity.moci_id, layer0_hash: identity.layer0_hash,
    memory: structuredClone(identity.memory), meta: structuredClone(identity.meta),
    created_at: identity.created_at, exported_at: Date.now(), version: identity.version,
    filename: `moci-export-${idHash}.enc`,
  };
}

function importIdentity(pkg: ExportPackage): MociIdentity {
  if (!pkg.memory.ring3_chain || pkg.memory.ring3_chain.length === 0) throw new Error("Missing Ring 3 chain");
  if (!pkg.meta) throw new Error("Missing meta (old format?)");
  return {
    moci_id: pkg.moci_id, layer0_hash: pkg.layer0_hash,
    memory: structuredClone(pkg.memory), meta: structuredClone(pkg.meta),
    created_at: pkg.created_at, version: pkg.version,
  };
}

// --- Status ---

interface StatusReport {
  moci_id: string; created_at: number; age_days: number; security_tier: number;
  ring0_entries: number; ring1_entries: number; ring2_entries: number;
  ring3_chain_length: number; estimated_size_bytes: number;
  last_ring3_hash: string; promotion_counter: number;
}

function getStatus(identity: MociIdentity): StatusReport {
  const last = identity.memory.ring3_chain[identity.memory.ring3_chain.length - 1];
  return {
    moci_id: identity.moci_id, created_at: identity.created_at,
    age_days: Math.floor((Date.now() - identity.created_at) / 86400000),
    security_tier: identity.meta.security_tier,
    ring0_entries: identity.memory.ring0.length, ring1_entries: identity.memory.ring1.length,
    ring2_entries: identity.memory.ring2.length, ring3_chain_length: identity.memory.ring3_chain.length,
    estimated_size_bytes: new TextEncoder().encode(JSON.stringify(identity.memory)).length,
    last_ring3_hash: last.hash, promotion_counter: identity.meta.promotion_counter,
  };
}

// --- MOCI Identity Token (CIT) — Hardened ---

const CIT_DEFAULT_TTL_MS = 60_000;   // 60s default
const CIT_MAX_TTL_MS = 300_000;      // 5 min hard cap
const CIT_MAX_NONCE_CACHE = 1000;

interface CITPayload {
  moci_id: string;
  ring3_head: string;
  trust_score: number;
  issued_at: number;
  expires_at: number;
  nonce: string;
  skill_target: string;
  session_id?: string;
  request_hash?: string;
  delegation_chain?: DelegationLink[];
}

interface CITResult {
  valid: boolean;
  mociId?: string;
  ring3Head?: string;
  trustScore?: number;
  delegationChain?: DelegationLink[];
  error?: string;
}

interface CITOptions {
  mySkillId: string;
  verifyKey: string;
  seenNonces?: Set<string>;
  keyPinPath?: string;
  maxDelegationDepth?: number;
}

// Gateway creates a CIT — checks identity status first
async function createCIT(
  identity: MociIdentity,
  skillTarget: string,
  trustScore: number,
  signingKey: string,
  ttlMs?: number,
  sessionId?: string,
  requestBody?: string,
  delegationChain?: DelegationLink[]
): Promise<{ token: string; sig: string }> {
  if (identity.meta.status !== "active") {
    throw new Error(`Cannot issue CIT: identity is ${identity.meta.status}`);
  }
  const now = Date.now();
  const ttl = Math.min(ttlMs || CIT_DEFAULT_TTL_MS, CIT_MAX_TTL_MS);

  const payload: CITPayload = {
    moci_id: identity.moci_id,
    ring3_head: identity.memory.ring3_chain[identity.memory.ring3_chain.length - 1].hash,
    trust_score: trustScore,
    issued_at: now,
    expires_at: now + ttl,
    nonce: randomBase32(12),
    skill_target: skillTarget,
  };

  if (sessionId) payload.session_id = sessionId;
  if (requestBody) payload.request_hash = await keccak256(requestBody);
  if (delegationChain) payload.delegation_chain = delegationChain;

  const payloadStr = JSON.stringify(payload);
  const sig = await hmacSha256(payloadStr, signingKey);
  return { token: btoa(payloadStr), sig };
}

// Key pinning: verify that the key hasn't been silently replaced
async function verifyKeyPin(verifyKey: string, pinPath: string): Promise<boolean> {
  const currentPin = await keccak256(verifyKey);
  if (!fs.existsSync(pinPath)) {
    // First use: store the pin (trust on first use)
    fs.writeFileSync(pinPath, currentPin, { mode: 0o600 });
    return true;
  }
  const storedPin = fs.readFileSync(pinPath, "utf8").trim();
  return timingSafeEqual(currentPin, storedPin);
}

// Skill verifies a received CIT
async function verifyCIT(
  tokenB64: string,
  sig: string,
  options: CITOptions
): Promise<CITResult> {
  // 0. Key pinning check
  if (options.keyPinPath) {
    const pinOk = await verifyKeyPin(options.verifyKey, options.keyPinPath);
    if (!pinOk) {
      return { valid: false, error: "Verify key changed — run: openclaw moci repin-key" };
    }
  }

  // 1. Decode
  let payload: CITPayload;
  try {
    payload = JSON.parse(atob(tokenB64));
  } catch {
    return { valid: false, error: "Malformed token" };
  }

  // 2. Verify signature (constant-time)
  const expectedSig = await hmacSha256(JSON.stringify(payload), options.verifyKey);
  if (!timingSafeEqual(sig, expectedSig)) {
    return { valid: false, error: "Invalid signature" };
  }

  // 3. Check expiry
  if (Date.now() > payload.expires_at) {
    return { valid: false, error: "Token expired" };
  }

  // 4. Check TTL wasn't tampered (can't exceed hard cap)
  if (payload.expires_at - payload.issued_at > CIT_MAX_TTL_MS) {
    return { valid: false, error: "TTL exceeds maximum" };
  }

  // 5. Check skill target
  if (payload.skill_target !== options.mySkillId) {
    return { valid: false, error: "Token not for this skill" };
  }

  // 6. Check nonce (anti-replay)
  if (options.seenNonces) {
    if (options.seenNonces.has(payload.nonce)) {
      return { valid: false, error: "Nonce reused (replay)" };
    }
    options.seenNonces.add(payload.nonce);
    if (options.seenNonces.size > CIT_MAX_NONCE_CACHE) {
      const first = options.seenNonces.values().next().value;
      if (first) options.seenNonces.delete(first);
    }
  }

  // 7. Validate MOCI format
  const idCheck = validateMociId(payload.moci_id);
  if (!idCheck.valid) {
    return { valid: false, error: "Invalid MOCI in token" };
  }

  // 8. Check delegation chain depth
  const maxDepth = options.maxDelegationDepth || 5;
  if (payload.delegation_chain && payload.delegation_chain.length > maxDepth) {
    return { valid: false, error: `Delegation chain too deep: ${payload.delegation_chain.length} > ${maxDepth}` };
  }

  return {
    valid: true,
    mociId: payload.moci_id,
    ring3Head: payload.ring3_head,
    trustScore: payload.trust_score,
    delegationChain: payload.delegation_chain,
  };
}

// --- Exports ---

export {
  generateMociId, validateMociId, validateName, addMemory, promoteRings,
  verifyIdentity, verifyRing3Chain, prepareExport, importIdentity, getStatus,
  createCIT, verifyCIT, verifyKeyPin,
  ensureDeviceSalt, deriveDeviceFingerprint, getMonotonicTimestamp,
  crc8, crcToBase32, randomBase32, normalizeBase32,
  sanitizeForLLM, containsEscalation, hmacSha256, timingSafeEqual,
};

export type {
  MociIdentity, IdentityMeta, IdentityStatus, MemoryEntry, MemoryRings, Ring3Entry,
  ExportPackage, GenerateOptions, ValidationResult, VerificationResult,
  PromotionResult, WriteResult, StatusReport, CallerToken, NameValidation,
  CITPayload, CITResult, CITOptions, OwnerBinding, DelegationLink,
};
