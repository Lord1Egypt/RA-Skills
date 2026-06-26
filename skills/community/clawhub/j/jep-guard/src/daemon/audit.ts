import { JPEvent, AuditFilter } from '../core/types';
import fs from 'fs';
import path from 'path';
import os from 'os';

export class AuditStreamService {
  private streamPath: string;
  private events: JPEvent[] = [];
  private maxMemoryEvents = 10000;

  constructor(configDir?: string) {
    const dir = configDir || path.join(os.homedir(), '.jep-guard');
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    this.streamPath = path.join(dir, 'audit-stream.jep');
    this.load();
  }

  async emit(event: JPEvent): Promise<void> {
    this.events.push(event);

    // Rotate if too many in memory
    if (this.events.length > this.maxMemoryEvents) {
      this.events = this.events.slice(-this.maxMemoryEvents / 2);
    }

    const line = JSON.stringify(event) + '\n';
    fs.appendFileSync(this.streamPath, line, { mode: 0o600 });
  }

  async query(filter: AuditFilter): Promise<JPEvent[]> {
    return this.events.filter(e => {
      if (filter.since && e.when * 1000 < filter.since.getTime()) return false;
      if (filter.agent && e.who !== filter.agent) return false;
      if (filter.verb && e.verb !== filter.verb) return false;
      return true;
    });
  }

  export(format: 'jep' | 'json' = 'jep'): string {
    if (format === 'jep') {
      return JSON.stringify({ events: this.events }, null, 2);
    }
    return JSON.stringify(this.events, null, 2);
  }

  stats(): { total: number; byVerb: Record<string, number>; sizeBytes: number } {
    const byVerb: Record<string, number> = {};
    for (const e of this.events) {
      byVerb[e.verb] = (byVerb[e.verb] || 0) + 1;
    }
    return {
      total: this.events.length,
      byVerb,
      sizeBytes: fs.existsSync(this.streamPath) ? fs.statSync(this.streamPath).size : 0
    };
  }

  private load(): void {
    if (!fs.existsSync(this.streamPath)) return;

    const lines = fs.readFileSync(this.streamPath, 'utf-8').split('\n').filter(Boolean);
    // Only load last N events to memory
    const recent = lines.slice(-this.maxMemoryEvents);
    for (const line of recent) {
      try { this.events.push(JSON.parse(line)); } catch {}
    }
  }
}