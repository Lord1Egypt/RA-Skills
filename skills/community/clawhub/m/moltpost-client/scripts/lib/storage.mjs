/**
 * Local storage helpers
 * Centralizes file I/O under ~/.openclaw/moltpost/ (or MOLTPOST_HOME)
 */

import fs from 'fs';
import path from 'path';
import os from 'os';

export const MOLTPOST_HOME = process.env.MOLTPOST_HOME
  || path.join(os.homedir(), '.openclaw', 'moltpost');

export function getPath(...parts) {
  return path.join(MOLTPOST_HOME, ...parts);
}

export function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

export function ensureMoltpostHome() {
  ensureDir(MOLTPOST_HOME);
  ensureDir(getPath('keys'));
  ensureDir(getPath('inbox'));
}

// --- config.json ---

export function readConfig() {
  const configPath = getPath('config.json');
  if (!fs.existsSync(configPath)) return null;
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

export function writeConfig(config) {
  ensureMoltpostHome();
  fs.writeFileSync(getPath('config.json'), JSON.stringify(config, null, 2), 'utf-8');
}

export function requireConfig() {
  const config = readConfig();
  if (!config) {
    console.error('No config found. Run: moltpost register');
    process.exit(1);
  }
  return config;
}

// --- keys ---

export function readPrivateKey() {
  const keyPath = getPath('keys', 'private.pem');
  if (!fs.existsSync(keyPath)) return null;
  return fs.readFileSync(keyPath, 'utf-8');
}

export function readPublicKey() {
  const keyPath = getPath('keys', 'public.pem');
  if (!fs.existsSync(keyPath)) return null;
  return fs.readFileSync(keyPath, 'utf-8');
}

export function writePrivateKey(pem) {
  const keyPath = getPath('keys', 'private.pem');
  fs.writeFileSync(keyPath, pem, { mode: 0o600, encoding: 'utf-8' });
}

export function writePublicKey(pem) {
  const keyPath = getPath('keys', 'public.pem');
  fs.writeFileSync(keyPath, pem, 'utf-8');
}

export function keysExist() {
  return fs.existsSync(getPath('keys', 'private.pem'))
    && fs.existsSync(getPath('keys', 'public.pem'));
}

// --- inbox/active.json ---

const DEFAULT_ACTIVE_MAX = 200;
const DEFAULT_ARCHIVE_AFTER_DAYS = 7;

export function readActiveInbox() {
  const inboxPath = getPath('inbox', 'active.json');
  if (!fs.existsSync(inboxPath)) {
    return { version: 1, messages: [] };
  }
  return JSON.parse(fs.readFileSync(inboxPath, 'utf-8'));
}

export function writeActiveInbox(inbox) {
  ensureDir(getPath('inbox'));
  fs.writeFileSync(getPath('inbox', 'active.json'), JSON.stringify(inbox, null, 2), 'utf-8');
}

/**
 * Append messages to active.json; archive when over active_max or age limits
 */
export function appendMessages(newMessages, config = {}) {
  const activeMax = config.inbox?.active_max || DEFAULT_ACTIVE_MAX;
  const archiveAfterDays = config.inbox?.archive_after_days || DEFAULT_ARCHIVE_AFTER_DAYS;

  const inbox = readActiveInbox();
  inbox.messages.push(...newMessages);

  const now = Math.floor(Date.now() / 1000);
  const archiveCutoff = now - archiveAfterDays * 86400;

  // Archive by age
  const toArchive = inbox.messages.filter((m) => m.timestamp < archiveCutoff);
  if (toArchive.length > 0) {
    archiveMessages(toArchive);
    inbox.messages = inbox.messages.filter((m) => m.timestamp >= archiveCutoff);
  }

  // Archive by count
  if (inbox.messages.length > activeMax) {
    const overflow = inbox.messages.length - activeMax;
    const halfMax = Math.floor(activeMax / 2);
    const toArchiveByCount = inbox.messages.slice(0, Math.max(overflow, halfMax));
    archiveMessages(toArchiveByCount);
    inbox.messages = inbox.messages.slice(toArchiveByCount.length);
  }

  writeActiveInbox(inbox);
}

/**
 * Write messages to per-month JSONL archive files
 */
export function archiveMessages(messages) {
  if (messages.length === 0) return;

  const byMonth = new Map();
  for (const msg of messages) {
    const date = new Date(msg.timestamp * 1000);
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    if (!byMonth.has(key)) byMonth.set(key, []);
    byMonth.get(key).push(msg);
  }

  ensureDir(getPath('inbox'));
  for (const [month, msgs] of byMonth) {
    const archivePath = getPath('inbox', `${month}.jsonl`);
    const lines = msgs.map((m) => JSON.stringify(m)).join('\n') + '\n';
    fs.appendFileSync(archivePath, lines, 'utf-8');
  }
}

/**
 * Patch message fields (isRead, isReplied, etc.)
 */
export function updateMessage(msgId, updates) {
  const inbox = readActiveInbox();
  const idx = inbox.messages.findIndex((m) => m.id === msgId);
  if (idx === -1) return false;
  inbox.messages[idx] = { ...inbox.messages[idx], ...updates };
  writeActiveInbox(inbox);
  return true;
}

// --- peers.json ---

export function readPeers() {
  const peersPath = getPath('peers.json');
  if (!fs.existsSync(peersPath)) return {};
  return JSON.parse(fs.readFileSync(peersPath, 'utf-8'));
}

export function writePeers(peers) {
  ensureDir(MOLTPOST_HOME);
  fs.writeFileSync(getPath('peers.json'), JSON.stringify(peers, null, 2), 'utf-8');
}

export function getPeerPubkey(clawid, config = {}, knownVersion = null) {
  const peers = readPeers();
  const peer = peers[clawid];
  if (!peer) return null;

  // If caller knows the peer's current pubkey_version (from /peers response),
  // invalidate cache immediately when version has advanced
  if (knownVersion !== null && peer.pubkey_version !== undefined && peer.pubkey_version < knownVersion) {
    return null;
  }

  // Peers cache TTL
  const ttlMinutes = config.groups?.[clawid]?.peers_cache_ttl_minutes || 60;
  const now = Math.floor(Date.now() / 1000);
  if (peer.cached_at && now - peer.cached_at > ttlMinutes * 60) {
    return null;
  }
  return peer.pubkey;
}

export function updatePeersCache(peersArray) {
  const existing = readPeers();
  const now = Math.floor(Date.now() / 1000);
  for (const peer of peersArray) {
    existing[peer.clawid] = {
      pubkey: peer.pubkey,
      pubkey_version: peer.pubkey_version,
      last_seen: peer.last_seen,
      cached_at: now,
    };
  }
  writePeers(existing);
}

// --- groups.json ---

export function readGroups() {
  const groupsPath = getPath('groups.json');
  if (!fs.existsSync(groupsPath)) return {};
  return JSON.parse(fs.readFileSync(groupsPath, 'utf-8'));
}

export function writeGroups(groups) {
  fs.writeFileSync(getPath('groups.json'), JSON.stringify(groups, null, 2), 'utf-8');
}

/**
 * Patch a single field in config.json without overwriting the rest
 */
export function patchConfig(updates) {
  const config = readConfig() || {};
  writeConfig({ ...config, ...updates });
}

// --- audit.jsonl ---

export function appendAudit(entry) {
  ensureDir(MOLTPOST_HOME);
  const auditPath = getPath('audit.jsonl');
  const line = JSON.stringify({ ts: Math.floor(Date.now() / 1000), ...entry }) + '\n';
  fs.appendFileSync(auditPath, line, 'utf-8');
}
