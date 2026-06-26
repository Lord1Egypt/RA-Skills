"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Store = void 0;
// Debug mode toggle
const DEBUG_MODE = process.env.MEMORY_ENGINE_DEBUG === 'true' || process.env.MEMORY_ENGINE_DEBUG === '1';
const debugLog = (...args) => {
    if (DEBUG_MODE) {
        console.log('[memory-engine]', ...args);
    }
};
class Store {
    dbPath;
    db;
    initialized = false;
    constructor(dbPath = ':memory:') {
        this.dbPath = dbPath;
    }
    async initialize() {
        if (this.initialized)
            return;
        try {
            const Database = require('better-sqlite3');
            this.db = new Database(this.dbPath);
            this.db.exec(`
 CREATE TABLE IF NOT EXISTS memories (
 id TEXT PRIMARY KEY,
 content TEXT NOT NULL,
 type TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'active',
 importance REAL NOT NULL DEFAULT 0.5,
 tags TEXT,
 userId TEXT,
 agentId TEXT,
 createdAt INTEGER NOT NULL,
 updatedAt INTEGER NOT NULL,
 accessedAt INTEGER NOT NULL,
 accessCount INTEGER NOT NULL DEFAULT 0,
 version INTEGER NOT NULL DEFAULT 1,
 metadata TEXT,
 embedding TEXT
 );
 
 CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
 CREATE INDEX IF NOT EXISTS idx_memories_status ON memories(status);
 CREATE INDEX IF NOT EXISTS idx_memories_createdAt ON memories(createdAt);
 CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories(tags);
 `);
            //兼容旧库：尝试添加 embedding 列
            try {
                this.db.exec(`ALTER TABLE memories ADD COLUMN embedding TEXT`);
            }
            catch (_) { }
            this.initialized = true;
            debugLog('✅ Store initialized (better-sqlite3)');
        }
        catch (error) {
            console.error('[memory-engine] ❌ Store initialization failed:', error);
            throw error;
        }
    }
    // 创建记忆
    create(input) {
        const contentStr = String(input.content || '').trim();
        if (!contentStr) {
            debugLog('ℹ️ Empty content, skipping');
            return null;
        }
        const existing = this.db.prepare('SELECT id FROM memories WHERE content = ? AND status = ?').get(contentStr, 'active');
        if (existing) {
            debugLog('ℹ️ Memory already exists, skipping:', contentStr.substring(0, 30));
            return null;
        }
        const record = {
            id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            content: contentStr,
            type: input.type || 'fact',
            status: 'active',
            importance: input.importance || 0.5,
            tags: input.tags || [],
            userId: input.userId,
            agentId: input.agentId,
            createdAt: Date.now(),
            updatedAt: Date.now(),
            accessedAt: Date.now(),
            accessCount: 0,
            version: 1,
            metadata: input.metadata,
            embedding: input.embedding
        };
        const stmt = this.db.prepare(`
 INSERT INTO memories (id, content, type, status, importance, tags, userId, agentId, createdAt, updatedAt, accessedAt, accessCount, version, metadata, embedding)
 VALUES (@id, @content, @type, @status, @importance, @tags, @userId, @agentId, @createdAt, @updatedAt, @accessedAt, @accessCount, @version, @metadata, @embedding)
 `);
        stmt.run({
            ...record,
            tags: JSON.stringify(record.tags),
            metadata: record.metadata ? JSON.stringify(record.metadata) : null,
            embedding: record.embedding ? JSON.stringify(record.embedding) : null
        });
        return record;
    }
    // 搜索记忆
    search(options) {
        let query = 'SELECT * FROM memories WHERE status = @status';
        const params = { status: options.status || 'active' };
        if (options.userId) {
            query += ' AND userId = @userId';
            params.userId = options.userId;
        }
        if (options.type) {
            query += ' AND type = @type';
            params.type = options.type;
        }
        if (options.tags && options.tags.length > 0) {
            const tagConditions = options.tags.map((tag, i) => {
                params[`tag${i}`] = `%${tag}%`;
                return `tags LIKE @tag${i}`;
            });
            query += ` AND (${tagConditions.join(' OR ')})`;
        }
        if (options.query && options.query.trim()) {
            query += ' AND content LIKE @query';
            params.query = `%${options.query}%`;
        }
        query += ' ORDER BY createdAt DESC, importance DESC';
        if (options.limit) {
            query += ' LIMIT @limit';
            params.limit = options.limit;
        }
        if (options.offset) {
            query += ' OFFSET @offset';
            params.offset = options.offset;
        }
        const rows = this.db.prepare(query).all(params);
        return rows.map((row) => ({
            ...row,
            tags: row.tags ? JSON.parse(row.tags) : [],
            metadata: row.metadata ? JSON.parse(row.metadata) : undefined,
            embedding: row.embedding ? JSON.parse(row.embedding) : undefined
        }));
    }
    // 获取单个记忆
    getById(id) {
        const row = this.db.prepare('SELECT * FROM memories WHERE id = @id').get({ id });
        if (!row)
            return null;
        return {
            ...row,
            tags: row.tags ? JSON.parse(row.tags) : [],
            metadata: row.metadata ? JSON.parse(row.metadata) : undefined,
            embedding: row.embedding ? JSON.parse(row.embedding) : undefined
        };
    }
    // 更新记忆
    update(id, updates) {
        const existing = this.getById(id);
        if (!existing)
            return null;
        const updated = { ...existing, ...updates, updatedAt: Date.now() };
        const stmt = this.db.prepare(`
 UPDATE memories
 SET content = @content, type = @type, status = @status, importance = @importance,
 tags = @tags, accessedAt = @accessedAt, accessCount = @accessCount, version = @version, metadata = @metadata, embedding = @embedding
 WHERE id = @id
 `);
        stmt.run({
            ...updated,
            tags: JSON.stringify(updated.tags),
            metadata: updated.metadata ? JSON.stringify(updated.metadata) : null,
            embedding: updated.embedding ? JSON.stringify(updated.embedding) : null
        });
        return updated;
    }
    // 删除记忆（软删除）
    delete(id) {
        const result = this.db.prepare('UPDATE memories SET status = @status WHERE id = @id').run({
            id,
            status: 'archived'
        });
        return result.changes > 0;
    }
    //归档旧记忆
    archiveOldMemories(maxAgeDays, minImportance) {
        const cutoff = Date.now() - maxAgeDays * 24 * 60 * 60 * 1000;
        const stmt = this.db.prepare(`
 UPDATE memories
 SET status = 'archived'
 WHERE status = 'active'
 AND importance < @minImportance
 AND updatedAt < @cutoff
 `);
        const result = stmt.run({ minImportance, cutoff });
        return result.changes || 0;
    }
    // 获取所有记忆
    getAllMemories(limit = 50) {
        return this.search({ limit });
    }
    // 获取统计信息
    getStats() {
        if (!this.db)
            return { totalCount: 0, activeCount: 0, byType: {} };
        const total = this.db.prepare('SELECT COUNT(*) as count FROM memories WHERE status = @status').get({ status: 'active' });
        const byType = this.db.prepare('SELECT type, COUNT(*) as count FROM memories WHERE status = @status GROUP BY type').all({ status: 'active' });
        return {
            totalCount: total.count,
            activeCount: total.count,
            byType: byType.reduce((acc, row) => { acc[row.type] = row.count; return acc; }, {})
        };
    }
    //关闭数据库
    close() {
        if (this.db) {
            this.db.close();
        }
    }
}
exports.Store = Store;
//# sourceMappingURL=store.js.map