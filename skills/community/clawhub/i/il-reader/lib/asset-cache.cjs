'use strict';

// Runtime-only cache for explicitly indexed skill assets. It never scans a
// directory, and each reuse checks both the real path and file metadata.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

function within(root, file) {
  const relative = path.relative(root, file);
  return relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative);
}

class FileAssetCache {
  constructor() {
    this.entries = new Map();
    this.metrics = { stats: 0, reads: 0, hits: 0, hashes: 0 };
  }

  inspect(file, allowedRoot) {
    const realPath = fs.realpathSync(file);
    if (allowedRoot && !within(fs.realpathSync(allowedRoot), realPath)) throw new Error('Skill asset escapes its managed directory.');
    this.metrics.stats++;
    const stat = fs.statSync(realPath, { bigint: true });
    if (!stat.isFile()) throw new Error('Skill asset must be a regular file.');
    const signature = [realPath, stat.dev, stat.ino, stat.size, stat.mtimeNs, stat.ctimeNs].map(String).join('|');
    return { signature, realPath };
  }

  load(file, { allowedRoot, json = false } = {}) {
    const key = path.resolve(file);
    try {
      let inspected = this.inspect(key, allowedRoot);
      const previous = this.entries.get(key);
      if (previous && previous.signature === inspected.signature && previous.json === json) {
        this.metrics.hits++;
        return previous;
      }
      // A changed or malformed asset must never fall back to its old contents.
      this.entries.delete(key);
      for (let attempt = 0; attempt < 2; attempt++) {
        this.metrics.reads++;
        const raw = fs.readFileSync(inspected.realPath);
        const after = this.inspect(key, allowedRoot);
        if (inspected.signature !== after.signature) {
          inspected = after;
          continue;
        }
        const value = json ? JSON.parse(raw.toString('utf8').replace(/^\uFEFF/, '')) : undefined;
        this.metrics.hashes++;
        const entry = { ...after, raw, value, json, sha256: crypto.createHash('sha256').update(raw).digest('hex') };
        this.entries.set(key, entry);
        return entry;
      }
      throw new Error('Skill asset changed while reading; retry after the update completes.');
    } catch (error) {
      this.entries.delete(key);
      throw error;
    }
  }

  diagnostics() { return { ...this.metrics }; }
}

module.exports = { FileAssetCache };
