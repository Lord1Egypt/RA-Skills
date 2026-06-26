// ============================================
// scripts/storage.js — File-based alert storage
// Menyimpan data di .data/ dalam direktori skill
// ============================================

import fs from "node:fs/promises";
import path from "node:path";

/**
 * Simple JSON file storage untuk AlertRule
 * Cocok untuk OpenClaw self-hosted (tidak perlu DB eksternal)
 */
export class FileAlertStorage {
  constructor(filePath) {
    this.filePath = filePath;
  }

  async _ensureFile() {
    const dir = path.dirname(this.filePath);
    await fs.mkdir(dir, { recursive: true });
    try {
      await fs.access(this.filePath);
    } catch {
      await fs.writeFile(this.filePath, JSON.stringify([]));
    }
  }

  async _readAll() {
    await this._ensureFile();
    const raw = await fs.readFile(this.filePath, "utf-8");
    const parsed = JSON.parse(raw);
    // Restore Date objects
    return parsed.map((a) => ({
      ...a,
      createdAt: new Date(a.createdAt),
    }));
  }

  async _writeAll(alerts) {
    await this._ensureFile();
    await fs.writeFile(this.filePath, JSON.stringify(alerts, null, 2));
  }

  async getAlerts(userId) {
    const all = await this._readAll();
    return all.filter((a) => a.userId === userId);
  }

  async saveAlert(alert) {
    const all = await this._readAll();
    all.push(alert);
    await this._writeAll(all);
  }

  async deleteAlert(id) {
    const all = await this._readAll();
    const filtered = all.filter((a) => a.id !== id);
    if (filtered.length === all.length) {
      throw new Error(`Alert dengan id "${id}" tidak ditemukan`);
    }
    await this._writeAll(filtered);
  }

  async markTriggered(id) {
    const all = await this._readAll();
    const idx = all.findIndex((a) => a.id === id);
    if (idx === -1) throw new Error(`Alert "${id}" tidak ditemukan`);
    all[idx].triggered = true;
    await this._writeAll(all);
  }

  async getAllUserIds() {
    const all = await this._readAll();
    return [...new Set(all.filter((a) => !a.triggered).map((a) => a.userId))];
  }
}

/**
 * In-memory storage (untuk testing)
 */
export class MemoryAlertStorage {
  constructor() {
    this.store = new Map();
  }

  async getAlerts(userId) {
    return [...(this.store.values())].filter((a) => a.userId === userId);
  }

  async saveAlert(alert) {
    this.store.set(alert.id, { ...alert });
  }

  async deleteAlert(id) {
    if (!this.store.has(id)) throw new Error(`Alert "${id}" tidak ditemukan`);
    this.store.delete(id);
  }

  async markTriggered(id) {
    const alert = this.store.get(id);
    if (!alert) throw new Error(`Alert "${id}" tidak ditemukan`);
    this.store.set(id, { ...alert, triggered: true });
  }

  async getAllUserIds() {
    const all = [...this.store.values()];
    return [...new Set(all.filter((a) => !a.triggered).map((a) => a.userId))];
  }
}
