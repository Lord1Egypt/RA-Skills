/**
 * 变更日志 —— per-agent 环形缓冲，用于"撤销上一步"
 *
 * 设计要点：
 *   - 只记录"可逆的 write"：记录 write 前的字段快照 + write 的新值，
 *     undo 时把旧值写回去。
 *   - 不记录 create / unlink：create 的"撤销"在 Odoo 上是 unlink（不安全，
 *     可能触发级联），unlink 的"撤销"需要 restore（不一定存在）。这两类
 *     通过 active=false 软删/恢复实现，但语义外部明确，不走 undo 路径。
 *   - 环形缓冲：超过 maxEntries 丢掉最旧的一条。
 *   - 存储：JSON 文件在 ~/.openclaw/plugin-configs/odoo/{agentId}.ops.log.json
 *   - 并发：单进程 best-effort 同步写；per-agent 文件隔离，冲突窗口很窄，
 *     再说 undo 是低频操作，不上锁。
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

export interface MutationEntry {
  id: string;
  timestamp: number;
  tool: string;                      // e.g. "odoo_update_task", "odoo_bulk_update"
  model: string;                     // e.g. "project.task"
  ids: number[];                     // 受影响记录的 id 列表
  before: Record<string, unknown>[]; // per-id 变更前快照，顺序与 ids 对应
  after: Record<string, unknown>;    // write 时传入的新值
  reversible: boolean;               // 只有捕获到 before 快照时才算可逆
  undone: boolean;
  summary: string;                   // 供用户确认用的一行描述
}

export interface MutationLogOptions {
  maxEntries?: number;
  baseDir?: string;
}

export class MutationLog {
  private readonly maxEntries: number;
  private readonly baseDir: string;

  constructor(options: MutationLogOptions = {}) {
    this.maxEntries = options.maxEntries ?? 50;
    this.baseDir = options.baseDir ?? join(homedir(), '.openclaw', 'plugin-configs', 'odoo');
  }

  private logPath(agentId: string): string {
    return join(this.baseDir, `${agentId}.ops.log.json`);
  }

  private load(agentId: string): MutationEntry[] {
    const path = this.logPath(agentId);
    if (!existsSync(path)) return [];
    try {
      const raw = readFileSync(path, 'utf8');
      const parsed = JSON.parse(raw) as unknown;
      if (Array.isArray(parsed)) return parsed as MutationEntry[];
      return [];
    } catch {
      return [];
    }
  }

  private save(agentId: string, entries: MutationEntry[]): void {
    if (!existsSync(this.baseDir)) mkdirSync(this.baseDir, { recursive: true });
    const trimmed = entries.slice(-this.maxEntries);
    writeFileSync(this.logPath(agentId), JSON.stringify(trimmed, null, 2), 'utf8');
  }

  /** 追加一条变更日志 */
  append(agentId: string, entry: Omit<MutationEntry, 'id' | 'timestamp' | 'undone'>): MutationEntry {
    const full: MutationEntry = {
      ...entry,
      id: `m_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`,
      timestamp: Date.now(),
      undone: false,
    };
    const entries = this.load(agentId);
    entries.push(full);
    this.save(agentId, entries);
    return full;
  }

  /** 列出最近的 N 条（最新在前），可选只显示可撤销的 */
  list(agentId: string, options: { limit?: number; reversibleOnly?: boolean; includeUndone?: boolean } = {}): MutationEntry[] {
    const entries = this.load(agentId);
    let filtered = entries;
    if (options.reversibleOnly) filtered = filtered.filter(e => e.reversible);
    if (!options.includeUndone) filtered = filtered.filter(e => !e.undone);
    filtered = filtered.slice().reverse();
    if (options.limit) filtered = filtered.slice(0, options.limit);
    return filtered;
  }

  /** 找最后一条可撤销条目（最新优先） */
  findLastReversible(agentId: string): MutationEntry | null {
    const entries = this.load(agentId);
    for (let i = entries.length - 1; i >= 0; i--) {
      const e = entries[i]!;
      if (e.reversible && !e.undone) return e;
    }
    return null;
  }

  /** 标记某条已撤销（写回旧值后调用） */
  markUndone(agentId: string, entryId: string): void {
    const entries = this.load(agentId);
    const found = entries.find(e => e.id === entryId);
    if (!found) return;
    found.undone = true;
    this.save(agentId, entries);
  }

  /** 清空日志（调试/测试用） */
  clear(agentId: string): void {
    this.save(agentId, []);
  }
}

/** 共享单例（足够，因为 per-agent 文件已经隔离了） */
export const mutationLog = new MutationLog();
