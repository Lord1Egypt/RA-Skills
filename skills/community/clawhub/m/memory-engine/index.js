"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = register;
const memory_engine_1 = require("./memory-engine");
// Debug mode toggle - controlled by MEMORY_ENGINE_DEBUG env variable
const DEBUG_MODE = process.env.MEMORY_ENGINE_DEBUG === 'true' || process.env.MEMORY_ENGINE_DEBUG === '1';
// Conditional debug logging
const debugLog = (...args) => {
    if (DEBUG_MODE) {
        console.log('[memory-engine]', ...args);
    }
};
function getDefaultDbPath() {
    return `${process.env.HOME || process.env.USERPROFILE}/.openclaw/memory/memories.db`;
}
// 单例引擎实例
let globalEngine = null;
let enginePromise = null;
class MemoryEngineContextEngine {
    config = {};
    embeddingCache = new Map();
    maxEmbeddingCacheSize = 1000;
    recallTopK = 5;
    memoryFetchLimit = 100;
    similarityThreshold = 0.3;
    semanticThreshold = 0.35;
    storeMinLength = 6;
    dedupSimilarityThreshold = 0.92;
    stats = {
        searches: 0,
        hits: 0,
        totalSearchMs: 0,
        lastSearchMs: 0
    };
    cleanupEnabled = false;
    cleanupMaxAgeDays = 90;
    cleanupMinImportance = 0.4;
    setConfig(config) {
        this.config = config || {};
        this.maxEmbeddingCacheSize = this.resolveNumber(this.config.embeddingCacheSize, Number(process.env.MEMORY_ENGINE_EMBED_CACHE_SIZE || 1000));
        this.recallTopK = this.resolveNumber(this.config.recallTopK, Number(process.env.MEMORY_ENGINE_RECALL_TOPK || 5));
        this.memoryFetchLimit = this.resolveNumber(this.config.memoryFetchLimit, Number(process.env.MEMORY_ENGINE_MEMORY_LIMIT || 100));
        this.similarityThreshold = this.resolveNumber(this.config.similarityThreshold, Number(process.env.MEMORY_ENGINE_SIM_THRESHOLD || 0.3));
        this.semanticThreshold = this.resolveNumber(this.config.semanticThreshold, Number(process.env.MEMORY_ENGINE_SEM_THRESHOLD || 0.35));
        this.storeMinLength = this.resolveNumber(this.config.storeMinLength, Number(process.env.MEMORY_ENGINE_STORE_MIN_LEN || 6));
        this.dedupSimilarityThreshold = this.resolveNumber(this.config.dedupSimilarityThreshold, Number(process.env.MEMORY_ENGINE_DEDUP_SIM || 0.92));
        this.cleanupEnabled = this.resolveBoolean(this.config.cleanupEnabled, process.env.MEMORY_ENGINE_CLEANUP_ENABLED === '1');
        this.cleanupMaxAgeDays = this.resolveNumber(this.config.cleanupMaxAgeDays, Number(process.env.MEMORY_ENGINE_CLEANUP_MAX_DAYS || 90));
        this.cleanupMinImportance = this.resolveNumber(this.config.cleanupMinImportance, Number(process.env.MEMORY_ENGINE_CLEANUP_MIN_IMPORTANCE || 0.4));
    }
    resolveBoolean(value, fallback) {
        if (value === undefined || value === null || value === '')
            return fallback;
        if (typeof value === 'boolean')
            return value;
        if (typeof value === 'string')
            return value === '1' || value.toLowerCase() === 'true';
        return Boolean(value);
    }
    resolveNumber(value, fallback) {
        if (value === undefined || value === null || value === '')
            return fallback;
        const n = Number(value);
        return Number.isFinite(n) ? n : fallback;
    }
    async getCachedEmbedding(cacheKey, text, embeddingModel) {
        if (this.embeddingCache.has(cacheKey)) {
            return this.embeddingCache.get(cacheKey);
        }
        const embedding = await embeddingModel.getEmbedding(text);
        this.embeddingCache.set(cacheKey, embedding);
        if (this.embeddingCache.size > this.maxEmbeddingCacheSize) {
            const firstKey = this.embeddingCache.keys().next().value;
            if (firstKey)
                this.embeddingCache.delete(firstKey);
        }
        return embedding;
    }
    // 获取引擎（单例模式，避免重复初始化）
    async getEngine() {
        if (globalEngine)
            return globalEngine;
        if (enginePromise)
            return enginePromise;
        debugLog('🔧 Creating engine...');
        const dbPath = this.config.dbPath || process.env.MEMORY_ENGINE_DB_PATH || getDefaultDbPath();
        enginePromise = (0, memory_engine_1.createMemoryEngine)({
            dbPath,
            enableCompression: true,
            maxMessages: 50,
            keepRecentCount: 10
        });
        globalEngine = await enginePromise;
        debugLog('✅ Engine created');
        return globalEngine;
    }
    // 提取用户文本内容
    extractUserContent(message) {
        if (typeof message.content === 'string')
            return message.content;
        if (Array.isArray(message.content)) {
            for (const item of message.content) {
                if (item?.type === 'text' && item?.text)
                    return item.text;
            }
        }
        return '';
    }
    //处理 untrusted metadata，提取真实内容
    processUntrustedMetadata(content) {
        if (!content)
            return '';
        if (content.includes('untrusted metadata')) {
            const lines = content.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
            if (lines.length > 0)
                return lines[lines.length - 1];
        }
        return content;
    }
    // 每轮对话后处理
    async afterTurn(params) {
        debugLog('📥 After turn:', params.messages.length, 'messages');
        const engine = await this.getEngine();
        // 获取所有用户消息
        const userMsgs = params.messages.filter((m) => m?.role === 'user');
        for (const userMsg of userMsgs) {
            let content = this.extractUserContent(userMsg);
            content = this.processUntrustedMetadata(content);
            if (!content || content.length < 3)
                continue;
            if (!this.shouldStoreMemory(content))
                continue;
            debugLog('📝 User content:', content.substring(0, 50));
            const knowledge = await engine.extractKnowledge(content, 'user');
            if (knowledge && knowledge.shouldExtract) {
                try {
                    const extractor = engine.extractor;
                    const embeddingModel = extractor.embeddingModel;
                    const embedding = await this.getCachedEmbedding(`m:new:${knowledge.content}`, knowledge.content, embeddingModel);
                    const isDup = await this.isNearDuplicate(engine, embeddingModel, embedding);
                    if (isDup) {
                        debugLog('ℹ️ Skip near-duplicate memory');
                        continue;
                    }
                    await engine.addMemory({
                        content: knowledge.content,
                        type: knowledge.knowledgeType,
                        importance: knowledge.importance,
                        tags: knowledge.tags,
                        metadata: knowledge.metadata,
                        embedding
                    });
                    debugLog('💾 Knowledge saved:', knowledge.knowledgeType);
                }
                catch (error) {
                    console.error('[memory-engine] ❌ Failed to save:', error);
                }
            }
        }
        if (this.cleanupEnabled) {
            try {
                const archived = engine.archiveOldMemories(this.cleanupMaxAgeDays, this.cleanupMinImportance);
                if (archived > 0)
                    debugLog('🧹 Archived memories:', archived);
            }
            catch (e) {
                console.error('[memory-engine] ❌ Cleanup failed:', e);
            }
        }
        return {
            processed: true,
            // OpenClaw可能期望的格式
            totalTokens: 0,
            tokenEstimate: 0
        };
    }
    //组装上下文
    async assemble(params) {
        debugLog('🔍 assemble 被调用', {
            sessionId: params.sessionId,
            messagesCount: params.messages?.length,
            hasMessages: !!params.messages,
            isArray: Array.isArray(params.messages),
            tokenBudget: params.tokenBudget
        });
        if (!params.messages || !Array.isArray(params.messages)) {
            console.error('[memory-engine] ❌ params.messages 无效');
            return {
                system: '[Memory Engine]\n',
                messages: [],
                tokenEstimate: 0,
                totalTokens: 0
            };
        }
        const engine = await this.getEngine();
        let systemPromptAddition = '';
        let activeRecallPrompts = [];
        const lastUser = params.messages.filter((m) => m?.role === 'user').pop();
        if (lastUser) {
            let userContent = this.extractUserContent(lastUser);
            userContent = this.processUntrustedMetadata(userContent);
            debugLog('🔍 Checking if should search:', userContent.substring(0, 30));
            const shouldSearch = await this.shouldSearchMemories(userContent);
            debugLog('🔍 shouldSearch结果:', shouldSearch);
            if (shouldSearch) {
                debugLog('🔍 使用 embedding进行语义搜索...');
                try {
                    const { systemPromptAddition: addition, activeRecallPrompts: prompts } = await this.searchMemoriesForContext(engine, userContent);
                    systemPromptAddition = addition;
                    activeRecallPrompts = prompts;
                }
                catch (error) {
                    console.error('[memory-engine] ❌ 搜索失败:', error);
                }
            }
            else {
                debugLog('🔍 跳过搜索 (不需要)');
            }
        }
        // 压缩上下文（如果消息过多）
        let messages = params.messages;
        if (messages.length > 30) {
            debugLog('📦 Compressing context...');
            const safeMessages = messages.map((m) => ({
                role: m.role,
                content: typeof m.content === 'string' ? m.content : JSON.stringify(m.content)
            }));
            const compressed = engine.compressContext(safeMessages);
            messages = compressed.messages.map((m) => ({ role: m.role, content: m.content }));
            debugLog('✅ Compressed from', compressed.originalCount, 'to', compressed.compressedCount, 'messages');
        }
        const system = `[Memory Engine]\n${systemPromptAddition}\n\n${activeRecallPrompts.join('\n')}`;
        const allContent = messages.map((m) => m.content || '').join('') + system;
        const tokenEstimate = Math.ceil(allContent.length / 3);
        const totalTokens = tokenEstimate;
        return {
            system,
            messages,
            tokenEstimate,
            totalTokens,
            systemPromptAddition,
            activeRecallPrompts
        };
    }
    // 判断是否应该搜索记忆（规则 + embedding 混合）
    async shouldSearchMemories(content) {
        const text = (content || '').trim();
        if (text.length < 4)
            return false;
        const quickResult = this.quickRuleCheck(text);
        if (quickResult !== null)
            return quickResult;
        // 短句且无明确意图时不搜索
        if (text.length < 10)
            return false;
        return await this.semanticCheck(text);
    }
    shouldStoreMemory(content) {
        const text = (content || '').trim();
        //过滤寒暄/确认/无意义
        if (/^(你好|您好|嗨|hello|hi|hey|早上好|下午好|晚上好|再见|拜拜)$/.test(text))
            return false;
        if (/^(好的|收到|明白|ok|okay|thanks|谢谢|知道了|嗯+|啊+|哦+)$/.test(text))
            return false;
        // 简单敏感信息过滤（可扩展）
        if (/\b\d{15,}\b/.test(text))
            return false; // 超长数字
        // 偏好类短句直接放行
        if (/(喜欢|爱好|偏好|讨厌)/.test(text))
            return true;
        // 中英文分别计数：中文按字符、英文按单词
        const hasCJK = /[\u4e00-\u9fff]/.test(text);
        if (hasCJK) {
            // 中文：去掉空白后字符数
            const cjkLen = text.replace(/\s+/g, '').length;
            if (cjkLen < this.storeMinLength)
                return false;
        }
        else {
            // 英文：按单词数
            const wordCount = text.split(/\s+/).filter(Boolean).length;
            if (wordCount < Math.max(2, Math.floor(this.storeMinLength / 2)))
                return false;
        }
        return true;
    }
    async isNearDuplicate(engine, embeddingModel, embedding) {
        const recent = await engine.getAllMemories(Math.min(50, this.memoryFetchLimit));
        if (!recent || recent.length === 0)
            return false;
        for (const memory of recent) {
            const existingEmbedding = memory.embedding || await this.getCachedEmbedding(`m:${memory.id}`, memory.content, embeddingModel);
            const similarity = embeddingModel.cosineSimilarity(embedding, existingEmbedding);
            if (similarity >= this.dedupSimilarityThreshold)
                return true;
        }
        return false;
    }
    // 快速规则检查
    quickRuleCheck(content) {
        const compact = content.toLowerCase().replace(/\s+/g, '');
        //纯寒暄/确认/感谢
        if (/^(你好|您好|嗨|hello|hi|hey|早上好|下午好|晚上好|再见|拜拜)$/.test(compact))
            return false;
        if (/^(好的|收到|明白|ok|okay|thanks|谢谢|知道了|嗯+|啊+|哦+)$/.test(compact))
            return false;
        const mustSearch = [
            '什么', '哪儿', '哪里', '如何', '为什么', '怎么', '谁',
            '记得', '之前', '以前', '曾经', '上次', '那次', '你说过', '还记得',
            '我几岁', '我多大', '我叫什么', '我是谁',
            '我喜欢', '喜欢什么', '爱好', '偏好', '习惯',
            '帮我回忆', '回忆', '查询', '搜索', 'history', 'remember', 'lasttime'
        ];
        if (mustSearch.some(k => compact.includes(k))) {
            debugLog('🔍 快速规则:需要搜索 (mustSearch)');
            return true;
        }
        //过短且不含明确触发词，不搜索
        if (compact.length < 6)
            return false;
        return null;
    }
    //语义检查（使用 embedding）
    async semanticCheck(content) {
        try {
            // 若无问句/回忆意图，直接不搜
            const hasQuestionMark = /[?？]/.test(content);
            const hasQuestionWord = /(什么|怎么|为何|为什么|如何|哪|哪儿|哪里|谁|几岁|多大|喜欢|偏好|习惯|记得|之前|曾经|上次|你说过|回忆)/.test(content);
            if (!hasQuestionMark && !hasQuestionWord)
                return false;
            const engine = await this.getEngine();
            const extractor = engine.extractor;
            const embeddingModel = extractor.embeddingModel;
            const userEmbedding = await this.getCachedEmbedding(`q:${content}`, content, embeddingModel);
            const searchIntentEmbedding = await this.getCachedEmbedding('q:intent', '查询记忆搜索', embeddingModel);
            const similarity = embeddingModel.cosineSimilarity(userEmbedding, searchIntentEmbedding);
            debugLog(`🔍语义检查: 相似度 ${similarity.toFixed(3)}`);
            return similarity > this.semanticThreshold;
        }
        catch (error) {
            console.error('[memory-engine] ❌语义检查失败:', error);
            return false;
        }
    }
    async searchMemoriesForContext(engine, userContent) {
        const start = Date.now();
        this.stats.searches += 1;
        const extractor = engine.extractor;
        const embeddingModel = extractor.embeddingModel;
        const queryEmbedding = await this.getCachedEmbedding(`q:${userContent}`, userContent, embeddingModel);
        const allMemories = await engine.getAllMemories(this.memoryFetchLimit);
        debugLog('🔍 获取到记忆数量:', allMemories?.length);
        if (!allMemories || allMemories.length === 0) {
            this.recordSearchStats(start, 0);
            return { systemPromptAddition: '', activeRecallPrompts: [] };
        }
        //先做关键词/tag召回
        const keywordHits = this.keywordRecall(allMemories, userContent);
        const results = await Promise.all(allMemories.map(async (memory) => {
            const memoryKey = memory.id || memory.content;
            const memoryEmbedding = memory.embedding || await this.getCachedEmbedding(`m:${memoryKey}`, memory.content, embeddingModel);
            const similarity = embeddingModel.cosineSimilarity(queryEmbedding, memoryEmbedding);
            const boost = keywordHits.has(memory.id) ? 0.15 : 0;
            return { memory, similarity: similarity + boost };
        }));
        const filteredResults = results
            .filter(r => r.similarity > this.similarityThreshold)
            .sort((a, b) => b.similarity - a.similarity)
            .slice(0, this.recallTopK);
        debugLog('🔍 找到', filteredResults.length, '条相关记忆');
        if (filteredResults.length === 0) {
            this.recordSearchStats(start, 0);
            return { systemPromptAddition: '', activeRecallPrompts: [] };
        }
        const grouped = this.groupByType(filteredResults.map(r => r.memory));
        const memoryTexts = this.buildMemoryText(grouped);
        if (!memoryTexts) {
            this.recordSearchStats(start, 0);
            return { systemPromptAddition: '', activeRecallPrompts: [] };
        }
        const systemPromptAddition = `\n\n[相关记忆]\n${memoryTexts}`;
        const activeRecallPrompts = [
            '根据你的记忆，这个问题可能与之前的经验相关。',
            '你之前遇到过类似的情况，可以参考以下经验。'
        ];
        this.recordSearchStats(start, filteredResults.length);
        return { systemPromptAddition, activeRecallPrompts };
    }
    keywordRecall(memories, userContent) {
        const hits = new Set();
        const text = userContent.toLowerCase();
        const keywordTags = [
            { tag: 'preference', keywords: ['喜欢', '爱好', '偏好', '讨厌'] },
            { tag: 'food', keywords: ['鱼', '虾', '肉', '菜', '饭', '面', '汤', '水果', '甜点', '披萨', '汉堡'] },
            { tag: 'skill', keywords: ['擅长', '精通', '会', '懂', '编程', '代码'] },
            { tag: 'experience', keywords: ['之前', '曾经', '那次', '经历过', '遇到过'] }
        ];
        const matchedTags = new Set();
        for (const item of keywordTags) {
            if (item.keywords.some(k => text.includes(k)))
                matchedTags.add(item.tag);
        }
        for (const memory of memories) {
            const tags = (memory.tags || []);
            if (tags.some(t => matchedTags.has(t))) {
                hits.add(memory.id);
                continue;
            }
            if (memory.content && text.length > 0) {
                const contentLower = String(memory.content).toLowerCase();
                if (this.simpleOverlap(contentLower, text))
                    hits.add(memory.id);
            }
        }
        return hits;
    }
    simpleOverlap(a, b) {
        const tokens = b.split(/\s+/).filter(Boolean).slice(0, 6);
        return tokens.some(t => t.length >= 2 && a.includes(t));
    }
    groupByType(memories) {
        const groups = {};
        for (const m of memories) {
            const t = m.type || 'fact';
            if (!groups[t])
                groups[t] = [];
            groups[t].push(m);
        }
        return groups;
    }
    buildMemoryText(grouped) {
        const order = ['fact', 'preference', 'skill', 'experience', 'lesson'];
        const lines = [];
        for (const t of order) {
            const arr = grouped[t] || [];
            if (arr.length === 0)
                continue;
            for (const m of arr) {
                if (!m.content)
                    continue;
                lines.push(`- ${m.content}`);
                if (lines.length >= this.recallTopK)
                    break;
            }
            if (lines.length >= this.recallTopK)
                break;
        }
        return lines.join('\n');
    }
    recordSearchStats(start, hitCount) {
        const cost = Date.now() - start;
        this.stats.lastSearchMs = cost;
        this.stats.totalSearchMs += cost;
        if (hitCount > 0)
            this.stats.hits += 1;
    }
    // 压缩上下文（OpenClaw hook）
    async compact(_params) {
        debugLog('📦 Compacting context...');
        debugLog('✅ Context compacted');
    }
    // 获取统计信息
    async getStats() {
        const engine = await this.getEngine();
        const base = engine.getStatistics();
        return {
            ...base,
            memoryEngine: {
                searches: this.stats.searches,
                hits: this.stats.hits,
                hitRate: this.stats.searches ? Number((this.stats.hits / this.stats.searches).toFixed(3)) : 0,
                avgSearchMs: this.stats.searches ? Number((this.stats.totalSearchMs / this.stats.searches).toFixed(2)) : 0,
                lastSearchMs: this.stats.lastSearchMs
            }
        };
    }
    //处理 dispose
    async dispose() {
        debugLog('Dispose (keeping engine alive)');
    }
}
// 创建上下文引擎实例
const contextEngine = new MemoryEngineContextEngine();
// 导出注册函数
function register(api) {
    // 注册上下文引擎
    api.registerContextEngine('memory-engine', () => contextEngine);
    //读取插件配置（如有）
    if (api?.getConfig) {
        try {
            const cfg = api.getConfig('memory-engine') || api.getConfig() || {};
            contextEngine.setConfig(cfg);
        }
        catch (e) {
            console.error('[memory-engine] ❌读取配置失败:', e);
        }
    }
    // 注册 memory_save 工具
    api.registerTool(() => ({
        name: 'memory_save',
        description: '保存重要信息到记忆系统',
        parameters: {
            type: 'object',
            properties: {
                content: { type: 'string', description: '要记忆的内容' },
                type: {
                    type: 'string',
                    enum: ['fact', 'experience', 'lesson', 'preference', 'skill'],
                    description: '记忆类型'
                },
                importance: {
                    type: 'number',
                    minimum: 0,
                    maximum: 1,
                    description: '重要性0-1'
                },
                tags: {
                    type: 'array',
                    items: { type: 'string' },
                    description: '标签数组'
                }
            },
            required: ['content']
        },
        execute: async (params) => {
            const engine = await contextEngine.getEngine();
            const knowledge = await engine.extractKnowledge(params.content || '', 'user');
            const tags = params.tags || knowledge?.tags || [];
            const result = await engine.addMemory({
                content: params.content || '',
                type: params.type || 'fact',
                importance: params.importance || 0.8,
                tags: tags
            });
            return { success: !!result, memory: result };
        }
    }), { names: ['memory_save'] });
    // 注册 memory_search 工具
    api.registerTool(() => ({
        name: 'memory_search',
        description: '搜索记忆',
        parameters: {
            type: 'object',
            properties: {
                query: { type: 'string', description: '搜索关键字' },
                limit: { type: 'number', default: 5, description: '返回数量' }
            },
            required: ['query']
        },
        execute: async (params) => {
            const engine = await contextEngine.getEngine();
            const results = await engine.searchMemories(params.query, {
                limit: params.limit || 5
            });
            return { results };
        }
    }), { names: ['memory_search'] });
    // 注册 memory_list 工具
    api.registerTool(() => ({
        name: 'memory_list',
        description: '列出所有记忆',
        parameters: {
            type: 'object',
            properties: {
                type: {
                    type: 'string',
                    enum: ['fact', 'experience', 'lesson', 'preference', 'skill'],
                    description: '记忆类型过滤'
                },
                limit: { type: 'number', default: 20, description: '返回数量' }
            }
        },
        execute: async (params) => {
            const engine = await contextEngine.getEngine();
            const memories = await engine.getAllMemories(params.limit || 20);
            return { memories };
        }
    }), { names: ['memory_list'] });
    // 注册 memory_stats 工具
    api.registerTool(() => ({
        name: 'memory_stats',
        description: '获取记忆统计',
        parameters: {
            type: 'object',
            properties: {}
        },
        execute: async () => {
            const engine = await contextEngine.getEngine();
            const stats = await engine.getStatistics();
            return { stats };
        }
    }), { names: ['memory_stats'] });
    debugLog('✅ All tools registered');
}
//# sourceMappingURL=index.js.map