#!/usr/bin/env node

/**
 * Joplin Server API Client
 * A JavaScript port of joppy's server_api.py
 * https://github.com/marph91/joppy
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Configuration
const CONFIG_FILE = path.join(process.env.HOME, '.joplin-server-config');

// TLS certificate validation - disable only if explicitly set (for self-signed certs)
const SKIP_TLS_VERIFY = process.env.JOPLIN_SKIP_TLS_VERIFY === '1' ||
                        process.env.JOPLIN_SKIP_TLS_VERIFY === 'true';
const SESSION_FILE = path.join(process.env.HOME, '.joplin-session');
const TIMEOUT_MS = 30000;

// Item types (matches Joplin's type_ field)
const ItemType = {
  NOTE: 1,
  FOLDER: 2,
  SETTING: 3,
  RESOURCE: 4,
  TAG: 5,
  NOTE_TAG: 6,
  REVISION: 13
};

const LockType = {
  NONE: 0,
  SYNC: 1,
  EXCLUSIVE: 2
};

const LockClientType = {
  DESKTOP: 1,
  MOBILE: 2,
  CLI: 3
};

// Generate a 32-char hex UUID
function generateId() {
  return crypto.randomBytes(16).toString('hex');
}

// Load config from environment or file
function loadConfig() {
  let config = {
    url: process.env.JOPLIN_SERVER_URL,
    email: process.env.JOPLIN_EMAIL,
    password: process.env.JOPLIN_PASSWORD,
    skipTlsVerify: SKIP_TLS_VERIFY
  };

  if (!config.url && fs.existsSync(CONFIG_FILE)) {
    const content = fs.readFileSync(CONFIG_FILE, 'utf8');
    for (const line of content.split('\n')) {
      const [key, ...valueParts] = line.split('=');
      const value = valueParts.join('=').trim();
      if (key.trim() === 'JOPLIN_SERVER_URL') config.url = value;
      if (key.trim() === 'JOPLIN_EMAIL') config.email = value;
      if (key.trim() === 'JOPLIN_PASSWORD') config.password = value;
      if (key.trim() === 'JOPLIN_SKIP_TLS_VERIFY') {
        config.skipTlsVerify = value === '1' || value === 'true';
      }
    }
  }

  return config;
}

// Deserialize Joplin item format to object
function deserialize(body) {
  const extractMetadata = (text) => {
    const metadata = {};
    for (const line of text.split('\n')) {
      const colonIdx = line.indexOf(': ');
      if (colonIdx > 0) {
        const key = line.slice(0, colonIdx);
        const value = line.slice(colonIdx + 2);
        if (value) metadata[key] = value;
      }
    }
    return metadata;
  };

  const parts = body.split('\n\n');
  let title = null;
  let noteBody = null;
  let metadata = {};

  if (parts.length === 1) {
    // metadata only
    metadata = extractMetadata(parts[0]);
  } else {
    // Last part is metadata
    metadata = extractMetadata(parts[parts.length - 1]);
    // First part is title, middle parts are body
    title = parts[0];
    if (parts.length > 2) {
      noteBody = parts.slice(1, -1).join('\n\n');
    }
  }

  if (title) metadata.title = title;
  if (noteBody) metadata.body = noteBody;

  return metadata;
}

// Serialize object to Joplin item format
function serializeNote(data) {
  const lines = [];

  // Title first
  lines.push(data.title || '');
  lines.push('');

  // Body if present
  if (data.body) {
    lines.push(data.body);
    lines.push('');
  }

  // ID (required)
  if (!data.id) data.id = generateId();
  lines.push(`id: ${data.id}`);

  // Parent ID
  if (data.parent_id) lines.push(`parent_id: ${data.parent_id}`);

  // Timestamps
  const now = new Date().toISOString();
  lines.push(`created_time: ${data.created_time || now}`);
  lines.push(`updated_time: ${data.updated_time || now}`);
  lines.push(`user_created_time: ${data.user_created_time || now}`);
  lines.push(`user_updated_time: ${data.user_updated_time || now}`);

  // Type
  lines.push(`type_: ${data.type_ || ItemType.NOTE}`);

  // Markup language (1 = markdown)
  lines.push(`markup_language: ${data.markup_language || 1}`);

  // Source application
  lines.push(`source_application: ${data.source_application || 'joplin-js'}`);

  // Todo fields
  if (data.is_todo) {
    lines.push(`is_todo: 1`);
    lines.push(`todo_due: ${data.todo_due || 0}`);
    lines.push(`todo_completed: ${data.todo_completed || 0}`);
  }

  return lines.join('\n');
}

function serializeNotebook(data) {
  const lines = [];

  if (data.title) {
    lines.push(data.title);
    lines.push('');
  }

  if (!data.id) data.id = generateId();
  lines.push(`id: ${data.id}`);

  if (data.parent_id) lines.push(`parent_id: ${data.parent_id}`);

  const now = new Date().toISOString();
  lines.push(`created_time: ${data.created_time || now}`);
  lines.push(`updated_time: ${data.updated_time || now}`);
  lines.push(`user_created_time: ${data.user_created_time || now}`);
  lines.push(`user_updated_time: ${data.user_updated_time || now}`);
  lines.push(`type_: ${ItemType.FOLDER}`);

  return lines.join('\n');
}

function serializeTag(data) {
  const lines = [];

  if (data.title) {
    lines.push(data.title);
    lines.push('');
  }

  if (!data.id) data.id = generateId();
  lines.push(`id: ${data.id}`);

  const now = new Date().toISOString();
  lines.push(`created_time: ${data.created_time || now}`);
  lines.push(`updated_time: ${data.updated_time || now}`);
  lines.push(`user_created_time: ${data.user_created_time || now}`);
  lines.push(`user_updated_time: ${data.user_updated_time || now}`);
  lines.push(`type_: ${ItemType.TAG}`);

  return lines.join('\n');
}

function serializeNoteTag(data) {
  const lines = [];

  if (!data.id) data.id = generateId();
  lines.push(`id: ${data.id}`);
  lines.push(`note_id: ${data.note_id}`);
  lines.push(`tag_id: ${data.tag_id}`);

  const now = new Date().toISOString();
  lines.push(`created_time: ${data.created_time || now}`);
  lines.push(`updated_time: ${data.updated_time || now}`);
  lines.push(`user_created_time: ${data.user_created_time || now}`);
  lines.push(`user_updated_time: ${data.user_updated_time || now}`);
  lines.push(`type_: ${ItemType.NOTE_TAG}`);

  return lines.join('\n');
}

// Add .md suffix if not present
function addSuffix(id, suffix = '.md') {
  return id.endsWith(suffix) ? id : id + suffix;
}

function removeSuffix(id) {
  return id.replace(/\.md$/, '');
}

/**
 * Joplin Server API Client
 */
