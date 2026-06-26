/**
 * EO Proactive Memory Manager v1.0.0
 *
 * Inspired by Claude Code's memdir.ts and memoryTypes.ts
 * Handles proactive memory saving and loading for session continuity.
 *
 * Key features:
 * - Session-end: proactively distill key info to MEMORY.md + topics/
 * - Session-start: load relevant memories using semantic search
 * - Four memory types: user, feedback, project, reference
 * - MEMORY.md truncation (200 lines / 25KB)
 */
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
// ============================================================================
// Constants (mirrors Claude Code's memdir.ts)
// ============================================================================
export const ENTRYPOINT_NAME = 'MEMORY.md';
export const MAX_ENTRYPOINT_LINES = 200;
export const MAX_ENTRYPOINT_BYTES = 25_000;
export const TOPICS_DIR = 'topics';
export const MEMORY_DIR = 'memory';
// ============================================================================
// Memory Types (mirrors Claude Code's memoryTypes.ts)
// ============================================================================
export const MEMORY_TYPES = ['user', 'feedback', 'project', 'reference'];
// ============================================================================
// Memory Manager Class
// ============================================================================
export class ProactiveMemoryManager {
    workspace;
    constructor(workspace) {
        this.workspace = workspace;
    }
    /**
     * Get the memory directory path
     */
    getMemoryDir() {
        return path.join(this.workspace, MEMORY_DIR);
    }
    /**
     * Get the topics directory path
     */
    getTopicsDir() {
        return path.join(this.getMemoryDir(), TOPICS_DIR);
    }
    /**
     * Ensure memory directory structure exists
     */
    ensureMemoryStructure() {
        const memDir = this.getMemoryDir();
        const topicsDir = this.getTopicsDir();
        if (!fs.existsSync(memDir)) {
            fs.mkdirSync(memDir, { recursive: true });
        }
        if (!fs.existsSync(topicsDir)) {
            fs.mkdirSync(topicsDir, { recursive: true });
        }
    }
    // ===========================================================================
    // Session-End: Save Memory
    // ===========================================================================
    /**
     * Extract key information from session messages and save to memory
     */
    async distillSessionMemory(sessionId, messages) {
        this.ensureMemoryStructure();
        const entries = this.categorizeMessages(messages);
        const saved = [];
        const skipped = [];
        for (const entry of entries) {
            try {
                const fileName = this.generateMemoryFileName(entry.type, entry.title);
                const filePath = path.join(this.getTopicsDir(), fileName);
                await this.saveMemoryEntry(filePath, entry);
                saved.push(fileName);
                // Update MEMORY.md index
                await this.updateMemoryIndex(fileName, entry.title, entry.description, entry.type);
            }
            catch (e) {
                skipped.push(entry.title);
            }
        }
        return { saved, skipped, total: entries.length };
    }
    /**
     * Categorize session messages into memory types
     */
    categorizeMessages(messages) {
        const candidates = [];
        for (const msg of messages) {
            const content = msg.content || '';
            // User role/preference mentions
            if (this.matchesPattern(content, /\b(I'm|I am|a|an)\s+\w+\s+(developer|engineer|scientist|manager|designer|researcher)/i)) {
                candidates.push({
                    type: 'user',
                    title: this.extractTitle(content, 50),
                    description: this.summarize(content),
                    content: content,
                });
            }
            // Feedback/corrections
            if (this.matchesPattern(content, /\b(don't|stop|don't do|no not|avoid|don't use|never)\b/i) ||
                this.matchesPattern(content, /\b(yes exactly|perfect|right call|keep doing)/i)) {
                candidates.push({
                    type: 'feedback',
                    title: this.extractTitle(content, 50),
                    description: this.summarize(content),
                    content: content,
                });
            }
            // Project state/decisions
            if (this.matchesPattern(content, /\b(freeze|deadline|launch|release|merge|shipping|cutting|planned)/i)) {
                candidates.push({
                    type: 'project',
                    title: this.extractTitle(content, 50),
                    description: this.summarize(content),
                    content: content,
                });
            }
            // External references
            if (this.matchesPattern(content, /\b(Linear|Slack|Grafana|Jira|Notion|Confluence|dashboard|tracker)/i)) {
                candidates.push({
                    type: 'reference',
                    title: this.extractTitle(content, 50),
                    description: this.summarize(content),
                    content: content,
                });
            }
        }
        return candidates;
    }
    matchesPattern(content, pattern) {
        return pattern.test(content);
    }
    extractTitle(content, maxLen) {
        const firstLine = content.split('\n')[0].trim();
        return firstLine.length > maxLen ? firstLine.substring(0, maxLen) + '...' : firstLine;
    }
    summarize(content) {
        // Simple summarization - take first 150 chars
        const cleaned = content.replace(/\n+/g, ' ').trim();
        return cleaned.length > 150 ? cleaned.substring(0, 150) + '...' : cleaned;
    }
    generateMemoryFileName(type, title) {
        const safeTitle = title
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '')
            .substring(0, 40);
        const timestamp = new Date().toISOString().slice(0, 10);
        return `${type}-${safeTitle}-${timestamp}.md`;
    }
    /**
     * Save a memory entry to a topic file
     */
    async saveMemoryEntry(filePath, entry) {
        const now = new Date().toISOString().slice(0, 10);
        const frontmatter = {
            name: entry.title,
            description: entry.description,
            type: entry.type,
            created: now,
            updated: now,
        };
        const content = [
            '---',
            ...Object.entries(frontmatter).map(([k, v]) => `${k}: ${v}`),
            '---',
            '',
            entry.content,
        ].join('\n');
        fs.writeFileSync(filePath, content, 'utf-8');
    }
    /**
     * Update MEMORY.md index with new memory entry
     */
    async updateMemoryIndex(fileName, title, description, type) {
        const indexPath = path.join(this.getMemoryDir(), ENTRYPOINT_NAME);
        const entryLine = `- [${title}](${TOPICS_DIR}/${fileName}) — ${description} [${type}]`;
        let existingContent = '';
        try {
            existingContent = fs.readFileSync(indexPath, 'utf-8');
        }
        catch {
            // Index doesn't exist, start fresh
            existingContent = '';
        }
        // Check for duplicate
        if (existingContent.includes(fileName)) {
            return; // Already indexed
        }
        // Append entry
        const newContent = existingContent.trim()
            ? `${existingContent}\n${entryLine}`
            : entryLine;
        // Truncate if needed
        const truncated = this.truncateIndex(newContent);
        fs.writeFileSync(indexPath, truncated.content, 'utf-8');
    }
    // ===========================================================================
    // Session-Start: Load Memory
    // ===========================================================================
    /**
     * Load all relevant memories for the current session
     */
    async loadRelevantMemories(query) {
        this.ensureMemoryStructure();
        const indexPath = path.join(this.getMemoryDir(), ENTRYPOINT_NAME);
        let indexContent = '';
        try {
            indexContent = fs.readFileSync(indexPath, 'utf-8');
        }
        catch {
            return { memories: [], indexLoaded: false, truncated: false };
        }
        // Check if index was truncated
        const { wasLineTruncated, wasByteTruncated } = this.truncateIndex(indexContent);
        const truncated = wasLineTruncated || wasByteTruncated;
        // Parse index entries
        const entries = this.parseIndexEntries(indexContent);
        // If query provided, filter by relevance
        const relevant = query
            ? this.filterByRelevance(entries, query)
            : entries.slice(0, 5); // Default: load up to 5 recent memories
        // Load topic file contents
        const memories = [];
        for (const entry of relevant) {
            try {
                const filePath = path.join(this.getMemoryDir(), entry.filePath);
                const content = fs.readFileSync(filePath, 'utf-8');
                memories.push({
                    ...entry,
                    content,
                    loaded: true,
                });
            }
            catch {
                memories.push({
                    ...entry,
                    content: '',
                    loaded: false,
                });
            }
        }
        return {
            memories,
            indexLoaded: true,
            truncated,
            totalIndexed: entries.length,
        };
    }
    /**
     * Parse MEMORY.md index entries
     */
    parseIndexEntries(content) {
        const entries = [];
        const lines = content.split('\n');
        for (const line of lines) {
            const match = line.match(/^- \[(.+?)\]\((.+?)\)\s*—?\s*(.+?)\s*\[(\w+)\]$/);
            if (match) {
                entries.push({
                    title: match[1],
                    filePath: match[2],
                    description: match[3],
                    type: match[4],
                });
            }
        }
        return entries;
    }
    /**
     * Filter entries by relevance to query
     */
    filterByRelevance(entries, query) {
        const queryLower = query.toLowerCase();
        const queryWords = queryLower.split(/\s+/);
        return entries
            .map(entry => {
            const text = `${entry.title} ${entry.description} ${entry.type}`.toLowerCase();
            let score = 0;
            for (const word of queryWords) {
                if (text.includes(word))
                    score++;
            }
            return { entry, score };
        })
            .filter(({ score }) => score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, 5)
            .map(({ entry }) => entry);
    }
    // ===========================================================================
    // Truncation (mirrors Claude Code's truncateEntrypointContent)
    // ===========================================================================
    /**
     * Truncate MEMORY.md content to line AND byte caps
     */
    truncateIndex(content) {
        const trimmed = content.trim();
        const contentLines = trimmed.split('\n');
        const lineCount = contentLines.length;
        const byteCount = trimmed.length;
        const wasLineTruncated = lineCount > MAX_ENTRYPOINT_LINES;
        const wasByteTruncated = byteCount > MAX_ENTRYPOINT_BYTES;
        if (!wasLineTruncated && !wasByteTruncated) {
            return { content: trimmed, wasLineTruncated: false, wasByteTruncated: false };
        }
        let truncated = wasLineTruncated
            ? contentLines.slice(0, MAX_ENTRYPOINT_LINES).join('\n')
            : trimmed;
        if (truncated.length > MAX_ENTRYPOINT_BYTES) {
            const cutAt = truncated.lastIndexOf('\n', MAX_ENTRYPOINT_BYTES);
            truncated = truncated.slice(0, cutAt > 0 ? cutAt : MAX_ENTRYPOINT_BYTES);
        }
        const reason = wasByteTruncated && !wasLineTruncated
            ? `${this.formatBytes(byteCount)} (limit: ${this.formatBytes(MAX_ENTRYPOINT_BYTES)})`
            : wasLineTruncated && !wasByteTruncated
                ? `${lineCount} lines (limit: ${MAX_ENTRYPOINT_LINES})`
                : `${lineCount} lines and ${this.formatBytes(byteCount)}`;
        return {
            content: truncated + `\n\n> WARNING: ${ENTRYPOINT_NAME} truncated (${reason}). Keep index concise.`,
            wasLineTruncated,
            wasByteTruncated,
        };
    }
    formatBytes(bytes) {
        if (bytes < 1024)
            return `${bytes}B`;
        if (bytes < 1024 * 1024)
            return `${(bytes / 1024).toFixed(1)}KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
    }
    // ===========================================================================
    // Memory Statistics
    // ===========================================================================
    /**
     * Get memory system statistics
     */
    getMemoryStats() {
        this.ensureMemoryStructure();
        const topicsDir = this.getTopicsDir();
        let topicCount = 0;
        let totalSize = 0;
        if (fs.existsSync(topicsDir)) {
            const files = fs.readdirSync(topicsDir).filter(f => f.endsWith('.md'));
            topicCount = files.length;
            for (const file of files) {
                const stat = fs.statSync(path.join(topicsDir, file));
                totalSize += stat.size;
            }
        }
        const indexPath = path.join(this.getMemoryDir(), ENTRYPOINT_NAME);
        let indexSize = 0;
        let indexLines = 0;
        try {
            const indexContent = fs.readFileSync(indexPath, 'utf-8');
            indexSize = Buffer.byteLength(indexContent, 'utf-8');
            indexLines = indexContent.split('\n').length;
        }
        catch { }
        return {
            topicCount,
            totalSize,
            indexSize,
            indexLines,
            truncated: indexLines > MAX_ENTRYPOINT_LINES || indexSize > MAX_ENTRYPOINT_BYTES,
        };
    }
}
// ============================================================================
// Export singleton factory
// ============================================================================
export function createMemoryManager(workspace) {
    return new ProactiveMemoryManager(workspace);
}
//# sourceMappingURL=proactive-memory-manager.js.map