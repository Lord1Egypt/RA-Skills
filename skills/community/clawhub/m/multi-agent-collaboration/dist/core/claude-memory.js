"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ClaudeMemorySystem = void 0;
const fs = require("fs");
const path = require("path");
class ClaudeMemorySystem {
    constructor(baseDir = 'memory', namespace = 'claude_grade') {
        this.entries = [];
        const root = path.join(baseDir, namespace);
        if (!fs.existsSync(root)) {
            fs.mkdirSync(root, { recursive: true });
        }
        this.storePath = path.join(root, 'claude_memory.json');
        this.load();
    }
    addMemory(kind, summary, content, options) {
        const now = new Date().toISOString();
        const entry = {
            id: `mem_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
            kind,
            summary,
            content,
            tags: (options === null || options === void 0 ? void 0 : options.tags) || [],
            importance: (options === null || options === void 0 ? void 0 : options.importance) !== undefined ? options.importance : 0.7,
            createdAt: now,
            updatedAt: now,
            source: (options === null || options === void 0 ? void 0 : options.source) || 'user'
        };
        this.entries.push(entry);
        this.save();
        return entry;
    }
    retrieve(query, topK = 5) {
        const tokens = this.tokenize(query);
        return this.entries
            .map((entry) => this.scoreEntry(entry, tokens))
            .filter((match) => match.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, topK);
    }
    backgroundExtract(turnText) {
        const created = [];
        const text = turnText.trim();
        if (!text)
            return created;
        const rules = [
            { test: (v) => /我叫|我是|称呼我|你可以叫我/.test(v), kind: 'identity', summary: 'User identity preference', importance: 0.95, tags: ['identity', 'user-profile'] },
            { test: (v) => /不要|别再|应该|必须|你上次错在|纠正/.test(v), kind: 'correction', summary: 'User correction or hard preference', importance: 1.0, tags: ['correction', 'guardrail'] },
            { test: (v) => /正在做|现在要|接下来做|当前任务/.test(v), kind: 'task', summary: 'Current task state', importance: 0.9, tags: ['task', 'active-work'] },
            { test: (v) => /项目|仓库|代码库|目录|工作目录/.test(v), kind: 'project', summary: 'Project-level fact', importance: 0.85, tags: ['project', 'workspace'] },
            { test: (v) => /参考|资料|文档|去看|在.*里面|源码里/.test(v), kind: 'reference', summary: 'Reference location', importance: 0.8, tags: ['reference', 'lookup'] }
        ];
        for (const rule of rules) {
            if (!rule.test(text))
                continue;
            created.push(this.addMemory(rule.kind, rule.summary, text, {
                importance: rule.importance,
                tags: rule.tags,
                source: 'user'
            }));
        }
        return created;
    }
    formatRetrievedContext(query, topK = 5) {
        const matches = this.retrieve(query, topK);
        if (matches.length === 0) {
            return 'No relevant memory found.';
        }
        return matches
            .map((match, index) => `${index + 1}. [${match.entry.kind}] ${match.entry.summary}: ${match.entry.content}`)
            .join('\n');
    }
    getStats() {
        return this.entries.reduce((acc, entry) => {
            acc.total += 1;
            acc[entry.kind] = (acc[entry.kind] || 0) + 1;
            return acc;
        }, { total: 0 });
    }
    tokenize(input) {
        return Array.from(new Set(input
            .toLowerCase()
            .split(/[^a-z0-9\u4e00-\u9fa5]+/)
            .map((v) => v.trim())
            .filter(Boolean)));
    }
    scoreEntry(entry, queryTokens) {
        const haystack = `${entry.summary} ${entry.content} ${entry.tags.join(' ')}`.toLowerCase();
        let score = entry.importance * 10;
        const reasons = [];
        for (const token of queryTokens) {
            if (haystack.includes(token)) {
                score += 3;
                reasons.push(`token:${token}`);
            }
        }
        const kindBonus = { identity: 1.2, correction: 1.4, task: 1.1, project: 1.05, reference: 1.0 };
        score *= kindBonus[entry.kind];
        return { entry, score, reasons };
    }
    load() {
        if (!fs.existsSync(this.storePath)) {
            this.entries = [];
            return;
        }
        this.entries = JSON.parse(fs.readFileSync(this.storePath, 'utf8'));
    }
    save() {
        fs.writeFileSync(this.storePath, JSON.stringify(this.entries, null, 2), 'utf8');
    }
}
exports.ClaudeMemorySystem = ClaudeMemorySystem;
exports.default = ClaudeMemorySystem;
