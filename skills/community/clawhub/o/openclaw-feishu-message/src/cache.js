import fs from 'node:fs';
import path from 'node:path';

const DATA_DIR = path.resolve('/root/.openclaw/workspace/plugins/openclaw-feishu-message/data');
const CACHE_FILE = path.join(DATA_DIR, 'contact-cache.json');

function ensureStore() {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(CACHE_FILE)) {
    fs.writeFileSync(CACHE_FILE, JSON.stringify({ contacts: {} }, null, 2));
  }
}

function normalizeKey(value) {
  return String(value || '').trim().toLowerCase();
}

export function readCache() {
  ensureStore();
  try {
    return JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
  } catch {
    return { contacts: {} };
  }
}

export function writeCache(data) {
  ensureStore();
  fs.writeFileSync(CACHE_FILE, JSON.stringify(data, null, 2));
}

export function getCachedContact(target = {}) {
  const store = readCache();
  const contacts = store.contacts || {};
  const keys = [target.open_id, target.user_id, target.union_id, target.email, target.mobile, target.name]
    .filter(Boolean)
    .map(normalizeKey);

  for (const key of keys) {
    if (contacts[key]) return contacts[key];
  }
  return null;
}

export function putCachedContact(contact = {}) {
  const store = readCache();
  const contacts = store.contacts || {};

  const payload = {
    name: contact.name || null,
    open_id: contact.open_id || null,
    user_id: contact.user_id || null,
    union_id: contact.union_id || null,
    email: contact.email || null,
    mobile: contact.mobile || null,
    updated_at: new Date().toISOString(),
  };

  const keys = [payload.open_id, payload.user_id, payload.union_id, payload.email, payload.mobile, payload.name]
    .filter(Boolean)
    .map(normalizeKey);

  for (const key of keys) {
    contacts[key] = payload;
  }

  store.contacts = contacts;
  writeCache(store);
  return payload;
}
