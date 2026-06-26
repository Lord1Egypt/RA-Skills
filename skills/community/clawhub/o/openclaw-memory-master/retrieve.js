"use strict";
/**
 * Memory Retriever v4.1 - 增强版记忆检索
 *
 * 基于 Generative Agents + Mem0 + MemoryBank 最佳实践
 *
 * 新增功能：
 * - 重要性评分（近因 + 重要性 + 相关性）
 * - 情感维度（情感类型 + 情感强度）
 * - 动态 Top-K 优化
 * - 混合检索（语义 + 关键词 + 时间）
 *
 * @author 小鬼 👻 + Jake
 * @version 4.1.0
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.MemoryRetrieverV41 = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
/**
 * 增强版记忆检索器
 */
class MemoryRetrieverV41 {
    constructor(memoryDir = 'memory') {
        this.indexCache = new Map();
        this.memoryDir = memoryDir;
    }
    /**
     * 检索记忆（增强版）
     */
    async retrieve(query, options = {}) {
        const { type = 'factual', limit = 5, recencyWeight = 0.3, importanceWeight = 0.5, relevanceWeight = 0.2, emotion, minEmotionIntensity, dynamicK = false, minK = 3, maxK = 10, startTime, endTime, hybridSearch = false, keywordBoost = 1.5, } = options;
        // 1. 加载记忆
        const memories = await this.loadMemories();
        // 2. 过滤（时间/情感/类型）
        let filtered = this.filterMemories(memories, {
            type,
            startTime,
            endTime,
            emotion,
            minEmotionIntensity,
        });
        // 3. 计算评分
        const scored = this.calculateScores(filtered, query, {
            recencyWeight,
            importanceWeight,
            relevanceWeight,
            hybridSearch,
            keywordBoost,
        });
        // 4. 排序
        scored.sort((a, b) => (b.combinedScore || 0) - (a.combinedScore || 0));
        // 5. 动态 Top-K（参考 Mem0）
        const finalLimit = dynamicK
            ? this.calculateDynamicK(scored, minK, maxK)
            : limit;
        const topMemories = scored.slice(0, finalLimit);
        // 6. 统计信息
        const stats = this.calculateStats(topMemories);
        return {
            memories: topMemories,
            total: filtered.length,
            query,
            searchType: type,
            scores: stats.scores,
            emotions: stats.emotions,
        };
    }
    /**
     * 加载记忆
     */
    async loadMemories() {
        // 检查缓存
        if (this.indexCache.has('all')) {
            return this.indexCache.get('all');
        }
        const memories = [];
        const memoryDir = path.join(process.cwd(), this.memoryDir);
        // 加载 MEMORY.md
        const memoryFile = path.join(memoryDir, 'MEMORY.md');
        if (fs.existsSync(memoryFile)) {
            const content = fs.readFileSync(memoryFile, 'utf-8');
            const parsed = this.parseMemoryMd(content);
            memories.push(...parsed);
        }
        // 加载 daily memory
        const dailyDir = path.join(memoryDir, 'daily');
        if (fs.existsSync(dailyDir)) {
            const files = fs.readdirSync(dailyDir).filter(f => f.endsWith('.md'));
            for (const file of files) {
                const filePath = path.join(dailyDir, file);
                const content = fs.readFileSync(filePath, 'utf-8');
                const parsed = this.parseDailyMemory(content, file);
                memories.push(...parsed);
            }
        }
        // 加载 wiki memory（v4.1 新增）
        const wikiDir = path.join(memoryDir, 'wiki');
        if (fs.existsSync(wikiDir)) {
            const files = fs.readdirSync(wikiDir).filter(f => f.endsWith('.md'));
            for (const file of files) {
                const filePath = path.join(wikiDir, file);
                const content = fs.readFileSync(filePath, 'utf-8');
                const parsed = this.parseWikiMemory(content, file);
                memories.push(...parsed);
            }
        }
        // 缓存
        this.indexCache.set('all', memories);
        return memories;
    }
    /**
     * 过滤记忆
     */
    filterMemories(memories, filters) {
        return memories.filter(memory => {
            // 时间过滤
            if (filters.startTime && memory.timestamp < filters.startTime) {
                return false;
            }
            if (filters.endTime && memory.timestamp > filters.endTime) {
                return false;
            }
            // 情感过滤（v4.1 新增）
            if (filters.emotion && memory.metadata?.emotion !== filters.emotion) {
                return false;
            }
            if (filters.minEmotionIntensity &&
                (memory.metadata?.emotionIntensity || 0) < filters.minEmotionIntensity) {
                return false;
            }
            return true;
        });
    }
    /**
     * 计算评分（参考 Generative Agents）
     */
    calculateScores(memories, query, options) {
        const now = Date.now();
        const oneDay = 24 * 60 * 60 * 1000;
        const oneWeek = 7 * oneDay;
        const oneMonth = 30 * oneDay;
        return memories.map(memory => {
            // 1. 近因评分（Recency）- 指数衰减
            const age = now - memory.timestamp;
            let recencyScore;
            if (age < oneDay) {
                recencyScore = 1.0;
            }
            else if (age < oneWeek) {
                recencyScore = 0.8;
            }
            else if (age < oneMonth) {
                recencyScore = 0.5;
            }
            else {
                recencyScore = 0.3;
            }
            // 2. 重要性评分（Importance）
            const importanceScore = memory.metadata?.importance || 3;
            // 3. 相关性评分（Relevance）- 简单关键词匹配
            let relevanceScore = 0;
            const queryWords = query.toLowerCase().split(/\s+/);
            const content = memory.content.toLowerCase();
            for (const word of queryWords) {
                if (word.length > 2 && content.includes(word)) {
                    relevanceScore += 1;
                }
            }
            relevanceScore = Math.min(relevanceScore / queryWords.length, 1.0);
            // 混合检索增强（v4.1 新增）
            if (options.hybridSearch && relevanceScore > 0) {
                relevanceScore *= options.keywordBoost;
            }
            // 4. 综合评分
            const combinedScore = recencyScore * options.recencyWeight +
                (importanceScore / 5) * options.importanceWeight +
                relevanceScore * options.relevanceWeight;
            return {
                ...memory,
                recencyScore,
                importanceScore,
                relevanceScore,
                combinedScore,
            };
        });
    }
    /**
     * 动态 Top-K（参考 Mem0）
     */
    calculateDynamicK(memories, minK, maxK) {
        if (memories.length === 0) {
            return minK;
        }
        // 计算评分分布
        const scores = memories.map(m => m.combinedScore || 0);
        const maxScore = Math.max(...scores);
        const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
        // 动态调整 K 值
        // 如果最高分远高于平均分，说明有明确答案，返回较少结果
        // 如果分数分布均匀，说明需要更多上下文，返回较多结果
        const ratio = maxScore / (avgScore || 0.1);
        if (ratio > 2) {
            // 明确答案
            return Math.max(minK, Math.floor(maxK * 0.3));
        }
        else if (ratio > 1.5) {
            // 中等明确
            return Math.max(minK, Math.floor(maxK * 0.5));
        }
        else {
            // 需要更多上下文
            return maxK;
        }
    }
    /**
     * 计算统计信息
     */
    calculateStats(memories) {
        const scores = {
            avgRecency: 0,
            avgImportance: 0,
            avgRelevance: 0,
        };
        const emotions = {
            positive: 0,
            negative: 0,
            neutral: 0,
        };
        if (memories.length === 0) {
            return { scores, emotions };
        }
        // 计算平均评分
        scores.avgRecency = memories.reduce((sum, m) => sum + (m.recencyScore || 0), 0) / memories.length;
        scores.avgImportance = memories.reduce((sum, m) => sum + (m.importanceScore || 0), 0) / memories.length;
        scores.avgRelevance = memories.reduce((sum, m) => sum + (m.relevanceScore || 0), 0) / memories.length;
        // 统计情感分布（v4.1 新增）
        for (const memory of memories) {
            const emotion = memory.metadata?.emotion;
            if (emotion) {
                if (['positive', 'joy', 'surprise'].includes(emotion)) {
                    emotions.positive++;
                }
                else if (['negative', 'sadness', 'anger', 'fear', 'disgust'].includes(emotion)) {
                    emotions.negative++;
                }
                else {
                    emotions.neutral++;
                }
            }
        }
        return { scores, emotions };
    }
    /**
     * 解析 MEMORY.md
     */
    parseMemoryMd(content) {
        const memories = [];
        const sections = content.split(/^(## |### )/gm);
        let currentSection = '';
        let currentId = '';
        let currentContent = '';
        for (const section of sections) {
            if (section.startsWith('## ') || section.startsWith('### ')) {
                // 保存上一个记忆
                if (currentId && currentContent) {
                    memories.push({
                        id: currentId,
                        content: currentContent.trim(),
                        type: '语义',
                        timestamp: Date.now(),
                        metadata: {
                            importance: 4,
                        },
                    });
                }
                currentSection = section.trim();
                currentId = this.extractId(section);
                currentContent = '';
            }
            else {
                currentContent += section;
            }
        }
        // 保存最后一个记忆
        if (currentId && currentContent) {
            memories.push({
                id: currentId,
                content: currentContent.trim(),
                type: '语义',
                timestamp: Date.now(),
                metadata: {
                    importance: 4,
                },
            });
        }
        return memories;
    }
    /**
     * 解析每日记忆
     */
    parseDailyMemory(content, filename) {
        const memories = [];
        const date = filename.replace('.md', '');
        const timestamp = new Date(date).getTime();
        const lines = content.split('\n');
        let currentId = '';
        let currentContent = '';
        for (const line of lines) {
            if (line.startsWith('**ID**:')) {
                // 保存上一个记忆
                if (currentId && currentContent) {
                    memories.push({
                        id: currentId,
                        content: currentContent.trim(),
                        type: '情景',
                        timestamp,
                        metadata: {
                            importance: 3,
                        },
                    });
                }
                currentId = line.replace('**ID**:', '').trim();
                currentContent = '';
            }
            else if (currentId) {
                currentContent += line + '\n';
            }
        }
        // 保存最后一个记忆
        if (currentId && currentContent) {
            memories.push({
                id: currentId,
                content: currentContent.trim(),
                type: '情景',
                timestamp,
                metadata: {
                    importance: 3,
                },
            });
        }
        return memories;
    }
    /**
     * 解析 Wiki 记忆（v4.1 新增）
     */
    parseWikiMemory(content, filename) {
        const memories = [];
        const type = filename.replace('.md', '');
        const sections = content.split(/^## /gm);
        for (const section of sections) {
            if (section.trim()) {
                const lines = section.split('\n');
                const title = lines[0].trim();
                const content = lines.slice(1).join('\n').trim();
                if (content) {
                    memories.push({
                        id: `wiki_${type}_${title}`,
                        content: `${title}: ${content}`,
                        type: '语义',
                        timestamp: Date.now(),
                        metadata: {
                            importance: 4,
                            tags: [type],
                        },
                    });
                }
            }
        }
        return memories;
    }
    /**
     * 提取 ID
     */
    extractId(text) {
        const match = text.match(/\*\*ID\*\*:\s*(\S+)/);
        return match ? match[1] : `mem_${Date.now()}`;
    }
    /**
     * 检测情感（v4.1 新增，简单实现）
     */
    detectEmotion(content) {
        const positiveWords = ['好', '棒', '优秀', '成功', '开心', '高兴', '喜欢', '爱', '满意', '完美'];
        const negativeWords = ['坏', '差', '失败', '难过', '生气', '讨厌', '恨', '失望', '糟糕', '错误'];
        const contentLower = content.toLowerCase();
        let positiveCount = 0;
        let negativeCount = 0;
        for (const word of positiveWords) {
            if (contentLower.includes(word)) {
                positiveCount++;
            }
        }
        for (const word of negativeWords) {
            if (contentLower.includes(word)) {
                negativeCount++;
            }
        }
        const total = positiveCount + negativeCount;
        if (total === 0) {
            return { emotion: 'neutral', intensity: 1 };
        }
        const intensity = Math.min(5, Math.ceil(total / 3));
        if (positiveCount > negativeCount) {
            return { emotion: 'positive', intensity };
        }
        else if (negativeCount > positiveCount) {
            return { emotion: 'negative', intensity };
        }
        else {
            return { emotion: 'neutral', intensity };
        }
    }
    /**
     * 清除缓存
     */
    clearCache() {
        this.indexCache.clear();
    }
}
exports.MemoryRetrieverV41 = MemoryRetrieverV41;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmV0cmlldmUtdjQxLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vc3JjL3JldHJpZXZlLXY0MS50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUE7Ozs7Ozs7Ozs7Ozs7R0FhRzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBRUgsdUNBQXlCO0FBQ3pCLDJDQUE2QjtBQTBGN0I7O0dBRUc7QUFDSCxNQUFhLGtCQUFrQjtJQUk3QixZQUFZLFlBQW9CLFFBQVE7UUFGaEMsZUFBVSxHQUE4QixJQUFJLEdBQUcsRUFBRSxDQUFDO1FBR3hELElBQUksQ0FBQyxTQUFTLEdBQUcsU0FBUyxDQUFDO0lBQzdCLENBQUM7SUFFRDs7T0FFRztJQUNILEtBQUssQ0FBQyxRQUFRLENBQ1osS0FBYSxFQUNiLFVBQTJCLEVBQUU7UUFFN0IsTUFBTSxFQUNKLElBQUksR0FBRyxTQUFTLEVBQ2hCLEtBQUssR0FBRyxDQUFDLEVBQ1QsYUFBYSxHQUFHLEdBQUcsRUFDbkIsZ0JBQWdCLEdBQUcsR0FBRyxFQUN0QixlQUFlLEdBQUcsR0FBRyxFQUNyQixPQUFPLEVBQ1AsbUJBQW1CLEVBQ25CLFFBQVEsR0FBRyxLQUFLLEVBQ2hCLElBQUksR0FBRyxDQUFDLEVBQ1IsSUFBSSxHQUFHLEVBQUUsRUFDVCxTQUFTLEVBQ1QsT0FBTyxFQUNQLFlBQVksR0FBRyxLQUFLLEVBQ3BCLFlBQVksR0FBRyxHQUFHLEdBQ25CLEdBQUcsT0FBTyxDQUFDO1FBRVosVUFBVTtRQUNWLE1BQU0sUUFBUSxHQUFHLE1BQU0sSUFBSSxDQUFDLFlBQVksRUFBRSxDQUFDO1FBRTNDLGtCQUFrQjtRQUNsQixJQUFJLFFBQVEsR0FBRyxJQUFJLENBQUMsY0FBYyxDQUFDLFFBQVEsRUFBRTtZQUMzQyxJQUFJO1lBQ0osU0FBUztZQUNULE9BQU87WUFDUCxPQUFPO1lBQ1AsbUJBQW1CO1NBQ3BCLENBQUMsQ0FBQztRQUVILFVBQVU7UUFDVixNQUFNLE1BQU0sR0FBRyxJQUFJ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Q0gsQ0FBQztRQUVELE1BQU0sS0FBSyxHQUFHLGFBQWEsR0FBRyxhQUFhLENBQUM7UUFFNUMsSUFBSSxLQUFLLEtBQUssQ0FBQyxFQUFFLENBQUM7WUFDaEIsT0FBTyxFQUFFLE9BQU8sRUFBRSxTQUFTLEVBQUUsU0FBUyxFQUFFLENBQUMsRUFBRSxDQUFDO1FBQzlDLENBQUM7UUFFRCxNQUFNLFNBQVMsR0FBRyxJQUFJLENBQUMsR0FBRyxDQUFDLENBQUMsRUFBRSxJQUFJLENBQUMsSUFBSSxDQUFDLEtBQUssR0FBRyxDQUFDLENBQUMsQ0FBQyxDQUFDO1FBRXBELElBQUksYUFBYSxHQUFHLGFBQWEsRUFBRSxDQUFDO1lBQ2xDLE9BQU8sRUFBRSxPQUFPLEVBQUUsVUFBVSxFQUFFLFNBQVMsRUFBRSxDQUFDO1FBQzVDLENBQUM7YUFBTSxJQUFJLGFBQWEsR0FBRyxhQUFhLEVBQUUsQ0FBQztZQUN6QyxPQUFPLEVBQUUsT0FBTyxFQUFFLFVBQVUsRUFBRSxTQUFTLEVBQUUsQ0FBQztRQUM1QyxDQUFDO2FBQU0sQ0FBQztZQUNOLE9BQU8sRUFBRSxPQUFPLEVBQUUsU0FBUyxFQUFFLFNBQVMsRUFBRSxDQUFDO1FBQzNDLENBQUM7SUFDSCxDQUFDO0lBRUQ7O09BRUc7SUFDSCxVQUFVO1FBQ1IsSUFBSSxDQUFDLFVBQVUsQ0FBQyxLQUFLLEVBQUUsQ0FBQztJQUMxQixDQUFDO0NBQ0Y7QUE5ZUQsZ0RBOGVDIiwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBNZW1vcnkgUmV0cmlldmVyIHY0LjEgLSDlop7lvLrniYjorrDlv4bmo4DntKJcbiAqIFxuICog5Z+65LqOIEdlbmVyYXRpdmUgQWdlbnRzICsgTWVtMCArIE1lbW9yeUJhbmsg5pyA5L2z5a6e6Le1XG4gKiBcbiAqIOaWsOWinuWKn+iDve+8mlxuICogLSDph43opoHmgKfor4TliIbvvIjov5Hlm6AgKyDph43opoHmgKcgKyDnm7jlhbPmgKfvvIlcbiAqIC0g5oOF5oSf57u05bqm77yI5oOF5oSf57G75Z6LICsg5oOF5oSf5by65bqm77yJXG4gKiAtIOWKqOaAgSBUb3AtSyDkvJjljJZcbiAqIC0g5re35ZCI5qOA57Si77yI6K+t5LmJICsg5YWz6ZSu6K+NICsg5pe26Ze077yJXG4gKiBcbiAqIEBhdXRob3Ig5bCP6ay8IPCfkbsgKyBKYWtlXG4gKiBAdmVyc2lvbiA0LjEuMFxuICovXG5cbmltcG9ydCAqIGFzIGZzIGZyb20gJ2ZzJztcbmltcG9ydCAqIGFzIHBhdGggZnJvbSAncGF0aCc7XG5cbi8qKlxuICog5oOF5oSf57G75Z6LXG4gKi9cbmV4cG9ydCB0eXBlIEVtb3Rpb25UeXBlID0gXG4gIHwgJ3Bvc2l0aXZlJyAgICAvLyDmraPpnaJcbiAgfCAnbmVnYXRpdmUnICAgIC8vIOi0n+mdolxuICB8ICduZXV0cmFsJyAgICAgLy8g5Lit5oCnXG4gIHwgJ2pveScgICAgICAgICAvLyDllpzmgqZcbiAgfCAnc2FkbmVzcycgICAgIC8vIOaCsuS8pFxuICB8ICdhbmdlcicgICAgICAgLy8g5oSk5oCSXG4gIHwgJ3N1cnByaXNlJyAgICAvLyDmg4rorrZcbiAgfCAnZmVhcicgICAgICAgIC8vIOaBkOaDp1xuICB8ICdkaXNndXN0JzsgICAgLy8g5Y6M5oG2XG5cbi8qKlxuICog6K6w5b+G6aG577yI5aKe5by654mI77yJXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgTWVtb3J5SXRlbSB7XG4gIGlkOiBzdHJpbmc7XG4gIGNvbnRlbnQ6IHN0cmluZztcbiAgdHlwZTogJ+aDheaZrycgfCAn6K+t5LmJJyB8ICfnqIvluo8nIHwgJ+S6uuiuvic7XG4gIHRpbWVzdGFtcDogbnVtYmVyO1xuICBtZXRhZGF0YT86IHtcbiAgICB0b3BpYz86IHN0cmluZztcbiAgICBwcm9qZWN0Pzogc3RyaW5nO1xuICAgIGVtb3Rpb24/OiBFbW90aW9uVHlwZTtcbiAgICBlbW90aW9uSW50ZW5zaXR5PzogbnVtYmVyOyAgLy8gMS01XG4gICAgaW1wb3J0YW5jZT86IG51bWJlcjsgICAgICAgIC8vIDEtNVxuICAgIHRhZ3M/OiBzdHJpbmdbXTtcbiAgfTtcbiAgLy8g5qOA57Si6K+E5YiGXG4gIHJlY2VuY3lTY29yZT86IG51bWJlcjsgICAgICAgIC8vIOi/keWboOivhOWIhlxuICBpbXBvcnRhbmNlU2NvcmU/OiBudW1iZXI7ICAgICAvLyDph43opoHmgKfor4TliIZcbiAgcmVsZXZhbmNlU2NvcmU/OiBudW1iZXI7ICAgICAgLy8g55u45YWz5oCn6K+E5YiGXG4gIGNvbWJpbmVkU2NvcmU/OiBudW1iZXI7ICAgICAgIC8vIOe7vOWQiOivhOWIhlxufVxuXG4vKipcbiAqIOajgOe0oumAiemhue+8iOWinuW8uueJiO+8iVxuICovXG5leHBvcnQgaW50ZXJmYWNlIFJldHJpZXZlT3B0aW9ucyB7XG4gIC8vIOWfuuehgOmAiemhuVxuICB0eXBlPzogJ3Byb2NlZHVyYWwnIHwgJ3RlbXBvcmFsJyB8ICdyZWxhdGlvbmFsJyB8ICdwZXJzb25hJyB8ICdmYWN0dWFsJztcbiAgbGltaXQ/OiBudW1iZXI7ICAgICAgICAgICAgICAgLy8g6L+U5Zue5pWw6YeP6ZmQ5Yi2XG4gIFxuICAvLyDor4TliIbmnYPph43vvIjlj4LogIMgR2VuZXJhdGl2ZSBBZ2VudHPvvIlcbiAgcmVjZW5jeVdlaWdodD86IG51bWJlcjsgICAgICAgLy8g6L+R5Zug5p2D6YeN77yI6buY6K6kIDAuM++8iVxuICBpbXBvcnRhbmNlV2VpZ2h0PzogbnVtYmVyOyAgICAvLyDph43opoHmgKfmnYPph43vvIjpu5jorqQgMC4177yJXG4gIHJlbGV2YW5jZVdlaWdodD86IG51bWJlcjsgICAgIC8vIOebuOWFs+aAp+adg+mHje+8iOm7mOiupCAwLjLvvIlcbiAgXG4gIC8vIOaDheaEn+i/h+a7pO+8iOWPguiAgyBNZW1vcnlCYW5r77yJXG4gIGVtb3Rpb24/OiBFbW90aW9uVHlwZTtcbiAgbWluRW1vdGlvbkludGVuc2l0eT86IG51bWJlcjsgLy8g5pyA5bCP5oOF5oSf5by65bqmXG4gIFxuICAvLyBUb3AtSyDkvJjljJbvvIjlj4LogIMgTWVtMO+8iVxuICBkeW5hbWljSz86IGJvb2xlYW47ICAgICAgICAgICAvLyDliqjmgIEgSyDlgLzvvIjpu5jorqQgZmFsc2XvvIlcbiAgbWluSz86IG51bWJlcjsgICAgICAgICAgICAgICAgLy8g5pyA5bCPIEsg5YC877yI6buY6K6kIDPvvIlcbiAgbWF4Sz86IG51bWJlcjsgICAgICAgICAgICAgICAgLy8g5pyA5aSnIEsg5YC877yI6buY6K6kIDEw77yJXG4gIFxuICAvLyDml7bpl7TojIPlm7RcbiAgc3RhcnRUaW1lPzogbnVtYmVyO1xuICBlbmRUaW1lPzogbnVtYmVyO1xuICBcbiAgLy8g5re35ZCI5qOA57SiXG4gIGh5YnJpZFNlYXJjaD86IGJvb2xlYW47ICAgICAgIC8vIOWQr+eUqOa3t+WQiOajgOe0ou+8iOm7mOiupCBmYWxzZe+8iVxuICBrZXl3b3JkQm9vc3Q/OiBudW1iZXI7ICAgICAgICAvLyDlhbPplK7or43mj5DljYflgI3mlbDvvIjpu5jorqQgMS4177yJXG59XG5cbi8qKlxuICog5qOA57Si57uT5p6c77yI5aKe5by654mI77yJXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgUmV0cmlldmVSZXN1bHQge1xuICBtZW1vcmllczogTWVtb3J5SXRlbVtdO1xuICB0b3RhbDogbnVtYmVyO1xuICBxdWVyeT86IHN0cmluZztcbiAgc2VhcmNoVHlwZT86IHN0cmluZztcbiAgc2NvcmVzPzoge1xuICAgIGF2Z1JlY2VuY3k6IG51bWJlcjtcbiAgICBhdmdJbXBvcnRhbmNlOiBudW1iZXI7XG4gICAgYXZnUmVsZXZhbmNlOiBudW1iZXI7XG4gIH07XG4gIGVtb3Rpb25zPzoge1xuICAgIHBvc2l0aXZlOiBudW1iZXI7XG4gICAgbmVnYXRpdmU6IG51bWJlcjtcbiAgICBuZXV0cmFsOiBudW1iZXI7XG4gIH07XG59XG5cbi8qKlxuICog5aKe5by654mI6K6w5b+G5qOA57Si5ZmoXG4gKi9cbmV4cG9ydCBjbGFzcyBNZW1vcnlSZXRyaWV2ZXJWNDEge1xuICBwcml2YXRlIG1lbW9yeURpcjogc3RyaW5nO1xuICBwcml2YXRlIGluZGV4Q2FjaGU6IE1hcDxzdHJpbmcsIE1lbW9yeUl0ZW1bXT4gPSBuZXcgTWFwKCk7XG5cbiAgY29uc3RydWN0b3IobWVtb3J5RGlyOiBzdHJpbmcgPSAnbWVtb3J5Jykge1xuICAgIHRoaXMubWVtb3J5RGlyID0gbWVtb3J5RGlyO1xuICB9XG5cbiAgLyoqXG4gICAqIOajgOe0ouiusOW/hu+8iOWinuW8uueJiO+8iVxuICAgKi9cbiAgYXN5bmMgcmV0cmlldmUoXG4gICAgcXVlcnk6IHN0cmluZyxcbiAgICBvcHRpb25zOiBSZXRyaWV2ZU9wdGlvbnMgPSB7fVxuICApOiBQcm9taXNlPFJldHJpZXZlUmVzdWx0PiB7XG4gICAgY29uc3Qge1xuICAgICAgdHlwZSA9ICdmYWN0dWFsJyxcbiAgICAgIGxpbWl0ID0gNSxcbiAgICAgIHJlY2VuY3lXZWlnaHQgPSAwLjMsXG4gICAgICBpbXBvcnRhbmNlV2VpZ2h0ID0gMC41LFxuICAgICAgcmVsZXZhbmNlV2VpZ2h0ID0gMC4yLFxuICAgICAgZW1vdGlvbixcbiAgICAgIG1pbkVtb3Rpb25JbnRlbnNpdHksXG4gICAgICBkeW5hbWljSyA9IGZhbHNlLFxuICAgICAgbWluSyA9IDMsXG4gICAgICBtYXhLID0gMTAsXG4gICAgICBzdGFydFRpbWUsXG4gICAgICBlbmRUaW1lLFxuICAgICAgaHlicmlkU2VhcmNoID0gZmFsc2UsXG4gICAgICBrZXl3b3JkQm9vc3QgPSAxLjUsXG4gICAgfSA9IG9wdGlvbnM7XG5cbiAgICAvLyAxLiDliqDovb3orrDlv4ZcbiAgICBjb25zdCBtZW1vcmllcyA9IGF3YWl0IHRoaXMubG9hZE1lbW9yaWVzKCk7XG5cbiAgICAvLyAyLiDov4fmu6TvvIjml7bpl7Qv5oOF5oSfL+exu+Wei++8iVxuICAgIGxldCBmaWx0ZXJlZCA9IHRoaXMuZmlsdGVyTWVtb3JpZXMobWVtb3JpZXMsIHtcbiAgICAgIHR5cGUsXG4gICAgICBzdGFydFRpbWUsXG4gICAgICBlbmRUaW1lLFxuICAgICAgZW1vdGlvbixcbiAgICAgIG1pbkVtb3Rpb25JbnRlbnNpdHksXG4gICAgfSk7XG5cbiAgICAvLyAzLiDorqHnrpfor4TliIZcbiAgICBjb25zdCBzY29yZWQgPSB0aGlzLmNhbGN1bGF0ZVNjb3JlcyhmaWx0ZXJlZCwgcXVlcnksIHtcbiAgICAgIHJlY2VuY3lXZWlnaHQsXG4gICAgICBpbXBvcnRhbmNlV2VpZ2h0LFxuICAgICAgcmVsZXZhbmNlV2VpZ2h0LFxuICAgICAgaHlicmlkU2VhcmNoLFxuICAgICAga2V5d29yZEJvb3N0LFxuICAgIH0pO1xuXG4gICAgLy8gNC4g5o6S5bqPXG4gICAgc2NvcmVkLnNvcnQoKGEsIGIpID0+IChiLmNvbWJpbmVkU2NvcmUgfHwgMCkgLSAoYS5jb21iaW5lZFNjb3JlIHx8IDApKTtcblxuICAgIC8vIDUuIOWKqOaAgSBUb3AtS++8iOWPguiAgyBNZW0w77yJXG4gICAgY29uc3QgZmluYWxMaW1pdCA9IGR5bmFtaWNLIFxuICAgICAgPyB0aGlzLmNhbGN1bGF0ZUR5bmFtaWNLKHNjb3JlZCwgbWluSywgbWF4SylcbiAgICAgIDogbGltaXQ7XG5cbiAgICBjb25zdCB0b3BNZW1vcmllcyA9IHNjb3JlZC5zbGljZSgwLCBmaW5hbExpbWl0KTtcblxuICAgIC8vIDYuIOe7n+iuoeS/oeaBr1xuICAgIGNvbnN0IHN0YXRzID0gdGhpcy5jYWxjdWxhdGVTdGF0cyh0b3BNZW1vcmllcyk7XG5cbiAgICByZXR1cm4ge1xuICAgICAgbWVtb3JpZXM6IHRvcE1lbW9yaWVzLFxuICAgICAgdG90YWw6IGZpbHRlcmVkLmxlbmd0aCxcbiAgICAgIHF1ZXJ5LFxuICAgICAgc2VhcmNoVHlwZTogdHlwZSxcbiAgICAgIHNjb3Jlczogc3RhdHMuc2NvcmVzLFxuICAgICAgZW1vdGlvbnM6IHN0YXRzLmVtb3Rpb25zLFxuICAgIH07XG4gIH1cblxuICAvKipcbiAgICog5Yqg6L296K6w5b+GXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIGxvYWRNZW1vcmllcygpOiBQcm9taXNlPE1lbW9yeUl0ZW1bXT4ge1xuICAgIC8vIOajgOafpee8k+WtmFxuICAgIGlmICh0aGlzLmluZGV4Q2FjaGUuaGFzKCdhbGwnKSkge1xuICAgICAgcmV0dXJuIHRoaXMuaW5kZXhDYWNoZS5nZXQoJ2FsbCcpITtcbiAgICB9XG5cbiAgICBjb25zdCBtZW1vcmllczogTWVtb3J5SXRlbVtdID0gW107XG4gICAgY29uc3QgbWVtb3J5RGlyID0gcGF0aC5qb2luKHByb2Nlc3MuY3dkKCksIHRoaXMubWVtb3J5RGlyKTtcblxuICAgIC8vIOWKoOi9vSBNRU1PUlkubWRcbiAgICBjb25zdCBtZW1vcnlGaWxlID0gcGF0aC5qb2luKG1lbW9yeURpciwgJ01FTU9SWS5tZCcpO1xuICAgIGlmIChmcy5leGlzdHNTeW5jKG1lbW9yeUZpbGUpKSB7XG4gICAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKG1lbW9yeUZpbGUsICd1dGYtOCcpO1xuICAgICAgY29uc3QgcGFyc2VkID0gdGhpcy5wYXJzZU1lbW9yeU1kKGNvbnRlbnQpO1xuICAgICAgbWVtb3JpZXMucHVzaCguLi5wYXJzZWQpO1xuICAgIH1cblxuICAgIC8vIOWKoOi9vSBkYWlseSBtZW1vcnlcbiAgICBjb25zdCBkYWlseURpciA9IHBhdGguam9pbihtZW1vcnlEaXIsICdkYWlseScpO1xuICAgIGlmIChmcy5leGlzdHNTeW5jKGRhaWx5RGlyKSkge1xuICAgICAgY29uc3QgZmlsZXMgPSBmcy5yZWFkZGlyU3luYyhkYWlseURpcikuZmlsdGVyKGYgPT4gZi5lbmRzV2l0aCgnLm1kJykpO1xuICAgICAgZm9yIChjb25zdCBmaWxlIG9mIGZpbGVzKSB7XG4gICAgICAgIGNvbnN0IGZpbGVQYXRoID0gcGF0aC5qb2luKGRhaWx5RGlyLCBmaWxlKTtcbiAgICAgICAgY29uc3QgY29udGVudCA9IGZzLnJlYWRGaWxlU3luYyhmaWxlUGF0aCwgJ3V0Zi04Jyk7XG4gICAgICAgIGNvbnN0IHBhcnNlZCA9IHRoaXMucGFyc2VEYWlseU1lbW9yeShjb250ZW50LCBmaWxlKTtcbiAgICAgICAgbWVtb3JpZXMucHVzaCguLi5wYXJzZWQpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIOWKoOi9vSB3aWtpIG1lbW9yee+8iHY0LjEg5paw5aKe77yJXG4gICAgY29uc3Qgd2lraURpciA9IHBhdGguam9pbihtZW1vcnlEaXIsICd3aWtpJyk7XG4gICAgaWYgKGZzLmV4aXN0c1N5bmMod2lraURpcikpIHtcbiAgICAgIGNvbnN0IGZpbGVzID0gZnMucmVhZGRpclN5bmMod2lraURpcikuZmlsdGVyKGYgPT4gZi5lbmRzV2l0aCgnLm1kJykpO1xuICAgICAgZm9yIChjb25zdCBmaWxlIG9mIGZpbGVzKSB7XG4gICAgICAgIGNvbnN0IGZpbGVQYXRoID0gcGF0aC5qb2luKHdpa2lEaXIsIGZpbGUpO1xuICAgICAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKGZpbGVQYXRoLCAndXRmLTgnKTtcbiAgICAgICAgY29uc3QgcGFyc2VkID0gdGhpcy5wYXJzZVdpa2lNZW1vcnkoY29udGVudCwgZmlsZSk7XG4gICAgICAgIG1lbW9yaWVzLnB1c2goLi4ucGFyc2VkKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyDnvJPlrZhcbiAgICB0aGlzLmluZGV4Q2FjaGUuc2V0KCdhbGwnLCBtZW1vcmllcyk7XG5cbiAgICByZXR1cm4gbWVtb3JpZXM7XG4gIH1cblxuICAvKipcbiAgICog6L+H5ruk6K6w5b+GXG4gICAqL1xuICBwcml2YXRlIGZpbHRlck1lbW9yaWVzKFxuICAgIG1lbW9yaWVzOiBNZW1vcnlJdGVtW10sXG4gICAgZmlsdGVyczoge1xuICAgICAgdHlwZT86IHN0cmluZztcbiAgICAgIHN0YXJ0VGltZT86IG51bWJlcjtcbiAgICAgIGVuZFRpbWU/OiBudW1iZXI7XG4gICAgICBlbW90aW9uPzogRW1vdGlvblR5cGU7XG4gICAgICBtaW5FbW90aW9uSW50ZW5zaXR5PzogbnVtYmVyO1xuICAgIH1cbiAgKTogTWVtb3J5SXRlbVtdIHtcbiAgICByZXR1cm4gbWVtb3JpZXMuZmlsdGVyKG1lbW9yeSA9PiB7XG4gICAgICAvLyDml7bpl7Tov4fmu6RcbiAgICAgIGlmIChmaWx0ZXJzLnN0YXJ0VGltZSAmJiBtZW1vcnkudGltZXN0YW1wIDwgZmlsdGVycy5zdGFydFRpbWUpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgaWYgKGZpbHRlcnMuZW5kVGltZSAmJiBtZW1vcnkudGltZXN0YW1wID4gZmlsdGVycy5lbmRUaW1lKSB7XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cblxuICAgICAgLy8g5oOF5oSf6L+H5ruk77yIdjQuMSDmlrDlop7vvIlcbiAgICAgIGlmIChmaWx0ZXJzLmVtb3Rpb24gJiYgbWVtb3J5Lm1ldGFkYXRhPy5lbW90aW9uICE9PSBmaWx0ZXJzLmVtb3Rpb24pIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgaWYgKGZpbHRlcnMubWluRW1vdGlvbkludGVuc2l0eSAmJiBcbiAgICAgICAgICAobWVtb3J5Lm1ldGFkYXRhPy5lbW90aW9uSW50ZW5zaXR5IHx8IDApIDwgZmlsdGVycy5taW5FbW90aW9uSW50ZW5zaXR5KSB7XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHRydWU7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICog6K6h566X6K+E5YiG77yI5Y+C6ICDIEdlbmVyYXRpdmUgQWdlbnRz77yJXG4gICAqL1xuICBwcml2YXRlIGNhbGN1bGF0ZVNjb3JlcyhcbiAgICBtZW1vcmllczogTWVtb3J5SXRlbVtdLFxuICAgIHF1ZXJ5OiBzdHJpbmcsXG4gICAgb3B0aW9uczoge1xuICAgICAgcmVjZW5jeVdlaWdodDogbnVtYmVyO1xuICAgICAgaW1wb3J0YW5jZVdlaWdodDogbnVtYmVyO1xuICAgICAgcmVsZXZhbmNlV2VpZ2h0OiBudW1iZXI7XG4gICAgICBoeWJyaWRTZWFyY2g6IGJvb2xlYW47XG4gICAgICBrZXl3b3JkQm9vc3Q6IG51bWJlcjtcbiAgICB9XG4gICk6IE1lbW9yeUl0ZW1bXSB7XG4gICAgY29uc3Qgbm93ID0gRGF0ZS5ub3coKTtcbiAgICBjb25zdCBvbmVEYXkgPSAyNCAqIDYwICogNjAgKiAxMDAwO1xuICAgIGNvbnN0IG9uZVdlZWsgPSA3ICogb25lRGF5O1xuICAgIGNvbnN0IG9uZU1vbnRoID0gMzAgKiBvbmVEYXk7XG5cbiAgICByZXR1cm4gbWVtb3JpZXMubWFwKG1lbW9yeSA9PiB7XG4gICAgICAvLyAxLiDov5Hlm6Dor4TliIbvvIhSZWNlbmN577yJLSDmjIfmlbDoobDlh49cbiAgICAgIGNvbnN0IGFnZSA9IG5vdyAtIG1lbW9yeS50aW1lc3RhbXA7XG4gICAgICBsZXQgcmVjZW5jeVNjb3JlOiBudW1iZXI7XG4gICAgICBcbiAgICAgIGlmIChhZ2UgPCBvbmVEYXkpIHtcbiAgICAgICAgcmVjZW5jeVNjb3JlID0gMS4wO1xuICAgICAgfSBlbHNlIGlmIChhZ2UgPCBvbmVXZWVrKSB7XG4gICAgICAgIHJlY2VuY3lTY29yZSA9IDAuODtcbiAgICAgIH0gZWxzZSBpZiAoYWdlIDwgb25lTW9udGgpIHtcbiAgICAgICAgcmVjZW5jeVNjb3JlID0gMC41O1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmVjZW5jeVNjb3JlID0gMC4zO1xuICAgICAgfVxuXG4gICAgICAvLyAyLiDph43opoHmgKfor4TliIbvvIhJbXBvcnRhbmNl77yJXG4gICAgICBjb25zdCBpbXBvcnRhbmNlU2NvcmUgPSBtZW1vcnkubWV0YWRhdGE/LmltcG9ydGFuY2UgfHwgMztcblxuICAgICAgLy8gMy4g55u45YWz5oCn6K+E5YiG77yIUmVsZXZhbmNl77yJLSDnroDljZXlhbPplK7or43ljLnphY1cbiAgICAgIGxldCByZWxldmFuY2VTY29yZSA9IDA7XG4gICAgICBjb25zdCBxdWVyeVdvcmRzID0gcXVlcnkudG9Mb3dlckNhc2UoKS5zcGxpdCgvXFxzKy8pO1xuICAgICAgY29uc3QgY29udGVudCA9IG1lbW9yeS5jb250ZW50LnRvTG93ZXJDYXNlKCk7XG4gICAgICBcbiAgICAgIGZvciAoY29uc3Qgd29yZCBvZiBxdWVyeVdvcmRzKSB7XG4gICAgICAgIGlmICh3b3JkLmxlbmd0aCA+IDIgJiYgY29udGVudC5pbmNsdWRlcyh3b3JkKSkge1xuICAgICAgICAgIHJlbGV2YW5jZVNjb3JlICs9IDE7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHJlbGV2YW5jZVNjb3JlID0gTWF0aC5taW4ocmVsZXZhbmNlU2NvcmUgLyBxdWVyeVdvcmRzLmxlbmd0aCwgMS4wKTtcblxuICAgICAgLy8g5re35ZCI5qOA57Si5aKe5by677yIdjQuMSDmlrDlop7vvIlcbiAgICAgIGlmIChvcHRpb25zLmh5YnJpZFNlYXJjaCAmJiByZWxldmFuY2VTY29yZSA+IDApIHtcbiAgICAgICAgcmVsZXZhbmNlU2NvcmUgKj0gb3B0aW9ucy5rZXl3b3JkQm9vc3Q7XG4gICAgICB9XG5cbiAgICAgIC8vIDQuIOe7vOWQiOivhOWIhlxuICAgICAgY29uc3QgY29tYmluZWRTY29yZSA9IFxuICAgICAgICByZWNlbmN5U2NvcmUgKiBvcHRpb25zLnJlY2VuY3lXZWlnaHQgK1xuICAgICAgICAoaW1wb3J0YW5jZVNjb3JlIC8gNSkgKiBvcHRpb25zLmltcG9ydGFuY2VXZWlnaHQgK1xuICAgICAgICByZWxldmFuY2VTY29yZSAqIG9wdGlvbnMucmVsZXZhbmNlV2VpZ2h0O1xuXG4gICAgICByZXR1cm4ge1xuICAgICAgICAuLi5tZW1vcnksXG4gICAgICAgIHJlY2VuY3lTY29yZSxcbiAgICAgICAgaW1wb3J0YW5jZVNjb3JlLFxuICAgICAgICByZWxldmFuY2VTY29yZSxcbiAgICAgICAgY29tYmluZWRTY29yZSxcbiAgICAgIH07XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICog5Yqo5oCBIFRvcC1L77yI5Y+C6ICDIE1lbTDvvIlcbiAgICovXG4gIHByaXZhdGUgY2FsY3VsYXRlRHluYW1pY0soXG4gICAgbWVtb3JpZXM6IE1lbW9yeUl0ZW1bXSxcbiAgICBtaW5LOiBudW1iZXIsXG4gICAgbWF4SzogbnVtYmVyXG4gICk6IG51bWJlciB7XG4gICAgaWYgKG1lbW9yaWVzLmxlbmd0aCA9PT0gMCkge1xuICAgICAgcmV0dXJuIG1pbks7XG4gICAgfVxuXG4gICAgLy8g6K6h566X6K+E5YiG5YiG5biDXG4gICAgY29uc3Qgc2NvcmVzID0gbWVtb3JpZXMubWFwKG0gPT4gbS5jb21iaW5lZFNjb3JlIHx8IDApO1xuICAgIGNvbnN0IG1heFNjb3JlID0gTWF0aC5tYXgoLi4uc2NvcmVzKTtcbiAgICBjb25zdCBhdmdTY29yZSA9IHNjb3Jlcy5yZWR1Y2UoKGEsIGIpID0+IGEgKyBiLCAwKSAvIHNjb3Jlcy5sZW5ndGg7XG5cbiAgICAvLyDliqjmgIHosIPmlbQgSyDlgLxcbiAgICAvLyDlpoLmnpzmnIDpq5jliIbov5zpq5jkuo7lubPlnYfliIbvvIzor7TmmI7mnInmmI7noa7nrZTmoYjvvIzov5Tlm57ovoPlsJHnu5PmnpxcbiAgICAvLyDlpoLmnpzliIbmlbDliIbluIPlnYfljIDvvIzor7TmmI7pnIDopoHmm7TlpJrkuIrkuIvmlofvvIzov5Tlm57ovoPlpJrnu5PmnpxcbiAgICBjb25zdCByYXRpbyA9IG1heFNjb3JlIC8gKGF2Z1Njb3JlIHx8IDAuMSk7XG4gICAgXG4gICAgaWYgKHJhdGlvID4gMikge1xuICAgICAgLy8g5piO56Gu562U5qGIXG4gICAgICByZXR1cm4gTWF0aC5tYXgobWluSywgTWF0aC5mbG9vcihtYXhLICogMC4zKSk7XG4gICAgfSBlbHNlIGlmIChyYXRpbyA+IDEuNSkge1xuICAgICAgLy8g5Lit562J5piO56GuXG4gICAgICByZXR1cm4gTWF0aC5tYXgobWluSywgTWF0aC5mbG9vcihtYXhLICogMC41KSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIOmcgOimgeabtOWkmuS4iuS4i+aWh1xuICAgICAgcmV0dXJuIG1heEs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIOiuoeeul+e7n+iuoeS/oeaBr1xuICAgKi9cbiAgcHJpdmF0ZSBjYWxjdWxhdGVTdGF0cyhtZW1vcmllczogTWVtb3J5SXRlbVtdKSB7XG4gICAgY29uc3Qgc2NvcmVzID0ge1xuICAgICAgYXZnUmVjZW5jeTogMCxcbiAgICAgIGF2Z0ltcG9ydGFuY2U6IDAsXG4gICAgICBhdmdSZWxldmFuY2U6IDAsXG4gICAgfTtcblxuICAgIGNvbnN0IGVtb3Rpb25zID0ge1xuICAgICAgcG9zaXRpdmU6IDAsXG4gICAgICBuZWdhdGl2ZTogMCxcbiAgICAgIG5ldXRyYWw6IDAsXG4gICAgfTtcblxuICAgIGlmIChtZW1vcmllcy5sZW5ndGggPT09IDApIHtcbiAgICAgIHJldHVybiB7IHNjb3JlcywgZW1vdGlvbnMgfTtcbiAgICB9XG5cbiAgICAvLyDorqHnrpflubPlnYfor4TliIZcbiAgICBzY29yZXMuYXZnUmVjZW5jeSA9IG1lbW9yaWVzLnJlZHVjZSgoc3VtLCBtKSA9PiBzdW0gKyAobS5yZWNlbmN5U2NvcmUgfHwgMCksIDApIC8gbWVtb3JpZXMubGVuZ3RoO1xuICAgIHNjb3Jlcy5hdmdJbXBvcnRhbmNlID0gbWVtb3JpZXMucmVkdWNlKChzdW0sIG0pID0+IHN1bSArIChtLmltcG9ydGFuY2VTY29yZSB8fCAwKSwgMCkgLyBtZW1vcmllcy5sZW5ndGg7XG4gICAgc2NvcmVzLmF2Z1JlbGV2YW5jZSA9IG1lbW9yaWVzLnJlZHVjZSgoc3VtLCBtKSA9PiBzdW0gKyAobS5yZWxldmFuY2VTY29yZSB8fCAwKSwgMCkgLyBtZW1vcmllcy5sZW5ndGg7XG5cbiAgICAvLyDnu5/orqHmg4XmhJ/liIbluIPvvIh2NC4xIOaWsOWinu+8iVxuICAgIGZvciAoY29uc3QgbWVtb3J5IG9mIG1lbW9yaWVzKSB7XG4gICAgICBjb25zdCBlbW90aW9uID0gbWVtb3J5Lm1ldGFkYXRhPy5lbW90aW9uO1xuICAgICAgaWYgKGVtb3Rpb24pIHtcbiAgICAgICAgaWYgKFsncG9zaXRpdmUnLCAnam95JywgJ3N1cnByaXNlJ10uaW5jbHVkZXMoZW1vdGlvbikpIHtcbiAgICAgICAgICBlbW90aW9ucy5wb3NpdGl2ZSsrO1xuICAgICAgICB9IGVsc2UgaWYgKFsnbmVnYXRpdmUnLCAnc2FkbmVzcycsICdhbmdlcicsICdmZWFyJywgJ2Rpc2d1c3QnXS5pbmNsdWRlcyhlbW90aW9uKSkge1xuICAgICAgICAgIGVtb3Rpb25zLm5lZ2F0aXZlKys7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgZW1vdGlvbnMubmV1dHJhbCsrO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIHsgc2NvcmVzLCBlbW90aW9ucyB9O1xuICB9XG5cbiAgLyoqXG4gICAqIOino+aekCBNRU1PUlkubWRcbiAgICovXG4gIHByaXZhdGUgcGFyc2VNZW1vcnlNZChjb250ZW50OiBzdHJpbmcpOiBNZW1vcnlJdGVtW10ge1xuICAgIGNvbnN0IG1lbW9yaWVzOiBNZW1vcnlJdGVtW10gPSBbXTtcbiAgICBjb25zdCBzZWN0aW9ucyA9IGNvbnRlbnQuc3BsaXQoL14oIyMgfCMjIyApL2dtKTtcblxuICAgIGxldCBjdXJyZW50U2VjdGlvbiA9ICcnO1xuICAgIGxldCBjdXJyZW50SWQgPSAnJztcbiAgICBsZXQgY3VycmVudENvbnRlbnQgPSAnJztcblxuICAgIGZvciAoY29uc3Qgc2VjdGlvbiBvZiBzZWN0aW9ucykge1xuICAgICAgaWYgKHNlY3Rpb24uc3RhcnRzV2l0aCgnIyMgJykgfHwgc2VjdGlvbi5zdGFydHNXaXRoKCcjIyMgJykpIHtcbiAgICAgICAgLy8g5L+d5a2Y5LiK5LiA5Liq6K6w5b+GXG4gICAgICAgIGlmIChjdXJyZW50SWQgJiYgY3VycmVudENvbnRlbnQpIHtcbiAgICAgICAgICBtZW1vcmllcy5wdXNoKHtcbiAgICAgICAgICAgIGlkOiBjdXJyZW50SWQsXG4gICAgICAgICAgICBjb250ZW50OiBjdXJyZW50Q29udGVudC50cmltKCksXG4gICAgICAgICAgICB0eXBlOiAn6K+t5LmJJyxcbiAgICAgICAgICAgIHRpbWVzdGFtcDogRGF0ZS5ub3coKSxcbiAgICAgICAgICAgIG1ldGFkYXRhOiB7XG4gICAgICAgICAgICAgIGltcG9ydGFuY2U6IDQsXG4gICAgICAgICAgICB9LFxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG5cbiAgICAgICAgY3VycmVudFNlY3Rpb24gPSBzZWN0aW9uLnRyaW0oKTtcbiAgICAgICAgY3VycmVudElkID0gdGhpcy5leHRyYWN0SWQoc2VjdGlvbik7XG4gICAgICAgIGN1cnJlbnRDb250ZW50ID0gJyc7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjdXJyZW50Q29udGVudCArPSBzZWN0aW9uO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIOS/neWtmOacgOWQjuS4gOS4quiusOW/hlxuICAgIGlmIChjdXJyZW50SWQgJiYgY3VycmVudENvbnRlbnQpIHtcbiAgICAgIG1lbW9yaWVzLnB1c2goe1xuICAgICAgICBpZDogY3VycmVudElkLFxuICAgICAgICBjb250ZW50OiBjdXJyZW50Q29udGVudC50cmltKCksXG4gICAgICAgIHR5cGU6ICfor63kuYknLFxuICAgICAgICB0aW1lc3RhbXA6IERhdGUubm93KCksXG4gICAgICAgIG1ldGFkYXRhOiB7XG4gICAgICAgICAgaW1wb3J0YW5jZTogNCxcbiAgICAgICAgfSxcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIHJldHVybiBtZW1vcmllcztcbiAgfVxuXG4gIC8qKlxuICAgKiDop6PmnpDmr4/ml6XorrDlv4ZcbiAgICovXG4gIHByaXZhdGUgcGFyc2VEYWlseU1lbW9yeShjb250ZW50OiBzdHJpbmcsIGZpbGVuYW1lOiBzdHJpbmcpOiBNZW1vcnlJdGVtW10ge1xuICAgIGNvbnN0IG1lbW9yaWVzOiBNZW1vcnlJdGVtW10gPSBbXTtcbiAgICBjb25zdCBkYXRlID0gZmlsZW5hbWUucmVwbGFjZSgnLm1kJywgJycpO1xuICAgIGNvbnN0IHRpbWVzdGFtcCA9IG5ldyBEYXRlKGRhdGUpLmdldFRpbWUoKTtcblxuICAgIGNvbnN0IGxpbmVzID0gY29udGVudC5zcGxpdCgnXFxuJyk7XG4gICAgbGV0IGN1cnJlbnRJZCA9ICcnO1xuICAgIGxldCBjdXJyZW50Q29udGVudCA9ICcnO1xuXG4gICAgZm9yIChjb25zdCBsaW5lIG9mIGxpbmVzKSB7XG4gICAgICBpZiAobGluZS5zdGFydHNXaXRoKCcqKklEKio6JykpIHtcbiAgICAgICAgLy8g5L+d5a2Y5LiK5LiA5Liq6K6w5b+GXG4gICAgICAgIGlmIChjdXJyZW50SWQgJiYgY3VycmVudENvbnRlbnQpIHtcbiAgICAgICAgICBtZW1vcmllcy5wdXNoKHtcbiAgICAgICAgICAgIGlkOiBjdXJyZW50SWQsXG4gICAgICAgICAgICBjb250ZW50OiBjdXJyZW50Q29udGVudC50cmltKCksXG4gICAgICAgICAgICB0eXBlOiAn5oOF5pmvJyxcbiAgICAgICAgICAgIHRpbWVzdGFtcCxcbiAgICAgICAgICAgIG1ldGFkYXRhOiB7XG4gICAgICAgICAgICAgIGltcG9ydGFuY2U6IDMsXG4gICAgICAgICAgICB9LFxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG5cbiAgICAgICAgY3VycmVudElkID0gbGluZS5yZXBsYWNlKCcqKklEKio6JywgJycpLnRyaW0oKTtcbiAgICAgICAgY3VycmVudENvbnRlbnQgPSAnJztcbiAgICAgIH0gZWxzZSBpZiAoY3VycmVudElkKSB7XG4gICAgICAgIGN1cnJlbnRDb250ZW50ICs9IGxpbmUgKyAnXFxuJztcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyDkv53lrZjmnIDlkI7kuIDkuKrorrDlv4ZcbiAgICBpZiAoY3VycmVudElkICYmIGN1cnJlbnRDb250ZW50KSB7XG4gICAgICBtZW1vcmllcy5wdXNoKHtcbiAgICAgICAgaWQ6IGN1cnJlbnRJZCxcbiAgICAgICAgY29udGVudDogY3VycmVudENvbnRlbnQudHJpbSgpLFxuICAgICAgICB0eXBlOiAn5oOF5pmvJyxcbiAgICAgICAgdGltZXN0YW1wLFxuICAgICAgICBtZXRhZGF0YToge1xuICAgICAgICAgIGltcG9ydGFuY2U6IDMsXG4gICAgICAgIH0sXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICByZXR1cm4gbWVtb3JpZXM7XG4gIH1cblxuICAvKipcbiAgICog6Kej5p6QIFdpa2kg6K6w5b+G77yIdjQuMSDmlrDlop7vvIlcbiAgICovXG4gIHByaXZhdGUgcGFyc2VXaWtpTWVtb3J5KGNvbnRlbnQ6IHN0cmluZywgZmlsZW5hbWU6IHN0cmluZyk6IE1lbW9yeUl0ZW1bXSB7XG4gICAgY29uc3QgbWVtb3JpZXM6IE1lbW9yeUl0ZW1bXSA9IFtdO1xuICAgIGNvbnN0IHR5cGUgPSBmaWxlbmFtZS5yZXBsYWNlKCcubWQnLCAnJykgYXMgYW55O1xuXG4gICAgY29uc3Qgc2VjdGlvbnMgPSBjb250ZW50LnNwbGl0KC9eIyMgL2dtKTtcblxuICAgIGZvciAoY29uc3Qgc2VjdGlvbiBvZiBzZWN0aW9ucykge1xuICAgICAgaWYgKHNlY3Rpb24udHJpbSgpKSB7XG4gICAgICAgIGNvbnN0IGxpbmVzID0gc2VjdGlvbi5zcGxpdCgnXFxuJyk7XG4gICAgICAgIGNvbnN0IHRpdGxlID0gbGluZXNbMF0udHJpbSgpO1xuICAgICAgICBjb25zdCBjb250ZW50ID0gbGluZXMuc2xpY2UoMSkuam9pbignXFxuJykudHJpbSgpO1xuXG4gICAgICAgIGlmIChjb250ZW50KSB7XG4gICAgICAgICAgbWVtb3JpZXMucHVzaCh7XG4gICAgICAgICAgICBpZDogYHdpa2lfJHt0eXBlfV8ke3RpdGxlfWAsXG4gICAgICAgICAgICBjb250ZW50OiBgJHt0aXRsZX06ICR7Y29udGVudH1gLFxuICAgICAgICAgICAgdHlwZTogJ+ivreS5iScsXG4gICAgICAgICAgICB0aW1lc3RhbXA6IERhdGUubm93KCksXG4gICAgICAgICAgICBtZXRhZGF0YToge1xuICAgICAgICAgICAgICBpbXBvcnRhbmNlOiA0LFxuICAgICAgICAgICAgICB0YWdzOiBbdHlwZV0sXG4gICAgICAgICAgICB9LFxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIG1lbW9yaWVzO1xuICB9XG5cbiAgLyoqXG4gICAqIOaPkOWPliBJRFxuICAgKi9cbiAgcHJpdmF0ZSBleHRyYWN0SWQodGV4dDogc3RyaW5nKTogc3RyaW5nIHtcbiAgICBjb25zdCBtYXRjaCA9IHRleHQubWF0Y2goL1xcKlxcKklEXFwqXFwqOlxccyooXFxTKykvKTtcbiAgICByZXR1cm4gbWF0Y2ggPyBtYXRjaFsxXSA6IGBtZW1fJHtEYXRlLm5vdygpfWA7XG4gIH1cblxuICAvKipcbiAgICog5qOA5rWL5oOF5oSf77yIdjQuMSDmlrDlop7vvIznroDljZXlrp7njrDvvIlcbiAgICovXG4gIGRldGVjdEVtb3Rpb24oY29udGVudDogc3RyaW5nKTogeyBlbW90aW9uOiBFbW90aW9uVHlwZTsgaW50ZW5zaXR5OiBudW1iZXIgfSB7XG4gICAgY29uc3QgcG9zaXRpdmVXb3JkcyA9IFsn5aW9JywgJ+ajkicsICfkvJjnp4AnLCAn5oiQ5YqfJywgJ+W8gOW/gycsICfpq5jlhbQnLCAn5Zac5qyiJywgJ+eIsScsICfmu6HmhI8nLCAn5a6M576OJ107XG4gICAgY29uc3QgbmVnYXRpdmVXb3JkcyA9IFsn5Z2PJywgJ+W3ricsICflpLHotKUnLCAn6Zq+6L+HJywgJ+eUn+awlCcsICforqjljownLCAn5oGoJywgJ+WkseacmycsICfns5/ns5UnLCAn6ZSZ6K+vJ107XG4gICAgXG4gICAgY29uc3QgY29udGVudExvd2VyID0gY29udGVudC50b0xvd2VyQ2FzZSgpO1xuICAgIGxldCBwb3NpdGl2ZUNvdW50ID0gMDtcbiAgICBsZXQgbmVnYXRpdmVDb3VudCA9IDA7XG5cbiAgICBmb3IgKGNvbnN0IHdvcmQgb2YgcG9zaXRpdmVXb3Jkcykge1xuICAgICAgaWYgKGNvbnRlbnRMb3dlci5pbmNsdWRlcyh3b3JkKSkge1xuICAgICAgICBwb3NpdGl2ZUNvdW50Kys7XG4gICAgICB9XG4gICAgfVxuXG4gICAgZm9yIChjb25zdCB3b3JkIG9mIG5lZ2F0aXZlV29yZHMpIHtcbiAgICAgIGlmIChjb250ZW50TG93ZXIuaW5jbHVkZXMod29yZCkpIHtcbiAgICAgICAgbmVnYXRpdmVDb3VudCsrO1xuICAgICAgfVxuICAgIH1cblxuICAgIGNvbnN0IHRvdGFsID0gcG9zaXRpdmVDb3VudCArIG5lZ2F0aXZlQ291bnQ7XG4gICAgXG4gICAgaWYgKHRvdGFsID09PSAwKSB7XG4gICAgICByZXR1cm4geyBlbW90aW9uOiAnbmV1dHJhbCcsIGludGVuc2l0eTogMSB9O1xuICAgIH1cblxuICAgIGNvbnN0IGludGVuc2l0eSA9IE1hdGgubWluKDUsIE1hdGguY2VpbCh0b3RhbCAvIDMpKTtcblxuICAgIGlmIChwb3NpdGl2ZUNvdW50ID4gbmVnYXRpdmVDb3VudCkge1xuICAgICAgcmV0dXJuIHsgZW1vdGlvbjogJ3Bvc2l0aXZlJywgaW50ZW5zaXR5IH07XG4gICAgfSBlbHNlIGlmIChuZWdhdGl2ZUNvdW50ID4gcG9zaXRpdmVDb3VudCkge1xuICAgICAgcmV0dXJuIHsgZW1vdGlvbjogJ25lZ2F0aXZlJywgaW50ZW5zaXR5IH07XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB7IGVtb3Rpb246ICduZXV0cmFsJywgaW50ZW5zaXR5IH07XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIOa4hemZpOe8k+WtmFxuICAgKi9cbiAgY2xlYXJDYWNoZSgpOiB2b2lkIHtcbiAgICB0aGlzLmluZGV4Q2FjaGUuY2xlYXIoKTtcbiAgfVxufVxuIl19