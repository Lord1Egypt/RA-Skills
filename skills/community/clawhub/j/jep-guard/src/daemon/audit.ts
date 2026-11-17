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
    this.events.push(JSON.parse(JSON.stringify(event)));

    // Rotate if too many in memory
    if (this.events.length > this.maxMemoryEvents) {
      this.events = this.events.slice(-this.maxMemoryEvents / 2);
    }

    const line = JSON.stringify(event) + '\n';
    const fd=fs.openSync(this.streamPath,fs.constants.O_WRONLY|fs.constants.O_APPEND|fs.constants.O_CREAT|fs.constants.O_NOFOLLOW,0o600);
    try { if(fs.fstatSync(fd).size+Buffer.byteLength(line)>16777216) throw new Error('Archive audit log before continuing'); fs.writeSync(fd,line); } finally {fs.closeSync(fd);}
  }

  async query(filter: AuditFilter): Promise<JPEvent[]> {
    return this.events.filter(e => {
      if (filter.since && e.when * 1000 < filter.since.getTime()) return false;
      if (filter.agent && e.who !== filter.agent) return false;
      if (filter.verb && e.verb !== filter.verb) return false;
      return true;
    });
  }

  export(format: 'jep' | 'json' = 'jep', events: JPEvent[] = this.events): string {
    if (format === 'jep') {
      return JSON.stringify({ events }, null, 2);
    }
    return JSON.stringify(events, null, 2);
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

    const stat=fs.lstatSync(this.streamPath);
    if(stat.isSymbolicLink() || (stat.mode&0o077) || stat.size>16777216) throw new Error('Audit file needs secure archival before startup');
    const lines = fs.readFileSync(this.streamPath, 'utf-8').split('\n').filter(Boolean);
    // Only load last N events to memory
    const recent = lines.slice(-this.maxMemoryEvents);
    for (const line of recent) {
      try { this.events.push(JSON.parse(line)); } catch {}
    }
  }
}