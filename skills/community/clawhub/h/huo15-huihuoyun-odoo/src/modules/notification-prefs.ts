/**
 * 每 agent 通知偏好 —— 持久化 + 默认值 + 过滤判定
 *
 * 与 ConfigManager 同一个目录体系（~/.openclaw/plugin-configs/odoo/），
 * 但文件名加 `.prefs.json` 后缀，不与凭据混在同一文件里。
 *
 * 过滤发生在 Odoo 插件一侧（生产者），bus 依然无感知。
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';
import type {
  NotificationPreferences,
  NotificationKind,
  NotificationPriority,
  NotificationEnvelope,
} from '../types/index.js';

const CONFIG_BASE = '.openclaw/plugin-configs/odoo';

function sanitize(agentId: string): string {
  return agentId.replace(/[^a-zA-Z0-9_\-]/g, '_').substring(0, 128) || 'default';
}

export const DEFAULT_PREFS: NotificationPreferences = {
  enabled: true,
  kinds: [],            // 空 = 全放行
  minPriority: 'low',   // 全通过
  updatedAt: 0,
};

const PRIORITY_RANK: Record<NotificationPriority, number> = {
  low: 0,
  normal: 1,
  high: 2,
  urgent: 3,
};

export class PrefsManager {
  private baseDir: string;

  constructor(homeDir: string = process.env['HOME'] ?? '/root') {
    this.baseDir = join(homeDir, CONFIG_BASE);
  }

  private pathFor(agentId: string): string {
    return join(this.baseDir, `${sanitize(agentId)}.prefs.json`);
  }

  load(agentId: string = 'default'): NotificationPreferences {
    try {
      const p = this.pathFor(agentId);
      if (!existsSync(p)) return { ...DEFAULT_PREFS };
      const parsed = JSON.parse(readFileSync(p, 'utf-8')) as Partial<NotificationPreferences>;
      return { ...DEFAULT_PREFS, ...parsed };
    } catch {
      return { ...DEFAULT_PREFS };
    }
  }

  save(prefs: NotificationPreferences, agentId: string = 'default'): boolean {
    try {
      if (!existsSync(this.baseDir)) mkdirSync(this.baseDir, { recursive: true });
      writeFileSync(
        this.pathFor(agentId),
        JSON.stringify({ ...prefs, updatedAt: Date.now() }, null, 2),
        'utf-8',
      );
      return true;
    } catch {
      return false;
    }
  }

  patch(
    partial: Partial<NotificationPreferences>,
    agentId: string = 'default',
  ): NotificationPreferences {
    const merged: NotificationPreferences = { ...this.load(agentId), ...partial, updatedAt: Date.now() };
    this.save(merged, agentId);
    return merged;
  }

  clear(agentId: string = 'default'): boolean {
    try {
      const p = this.pathFor(agentId);
      if (existsSync(p)) unlinkSync(p);
      return true;
    } catch {
      return false;
    }
  }
}

/**
 * 判断 envelope 在给定偏好下是否应该发出。
 *
 * 使用纯函数便于测试；调用方自己决定是否 log 拒绝原因。
 */
export function shouldDeliver(
  envelope: NotificationEnvelope,
  prefs: NotificationPreferences,
  now: Date = new Date(),
): { deliver: boolean; reason?: string } {
  if (!prefs.enabled) return { deliver: false, reason: 'notifications disabled' };

  if (prefs.kinds.length > 0 && !prefs.kinds.includes(envelope.kind as NotificationKind)) {
    return { deliver: false, reason: `kind ${envelope.kind} not in allowlist` };
  }

  if (PRIORITY_RANK[envelope.priority] < PRIORITY_RANK[prefs.minPriority]) {
    // urgent 级别永远放行（强行突破静音/优先级过滤）
    if (envelope.priority !== 'urgent') {
      return { deliver: false, reason: `priority ${envelope.priority} below ${prefs.minPriority}` };
    }
  }

  if (prefs.quietHours && inQuietHours(prefs.quietHours, now) && envelope.priority !== 'urgent') {
    return { deliver: false, reason: 'within quiet hours' };
  }

  return { deliver: true };
}

function parseHHMM(s: string): number | null {
  const m = /^(\d{1,2}):(\d{2})$/.exec(s.trim());
  if (!m) return null;
  const h = Number(m[1]);
  const mi = Number(m[2]);
  if (Number.isNaN(h) || Number.isNaN(mi) || h > 23 || mi > 59) return null;
  return h * 60 + mi;
}

/** 支持跨午夜：start=22:00 end=08:00 代表 22:00~次日 08:00 */
export function inQuietHours(
  window: { start: string; end: string },
  now: Date = new Date(),
): boolean {
  const start = parseHHMM(window.start);
  const end = parseHHMM(window.end);
  if (start === null || end === null) return false;
  const cur = now.getHours() * 60 + now.getMinutes();
  return start <= end
    ? cur >= start && cur < end
    : cur >= start || cur < end;
}
