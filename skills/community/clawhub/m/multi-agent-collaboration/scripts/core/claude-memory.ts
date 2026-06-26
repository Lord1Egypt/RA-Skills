import * as fs from 'fs';
import * as path from 'path';

export type ClaudeMemoryKind = 'identity' | 'correction' | 'task' | 'project' | 'reference';

export interface ClaudeMemoryEntry {
  id: string;
  kind: ClaudeMemoryKind;
  summary: string;
  content: string;
  tags: string[];
  importance: number;
  createdAt: string;
  updatedAt: string;
  source: 'user' | 'assistant' | 'system';
}

export class ClaudeMemorySystem {
  private storePath: string;
  private entries: ClaudeMemoryEntry[] = [];

  constructor(baseDir: string = 'memory', namespace: string = 'claude_grade') {
    const root = path.join(baseDir, namespace);
    if (!fs.existsSync(root)) fs.mkdirSync(root, { recursive: true });
    this.storePath = path.join(root, 'claude_memory.json');
    this.load();
  }

  addMemory(kind: ClaudeMemoryKind, summary: string, content: string, options?: {
    tags?: string[];
    importance?: number;
    source?: 'user' | 'assistant' | 'system';
  }): ClaudeMemoryEntry {
    const now = new Date().toISOString();
    const entry: ClaudeMemoryEntry = {
      id: `mem_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      kind,
      summary,
      content,
      tags: options?.tags || [],
      importance: options?.importance ?? 0.7,
      createdAt: now,
      updatedAt: now,
      source: options?.source || 'user'
    };
    this.entries.push(entry);
    this.save();
    return entry;
  }

  retrieve(query: string, topK: number = 5): Array<{ entry: ClaudeMemoryEntry; score: number; reasons: string[] }> {
    const tokens = Array.from(new Set(query.toLowerCase().split(/[^a-z0-9\u4e00-\u9fa5]+/).filter(Boolean)));
    return this.entries
      .map((entry) => {
        const haystack = `${entry.summary} ${entry.content} ${entry.tags.join(' ')}`.toLowerCase();
        let score = entry.importance * 10;
        const reasons: string[] = [];
        for (const token of tokens) {
          if (haystack.includes(token)) {
            score += 3;
            reasons.push(`token:${token}`);
          }
        }
        return { entry, score, reasons };
      })
      .filter((m) => m.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  backgroundExtract(turnText: string): ClaudeMemoryEntry[] {
    const created: ClaudeMemoryEntry[] = [];
    const rules: Array<{ re: RegExp; kind: ClaudeMemoryKind; summary: string; importance: number; tags: string[] }> = [
      { re: /我叫|我是|称呼我|你可以叫我/, kind: 'identity', summary: 'User identity preference', importance: 0.95, tags: ['identity'] },
      { re: /不要|别再|应该|必须|纠正/, kind: 'correction', summary: 'User correction or hard preference', importance: 1.0, tags: ['correction'] },
      { re: /正在做|现在要|接下来做|当前任务/, kind: 'task', summary: 'Current task state', importance: 0.9, tags: ['task'] },
      { re: /项目|仓库|代码库|目录|工作目录/, kind: 'project', summary: 'Project-level fact', importance: 0.85, tags: ['project'] },
      { re: /参考|资料|文档|源码/, kind: 'reference', summary: 'Reference location', importance: 0.8, tags: ['reference'] }
    ];
    for (const rule of rules) {
      if (!rule.re.test(turnText)) continue;
      created.push(this.addMemory(rule.kind, rule.summary, turnText, { importance: rule.importance, tags: rule.tags }));
    }
    return created;
  }

  formatRetrievedContext(query: string, topK: number = 5): string {
    const matches = this.retrieve(query, topK);
    if (matches.length === 0) return 'No relevant memory found.';
    return matches.map((m, i) => `${i + 1}. [${m.entry.kind}] ${m.entry.summary}: ${m.entry.content}`).join('\n');
  }

  getStats(): Record<string, number> {
    return this.entries.reduce<Record<string, number>>((acc, entry) => {
      acc.total = (acc.total || 0) + 1;
      acc[entry.kind] = (acc[entry.kind] || 0) + 1;
      return acc;
    }, {});
  }

  private load(): void {
    if (!fs.existsSync(this.storePath)) return;
    this.entries = JSON.parse(fs.readFileSync(this.storePath, 'utf8'));
  }

  private save(): void {
    fs.writeFileSync(this.storePath, JSON.stringify(this.entries, null, 2), 'utf8');
  }
}

export default ClaudeMemorySystem;