class ServerApi {
  constructor(config = {}) {
    const loaded = loadConfig();
    this.url = (config.url || loaded.url || '').replace(/\/$/, '');
    this.email = config.email || loaded.email;
    this.password = config.password || loaded.password;
    this.skipTlsVerify = config.skipTlsVerify !== undefined ? config.skipTlsVerify : loaded.skipTlsVerify;
    this.clientId = generateId();
    this.cookies = {};
    this.currentSyncLock = null;
    this.lockTtl = 3 * 60 * 1000; // 3 minutes
    this.lockAutoRefreshInterval = 60 * 1000; // 1 minute
  }

  // HTTP request helper
  async _request(method, urlPath, options = {}) {
    return new Promise((resolve, reject) => {
      const fullUrl = new URL(urlPath, this.url);
      const protocol = fullUrl.protocol === 'https:' ? https : http;

      // Build cookie header
      const cookieHeader = Object.entries(this.cookies)
        .map(([k, v]) => `${k}=${v}`)
        .join('; ');

      const reqOptions = {
        hostname: fullUrl.hostname,
        port: fullUrl.port || (fullUrl.protocol === 'https:' ? 443 : 80),
        path: fullUrl.pathname + fullUrl.search,
        method: method.toUpperCase(),
        headers: {
          'Content-Type': options.contentType || 'application/json',
          ...(cookieHeader && { 'Cookie': cookieHeader }),
          ...options.headers
        },
        rejectUnauthorized: !this.skipTlsVerify
      };

      const req = protocol.request(reqOptions, (res) => {
        // Store cookies
        const setCookie = res.headers['set-cookie'];
        if (setCookie) {
          for (const cookie of setCookie) {
            const [kv] = cookie.split(';');
            const [key, value] = kv.split('=');
            this.cookies[key] = value;
          }
        }

        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          let parsed = data;
          try {
            parsed = JSON.parse(data);
          } catch (e) {}

          if (res.statusCode >= 400) {
            reject({
              status: res.statusCode,
              message: typeof parsed === 'object' ? parsed.error : data,
              data: parsed
            });
          } else {
            resolve({
              status: res.statusCode,
              data: parsed,
              text: data
            });
          }
        });
      });

      req.setTimeout(TIMEOUT_MS, () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });

