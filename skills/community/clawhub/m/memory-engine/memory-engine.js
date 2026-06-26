"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MemoryEngine = void 0;
exports.createMemoryEngine = createMemoryEngine;
// 核心引擎
const store_1 = require("./store");
const extractor_1 = require("./extractor");
const compressor_1 = require("./compressor");
// Debug mode toggle
const DEBUG_MODE = process.env.MEMORY_ENGINE_DEBUG === 'true' || process.env.MEMORY_ENGINE_DEBUG === '1';
const debugLog = (...args) => {
    if (DEBUG_MODE) {
        console.log('[memory-engine]', ...args);
    }
};
class MemoryEngine {
    store;
    extractor;
    compressor;
    initialized = false;
    embeddingModel; // EmbeddingModel 类型
    constructor(config = {}) {
        const dbPath = config.dbPath || ':memory:';
        this.store = new store_1.Store(dbPath);
        this.extractor = new extractor_1.KnowledgeExtractor();
        this.compressor = new compressor_1.ContextCompressor();
        if (config.keepRecentCount) {
            this.compressor.setKeepRecentCount(config.keepRecentCount);
        }
        this.compressor.setEnableCompression(config.enableCompression !== false);
    }
    // 初始化引擎
    async initialize() {
        if (this.initialized)
            return;
        await this.store.initialize();
        await this.extractor.initialize();
        this.initialized = true;
        debugLog('✅ Engine initialized');
    }
    // 检查是否初始化
    isInitialized() {
        return this.initialized;
    }
    // 添加记忆
    async addMemory(input) {
        const record = this.store.create(input);
        if (!record) {
            debugLog('ℹ️ Memory already exists, skipped');
            return null;
        }
        debugLog('💾 Memory saved:', record.content.substring(0, 30));
        return record;
    }
    // 搜索记忆
    async searchMemories(query, options) {
        const searchOptions = {
            query,
            limit: options?.limit || 10,
            status: 'active',
            ...options
        };
        const memories = this.store.search(searchOptions);
        return memories.map(memory => ({
            memory,
            score: memory.importance || 0.5
        }));
    }
    // 获取所有记忆
    async getAllMemories(limit = 50) {
        return this.store.getAllMemories(limit);
    }
    // 提取知识
    async extractKnowledge(content, messageType = 'user') {
        if (messageType === 'user') {
            return await this.extractor.extractFromUserMessage(content);
        }
        return this.extractor.extractFromAIMessage(content);
    }
    // 从对话对提取知识
    async extractFromConversationPair(userMessage, aiMessage) {
        return await this.extractor.extractFromConversationPair(userMessage, aiMessage);
    }
    // 压缩上下文
    compressContext(messages) {
        return this.compressor.compress(messages);
    }
    // 获取上下文（带压缩）
    getContext(messages, _tokenBudget) {
        const result = this.compressContext(messages);
        return this.compressor.getPreservedMessages(result.messages);
    }
    // 获取统计信息
    getStatistics() {
        return this.store.getStats();
    }
    //归档旧记忆
    archiveOldMemories(maxAgeDays, minImportance) {
        return this.store.archiveOldMemories(maxAgeDays, minImportance);
    }
    //关闭引擎
    async shutdown() {
        if (this.store) {
            this.store.close();
        }
        debugLog('✅ Engine shutdown');
    }
}
exports.MemoryEngine = MemoryEngine;
// 创建引擎实例
async function createMemoryEngine(config = {}) {
    const engine = new MemoryEngine(config);
    await engine.initialize();
    return engine;
}
//# sourceMappingURL=memory-engine.js.map