      req.on('error', reject);

      if (options.body) {
        const bodyStr = typeof options.body === 'string'
          ? options.body
          : JSON.stringify(options.body);
        req.write(bodyStr);
      }

      req.end();
    });
  }

  async get(path, query = {}) {
    const queryStr = Object.entries(query)
      .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
      .join('&');
    const fullPath = queryStr ? `${path}?${queryStr}` : path;
    return this._request('GET', fullPath);
  }

  async post(path, body) {
    return this._request('POST', path, { body });
  }

  async put(path, data, contentType = 'application/octet-stream') {
    return this._request('PUT', path, { body: data, contentType });
  }

  async delete(path) {
    return this._request('DELETE', path);
  }

  // Authentication
  async login() {
    const res = await this.post('/login', {
      email: this.email,
      password: this.password
    });
    return res;
  }

  async ping() {
    return this.get('/api/ping');
  }

  // Sync lock management
  async _addLock() {
    const res = await this.post('/api/locks', {
      type: LockType.SYNC,
      clientId: this.clientId,
      clientType: LockClientType.DESKTOP
    });
    return res.data;
  }

  async _deleteLock(type, clientType, clientId) {
    await this.delete(`/api/locks/${type}_${clientType}_${clientId}`);
  }

  async _getLocks() {
    const res = await this.get('/api/locks');
    return res.data;
  }

  _isLockActive(updatedTime) {
    const updated = new Date(updatedTime).getTime();
    return updated + this.lockTtl > Date.now();
  }

  async _acquireSyncLock() {
    const locks = await this._getLocks();

    // Check for active exclusive locks
    for (const lock of locks.items || []) {
      if (lock.type === LockType.EXCLUSIVE && this._isLockActive(lock.updatedTime)) {
        throw new Error('Sync target has exclusive lock');
      }
    }

    this.currentSyncLock = await this._addLock();
    return this.currentSyncLock;
  }

  async _deleteOwnLock() {
    if (this.currentSyncLock) {
      await this._deleteLock(LockType.SYNC, LockClientType.DESKTOP, this.clientId);
      this.currentSyncLock = null;
    }
  }

  // Execute with sync lock
  async withSyncLock(fn) {
    await this.login();
    await this._acquireSyncLock();
    try {
      return await fn();
    } finally {
      await this._deleteOwnLock();
    }
  }

  // Note operations
  async addNote(data) {
    const noteData = { ...data, type_: ItemType.NOTE };
    if (!noteData.id) noteData.id = generateId();
    const serialized = serializeNote(noteData);
    await this.put(`/api/items/root:/${addSuffix(noteData.id)}:/content`, serialized);
    return noteData.id;
  }

  async getNote(id) {
    const res = await this.get(`/api/items/root:/${addSuffix(id)}:/content`);
    return deserialize(res.text);
  }

  async modifyNote(id, data) {
    const existing = await this.getNote(id);
    const merged = { ...existing, ...data, id: removeSuffix(id) };
    merged.updated_time = new Date().toISOString();
    const serialized = serializeNote(merged);
    await this.put(`/api/items/root:/${addSuffix(id)}:/content`, serialized);
  }

  async deleteNote(id) {
    await this.delete(`/api/items/root:/${addSuffix(id)}:`);
  }

  // Notebook operations
  async addNotebook(data) {
    const notebookData = { ...data };
    if (!notebookData.id) notebookData.id = generateId();
    const serialized = serializeNotebook(notebookData);
    await this.put(`/api/items/root:/${addSuffix(notebookData.id)}:/content`, serialized);
    return notebookData.id;
  }

  async getNotebook(id) {
    const res = await this.get(`/api/items/root:/${addSuffix(id)}:/content`);
    return deserialize(res.text);
  }

  async modifyNotebook(id, data) {
    const existing = await this.getNotebook(id);
    const merged = { ...existing, ...data, id: removeSuffix(id) };
    merged.updated_time = new Date().toISOString();
    const serialized = serializeNotebook(merged);
    await this.put(`/api/items/root:/${addSuffix(id)}:/content`, serialized);
  }

  async deleteNotebook(id) {
    await this.delete(`/api/items/root:/${addSuffix(id)}:`);
  }

  // Tag operations
  async addTag(data) {
    const tagData = { ...data };
    if (!tagData.id) tagData.id = generateId();
    const serialized = serializeTag(tagData);
    await this.put(`/api/items/root:/${addSuffix(tagData.id)}:/content`, serialized);
    return tagData.id;
  }

  async getTag(id) {
    const res = await this.get(`/api/items/root:/${addSuffix(id)}:/content`);
    return deserialize(res.text);
  }

  async deleteTag(id) {
    await this.delete(`/api/items/root:/${addSuffix(id)}:`);
  }

  async addTagToNote(tagId, noteId) {
    const noteTagData = {
      tag_id: tagId,
      note_id: noteId,
      id: generateId()
    };
    const serialized = serializeNoteTag(noteTagData);
    await this.put(`/api/items/root:/${addSuffix(noteTagData.id)}:/content`, serialized);
    return noteTagData.id;
  }

  // List operations
  async getItems(query = {}) {
    const res = await this.get('/api/items/root:/:/children', query);
    return res.data;
  }

  async getAllNotes() {
    const items = await this.getItems();
    const notes = [];
    for (const item of items.items || []) {
      if (item.name && item.name.endsWith('.md')) {
        try {
          const note = await this.getNote(removeSuffix(item.name));
          if (note.type_ == ItemType.NOTE) {
            notes.push(note);
          }
        } catch (e) {}
      }
    }
    return notes;
  }

  async getAllNotebooks() {
    const items = await this.getItems();
    const notebooks = [];
    for (const item of items.items || []) {
      if (item.name && item.name.endsWith('.md')) {
        try {
          const notebook = await this.getNotebook(removeSuffix(item.name));
          if (notebook.type_ == ItemType.FOLDER) {
            notebooks.push(notebook);
          }
        } catch (e) {}
      }
    }
    return notebooks;
  }

  async getAllTags() {
    const items = await this.getItems();
    const tags = [];
    for (const item of items.items || []) {
      if (item.name && item.name.endsWith('.md')) {
        try {
          const tag = await this.getTag(removeSuffix(item.name));
          if (tag.type_ == ItemType.TAG) {
            tags.push(tag);
          }
        } catch (e) {}
      }
    }
    return tags;
  }

  // Search (simple title/body search)
  async search(query) {
    const notes = await this.getAllNotes();
    const queryLower = query.toLowerCase();
    return notes.filter(note =>
      (note.title && note.title.toLowerCase().includes(queryLower)) ||
      (note.body && note.body.toLowerCase().includes(queryLower))
    );
  }
}

// CLI interface
async function main() {
  const [command, ...args] = process.argv.slice(2);

  if (!command) {
    console.log(JSON.stringify({
      ok: false,
      error: 'Usage: node joplin-server-api.js <command> [args...]',
      commands: [
        'ping',
        'login',
        'add-notebook <title>',
        'add-note <title> [parent_id]',
        'get-note <id>',
        'modify-note <id> <field> <value>',
        'delete-note <id>',
        'list-notes',
        'list-notebooks',
        'search <query>'
      ]
    }, null, 2));
    process.exit(1);
  }

  const api = new ServerApi();
  let result;

  try {
    switch (command) {
      case 'ping':
        result = await api.ping();
        break;

      case 'login':
        result = await api.login();
        break;

      case 'add-notebook':
        result = await api.withSyncLock(async () => {
          const id = await api.addNotebook({ title: args[0] });
          return { id, title: args[0] };
        });
        break;

      case 'add-note':
        result = await api.withSyncLock(async () => {
          const id = await api.addNote({
            title: args[0],
            body: args[2] || '',
            parent_id: args[1] || ''
          });
          return { id, title: args[0] };
        });
        break;

      case 'get-note':
        await api.login();
        result = await api.getNote(args[0]);
        break;

      case 'modify-note':
        result = await api.withSyncLock(async () => {
          await api.modifyNote(args[0], { [args[1]]: args[2] });
          return { id: args[0], modified: true };
        });
        break;

      case 'delete-note':
        result = await api.withSyncLock(async () => {
          await api.deleteNote(args[0]);
          return { id: args[0], deleted: true };
        });
        break;

      case 'list-notes':
        await api.login();
        result = await api.getAllNotes();
        break;

      case 'list-notebooks':
        await api.login();
        result = await api.getAllNotebooks();
        break;

      case 'search':
        await api.login();
        result = await api.search(args.join(' '));
        break;

      default:
        result = { error: `Unknown command: ${command}` };
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.log(JSON.stringify({
      ok: false,
      error: err.message || err
    }, null, 2));
    process.exit(1);
  }
}

// Export for use as module
module.exports = { ServerApi, ItemType, deserialize };

// Run CLI if executed directly
if (require.main === module) {
  main();
}
