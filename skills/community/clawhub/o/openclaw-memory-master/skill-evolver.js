"use strict";
/**
 * Memory-Master 记忆检索模块
 *
 * 支持 5 种查询类型（基于 Karpathy 方法论）
 * - procedural: 流程查询
 * - temporal: 时间查询
 * - relational: 关系查询
 * - persona: 偏好查询
 * - factual: 事实查询
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
exports.MemoryRetriever = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const glob = __importStar(require("glob"));
/**
 * 记忆检索器
 */
class MemoryRetriever {
    constructor(memoryDir = 'memory') {
        this.memoryDir = memoryDir;
        this.memoryFile = path.join(memoryDir, 'MEMORY.md');
    }
    /**
     * 检索记忆
     */
    async retrieve(query, options = {}) {
        const startTime = Date.now();
        const { type = this.classifyQuery(query), limit = 5, timeRange, includeRaw = false, } = options;
        // 1. 根据查询类型选择检索策略
        let memories = [];
        switch (type) {
            case 'procedural':
                memories = await this.searchProcedural(query, limit);
                break;
            case 'temporal':
                memories = await this.searchTemporal(query, limit, timeRange);
                break;
            case 'relational':
                memories = await this.searchRelational(query, limit);
                break;
            case 'persona':
                memories = await this.searchPersona(query, limit);
                break;
            case 'factual':
                memories = await this.searchFactual(query, limit);
                break;
        }
        // 2. 限制返回数量
        memories = memories.slice(0, limit);
        // 3. 返回结果
        return {
            success: true,
            queryType: type,
            memories,
            timeMs: Date.now() - startTime,
        };
    }
    /**
     * 自动分类查询类型
     */
    classifyQuery(query) {
        const q = query.toLowerCase();
        // 流程查询关键词
        if (q.includes('如何') || q.includes('怎么做') || q.includes('步骤') || q.includes('流程')) {
            return 'procedural';
        }
        // 时间查询关键词
        if (q.includes('什么时候') || q.includes('昨天') || q.includes('今天') ||
            q.includes('明天') || q.includes('上周') || q.includes('下周')) {
            return 'temporal';
        }
        // 偏好查询关键词
        if (q.includes('喜欢') || q.includes('偏好') || q.includes('习惯') ||
            q.includes('我 ') && (q.includes('什么') || q.includes('怎么样'))) {
            return 'persona';
        }
        // 关系查询关键词
        if (q.includes('关系') || q.includes('关联') || q.includes('和 ') && q.includes('什么')) {
            return 'relational';
        }
        // 默认：事实查询
        return 'factual';
    }
    /**
     * 流程查询
     */
    async searchProcedural(query, limit) {
        // 从 MEMORY.md 的程序记忆章节检索
        if (!fs.existsSync(this.memoryFile)) {
            return [];
        }
        const content = fs.readFileSync(this.memoryFile, 'utf-8');
        const sectionStart = content.indexOf('## 程序记忆');
        if (sectionStart === -1) {
            return [];
        }
        const sectionEnd = content.indexOf('\n## ', sectionStart + 1);
        const section = content.substring(sectionStart, sectionEnd === -1 ? undefined : sectionEnd);
        // 简单关键词匹配（TODO: 实现向量检索）
        const memories = this.extractMemoriesFromSection(section, '程序');
        return this.rankByRelevance(memories, query).slice(0, limit);
    }
    /**
     * 时间查询
     */
    async searchTemporal(query, limit, timeRange) {
        const memories = [];
        // 解析时间关键词
        const { start, end } = this.parseTimeRange(query, timeRange);
        // 检索指定日期范围内的文件
        const files = glob.sync(path.join(this.memoryDir, '*.md'));
        for (const file of files) {
            const fileName = path.basename(file);
            const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})\.md/);
            if (!dateMatch)
                continue;
            const fileDate = dateMatch[1];
            // 检查是否在时间范围内
            if (start && fileDate < start)
                continue;
            if (end && fileDate > end)
                continue;
            // 读取文件内容
            const content = fs.readFileSync(file, 'utf-8');
            const extracted = this.extractMemoriesFromFile(file, content);
            memories.push(...extracted);
        }
        // 按时间倒序排列
        memories.sort((a, b) => b.timestamp - a.timestamp);
        return memories.slice(0, limit);
    }
    /**
     * 关系查询
     */
    async searchRelational(query, limit) {
        // TODO: 实现知识图谱检索
        // 目前返回所有相关记忆
        return this.searchFactual(query, limit);
    }
    /**
     * 偏好查询
     */
    async searchPersona(query, limit) {
        if (!fs.existsSync(this.memoryFile)) {
            return [];
        }
        const content = fs.readFileSync(this.memoryFile, 'utf-8');
        const sectionStart = content.indexOf('## 人设记忆');
        if (sectionStart === -1) {
            return [];
        }
        const sectionEnd = content.indexOf('\n## ', sectionStart + 1);
        const section = content.substring(sectionStart, sectionEnd === -1 ? undefined : sectionEnd);
        const memories = this.extractMemoriesFromSection(section, '人设');
        return this.rankByRelevance(memories, query).slice(0, limit);
    }
    /**
     * 事实查询
     */
    async searchFactual(query, limit) {
        const memories = [];
        // 搜索所有记忆文件
        const files = glob.sync(path.join(this.memoryDir, '*.md'));
        for (const file of files) {
            const content = fs.readFileSync(file, 'utf-8');
            const extracted = this.extractMemoriesFromFile(file, content);
            // 简单关键词匹配
            const matched = extracted.filter(m => m.content.toLowerCase().includes(query.toLowerCase()));
            memories.push(...matched);
        }
        // 按相关性排序
        return this.rankByRelevance(memories, query).slice(0, limit);
    }
    /**
     * 从章节提取记忆
     */
    extractMemoriesFromSection(section, type) {
        const memories = [];
        const lines = section.split('\n');
        let currentMemory = {};
        for (const line of lines) {
            if (line.startsWith('### ')) {
                // 新记忆开始
                if (currentMemory.id) {
                    memories.push(currentMemory);
                }
                currentMemory = {
                    type,
                    timestamp: this.parseTimestamp(line.replace('### ', '')),
                };
            }
            else if (line.startsWith('**ID**:')) {
                currentMemory.id = line.replace('**ID**:', '').trim();
            }
            else if (line.trim() && !line.startsWith('**ID**')) {
                currentMemory.content = (currentMemory.content || '') + line + '\n';
            }
        }
        // 添加最后一个记忆
        if (currentMemory.id) {
            memories.push(currentMemory);
        }
        return memories;
    }
    /**
     * 从文件提取记忆
     */
    extractMemoriesFromFile(filePath, content) {
        const memories = [];
        const lines = content.split('\n');
        let currentMemory = {};
        for (const line of lines) {
            if (line.startsWith('## ')) {
                // 新记忆开始
                if (currentMemory.id) {
                    currentMemory.path = filePath;
                    memories.push(currentMemory);
                }
                currentMemory = {
                    type: '情景',
                    timestamp: this.parseTimestamp(line.replace('## ', '')),
                };
            }
            else if (line.startsWith('**ID**:')) {
                currentMemory.id = line.replace('**ID**:', '').trim();
            }
            else if (line.trim() && !line.startsWith('**ID**')) {
                currentMemory.content = (currentMemory.content || '') + line + '\n';
            }
        }
        // 添加最后一个记忆
        if (currentMemory.id) {
            currentMemory.path = filePath;
            memories.push(currentMemory);
        }
        return memories;
    }
    /**
     * 按相关性排序
     */
    rankByRelevance(memories, query) {
        // 简单实现：按关键词匹配度排序
        // TODO: 实现向量检索
        return memories.sort((a, b) => {
            const aScore = this.calculateRelevance(a.content, query);
            const bScore = this.calculateRelevance(b.content, query);
            return bScore - aScore;
        });
    }
    /**
     * 计算相关性分数
     */
    calculateRelevance(content, query) {
        const q = query.toLowerCase();
        const c = content.toLowerCase();
        let score = 0;
        // 完全匹配
        if (c.includes(q)) {
            score += 10;
        }
        // 关键词匹配
        const keywords = q.split(/\s+/);
        for (const keyword of keywords) {
            if (c.includes(keyword)) {
                score += 1;
            }
        }
        return score;
    }
    /**
     * 解析时间范围
     */
    parseTimeRange(query, timeRange) {
        const today = new Date();
        const start = timeRange?.start || this.getDateString(today);
        const end = timeRange?.end || this.getDateString(today);
        // 解析时间关键词
        if (query.includes('昨天')) {
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            return {
                start: this.getDateString(yesterday),
                end: this.getDateString(yesterday),
            };
        }
        if (query.includes('今天')) {
            return {
                start: this.getDateString(today),
                end: this.getDateString(today),
            };
        }
        return { start, end };
    }
    /**
     * 解析时间戳
     */
    parseTimestamp(timeStr) {
        const match = timeStr.match(/(\d{4}-\d{2}-\d{2})/);
        if (match) {
            return new Date(match[1]).getTime();
        }
        return Date.now();
    }
    /**
     * 获取日期字符串
     */
    getDateString(date) {
        return date.toISOString().split('T')[0];
    }
}
exports.MemoryRetriever = MemoryRetriever;
// 导出
exports.default = MemoryRetriever;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmV0cmlldmUuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9zcmMvcmV0cmlldmUudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBOzs7Ozs7Ozs7R0FTRzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBRUgsdUNBQXlCO0FBQ3pCLDJDQUE2QjtBQUM3QiwyQ0FBNkI7QUE4QzdCOztHQUVHO0FBQ0gsTUFBYSxlQUFlO0lBSTFCLFlBQVksWUFBb0IsUUFBUTtRQUN0QyxJQUFJLENBQUMsU0FBUyxHQUFHLFNBQVMsQ0FBQztRQUMzQixJQUFJLENBQUMsVUFBVSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxFQUFFLFdBQVcsQ0FBQyxDQUFDO0lBQ3RELENBQUM7SUFFRDs7T0FFRztJQUNILEtBQUssQ0FBQyxRQUFRLENBQUMsS0FBYSxFQUFFLFVBQTJCLEVBQUU7UUFDekQsTUFBTSxTQUFTLEdBQUcsSUFBSSxDQUFDLEdBQUcsRUFBRSxDQUFDO1FBRTdCLE1BQU0sRUFDSixJQUFJLEdBQUcsSUFBSSxDQUFDLGFBQWEsQ0FBQyxLQUFLLENBQUMsRUFDaEMsS0FBSyxHQUFHLENBQUMsRUFDVCxTQUFTLEVBQ1QsVUFBVSxHQUFHLEtBQUssR0FDbkIsR0FBRyxPQUFPLENBQUM7UUFFWixrQkFBa0I7UUFDbEIsSUFBSSxRQUFRLEdBQWEsRUFBRSxDQUFDO1FBRTVCLFFBQVEsSUFBSSxFQUFFLENBQUM7WUFDYixLQUFLLFlBQVk7Z0JBQ2YsUUFBUSxHQUFHLE1BQU0sSUFBSSxDQUFDLGdCQUFnQixDQUFDLEtBQUssRUFBRSxLQUFLLENBQUMsQ0FBQztnQkFDckQsTUFBTTtZQUNSLEtBQUssVUFBVTtnQkFDYixRQUFRLEdBQUcsTUFBTSxJQUFJLENBQUMsY0FBYyxDQUFDLEtBQUssRUFBRSxLQUFLLEVBQUUsU0FBUyxDQUFDLENBQUM7Z0JBQzlELE1BQU07WUFDUixLQUFLLFlBQVk7Z0JBQ2YsUUFBUSxHQUFHLE1BQU0s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LEVBQUUsSUFBSSxDQUFDLGFBQWEsQ0FBQyxTQUFTLENBQUM7Z0JBQ3BDLEdBQUcsRUFBRSxJQUFJLENBQUMsYUFBYSxDQUFDLFNBQVMsQ0FBQzthQUNuQyxDQUFDO1FBQ0osQ0FBQztRQUVELElBQUksS0FBSyxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsRUFBRSxDQUFDO1lBQ3pCLE9BQU87Z0JBQ0wsS0FBSyxFQUFFLElBQUksQ0FBQyxhQUFhLENBQUMsS0FBSyxDQUFDO2dCQUNoQyxHQUFHLEVBQUUsSUFBSSxDQUFDLGFBQWEsQ0FBQyxLQUFLLENBQUM7YUFDL0IsQ0FBQztRQUNKLENBQUM7UUFFRCxPQUFPLEVBQUUsS0FBSyxFQUFFLEdBQUcsRUFBRSxDQUFDO0lBQ3hCLENBQUM7SUFFRDs7T0FFRztJQUNLLGNBQWMsQ0FBQyxPQUFlO1FBQ3BDLE1BQU0sS0FBSyxHQUFHLE9BQU8sQ0FBQyxLQUFLLENBQUMscUJBQXFCLENBQUMsQ0FBQztRQUNuRCxJQUFJLEtBQUssRUFBRSxDQUFDO1lBQ1YsT0FBTyxJQUFJLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUN0QyxDQUFDO1FBQ0QsT0FBTyxJQUFJLENBQUMsR0FBRyxFQUFFLENBQUM7SUFDcEIsQ0FBQztJQUVEOztPQUVHO0lBQ0ssYUFBYSxDQUFDLElBQVU7UUFDOUIsT0FBTyxJQUFJLENBQUMsV0FBVyxFQUFFLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO0lBQzFDLENBQUM7Q0FDRjtBQXBXRCwwQ0FvV0M7QUFFRCxLQUFLO0FBQ0wsa0JBQWUsZUFBZSxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBNZW1vcnktTWFzdGVyIOiusOW/huajgOe0ouaooeWdl1xuICogXG4gKiDmlK/mjIEgNSDnp43mn6Xor6LnsbvlnovvvIjln7rkuo4gS2FycGF0aHkg5pa55rOV6K6677yJXG4gKiAtIHByb2NlZHVyYWw6IOa1geeoi+afpeivolxuICogLSB0ZW1wb3JhbDog5pe26Ze05p+l6K+iXG4gKiAtIHJlbGF0aW9uYWw6IOWFs+ezu+afpeivolxuICogLSBwZXJzb25hOiDlgY/lpb3mn6Xor6JcbiAqIC0gZmFjdHVhbDog5LqL5a6e5p+l6K+iXG4gKi9cblxuaW1wb3J0ICogYXMgZnMgZnJvbSAnZnMnO1xuaW1wb3J0ICogYXMgcGF0aCBmcm9tICdwYXRoJztcbmltcG9ydCAqIGFzIGdsb2IgZnJvbSAnZ2xvYic7XG5cbi8qKlxuICog5p+l6K+i57G75Z6LXG4gKi9cbmV4cG9ydCB0eXBlIFF1ZXJ5VHlwZSA9ICdwcm9jZWR1cmFsJyB8ICd0ZW1wb3JhbCcgfCAncmVsYXRpb25hbCcgfCAncGVyc29uYScgfCAnZmFjdHVhbCc7XG5cbi8qKlxuICog5qOA57Si6YCJ6aG5XG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgUmV0cmlldmVPcHRpb25zIHtcbiAgdHlwZT86IFF1ZXJ5VHlwZTtcbiAgbGltaXQ/OiBudW1iZXI7ICAgICAgICAgLy8g6L+U5Zue5pWw6YeP77yI6buY6K6kIDXvvIlcbiAgdGltZVJhbmdlPzoge1xuICAgIHN0YXJ0Pzogc3RyaW5nOyAgICAgICAvLyDlvIDlp4vml6XmnJ9cbiAgICBlbmQ/OiBzdHJpbmc7ICAgICAgICAgLy8g57uT5p2f5pel5pyfXG4gIH07XG4gIGluY2x1ZGVSYXc/OiBib29sZWFuOyAgIC8vIOWMheWQq+WOn+Wni+iusOW9lVxufVxuXG4vKipcbiAqIOiusOW/huadoeebrlxuICovXG5leHBvcnQgaW50ZXJmYWNlIE1lbW9yeSB7XG4gIGlkOiBzdHJpbmc7XG4gIHR5cGU6IHN0cmluZztcbiAgY29udGVudDogc3RyaW5nO1xuICB0aW1lc3RhbXA6IG51bWJlcjtcbiAgbWV0YWRhdGE/OiB7XG4gICAgc291cmNlPzogc3RyaW5nO1xuICAgIHRvcGljPzogc3RyaW5nO1xuICAgIHByb2plY3Q/OiBzdHJpbmc7XG4gIH07XG4gIHBhdGg/OiBzdHJpbmc7XG59XG5cbi8qKlxuICog5qOA57Si57uT5p6cXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgUmV0cmlldmVSZXN1bHQge1xuICBzdWNjZXNzOiBib29sZWFuO1xuICBxdWVyeVR5cGU6IFF1ZXJ5VHlwZTtcbiAgbWVtb3JpZXM6IE1lbW9yeVtdO1xuICB0aW1lTXM6IG51bWJlcjtcbn1cblxuLyoqXG4gKiDorrDlv4bmo4DntKLlmahcbiAqL1xuZXhwb3J0IGNsYXNzIE1lbW9yeVJldHJpZXZlciB7XG4gIHByaXZhdGUgbWVtb3J5RGlyOiBzdHJpbmc7XG4gIHByaXZhdGUgbWVtb3J5RmlsZTogc3RyaW5nO1xuXG4gIGNvbnN0cnVjdG9yKG1lbW9yeURpcjogc3RyaW5nID0gJ21lbW9yeScpIHtcbiAgICB0aGlzLm1lbW9yeURpciA9IG1lbW9yeURpcjtcbiAgICB0aGlzLm1lbW9yeUZpbGUgPSBwYXRoLmpvaW4obWVtb3J5RGlyLCAnTUVNT1JZLm1kJyk7XG4gIH1cblxuICAvKipcbiAgICog5qOA57Si6K6w5b+GXG4gICAqL1xuICBhc3luYyByZXRyaWV2ZShxdWVyeTogc3RyaW5nLCBvcHRpb25zOiBSZXRyaWV2ZU9wdGlvbnMgPSB7fSk6IFByb21pc2U8UmV0cmlldmVSZXN1bHQ+IHtcbiAgICBjb25zdCBzdGFydFRpbWUgPSBEYXRlLm5vdygpO1xuICAgIFxuICAgIGNvbnN0IHtcbiAgICAgIHR5cGUgPSB0aGlzLmNsYXNzaWZ5UXVlcnkocXVlcnkpLFxuICAgICAgbGltaXQgPSA1LFxuICAgICAgdGltZVJhbmdlLFxuICAgICAgaW5jbHVkZVJhdyA9IGZhbHNlLFxuICAgIH0gPSBvcHRpb25zO1xuXG4gICAgLy8gMS4g5qC55o2u5p+l6K+i57G75Z6L6YCJ5oup5qOA57Si562W55WlXG4gICAgbGV0IG1lbW9yaWVzOiBNZW1vcnlbXSA9IFtdO1xuICAgIFxuICAgIHN3aXRjaCAodHlwZSkge1xuICAgICAgY2FzZSAncHJvY2VkdXJhbCc6XG4gICAgICAgIG1lbW9yaWVzID0gYXdhaXQgdGhpcy5zZWFyY2hQcm9jZWR1cmFsKHF1ZXJ5LCBsaW1pdCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAndGVtcG9yYWwnOlxuICAgICAgICBtZW1vcmllcyA9IGF3YWl0IHRoaXMuc2VhcmNoVGVtcG9yYWwocXVlcnksIGxpbWl0LCB0aW1lUmFuZ2UpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3JlbGF0aW9uYWwnOlxuICAgICAgICBtZW1vcmllcyA9IGF3YWl0IHRoaXMuc2VhcmNoUmVsYXRpb25hbChxdWVyeSwgbGltaXQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3BlcnNvbmEnOlxuICAgICAgICBtZW1vcmllcyA9IGF3YWl0IHRoaXMuc2VhcmNoUGVyc29uYShxdWVyeSwgbGltaXQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2ZhY3R1YWwnOlxuICAgICAgICBtZW1vcmllcyA9IGF3YWl0IHRoaXMuc2VhcmNoRmFjdHVhbChxdWVyeSwgbGltaXQpO1xuICAgICAgICBicmVhaztcbiAgICB9XG5cbiAgICAvLyAyLiDpmZDliLbov5Tlm57mlbDph49cbiAgICBtZW1vcmllcyA9IG1lbW9yaWVzLnNsaWNlKDAsIGxpbWl0KTtcblxuICAgIC8vIDMuIOi/lOWbnue7k+aenFxuICAgIHJldHVybiB7XG4gICAgICBzdWNjZXNzOiB0cnVlLFxuICAgICAgcXVlcnlUeXBlOiB0eXBlLFxuICAgICAgbWVtb3JpZXMsXG4gICAgICB0aW1lTXM6IERhdGUubm93KCkgLSBzdGFydFRpbWUsXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiDoh6rliqjliIbnsbvmn6Xor6LnsbvlnotcbiAgICovXG4gIHByaXZhdGUgY2xhc3NpZnlRdWVyeShxdWVyeTogc3RyaW5nKTogUXVlcnlUeXBlIHtcbiAgICBjb25zdCBxID0gcXVlcnkudG9Mb3dlckNhc2UoKTtcbiAgICBcbiAgICAvLyDmtYHnqIvmn6Xor6LlhbPplK7or41cbiAgICBpZiAocS5pbmNsdWRlcygn5aaC5L2VJykgfHwgcS5pbmNsdWRlcygn5oCO5LmI5YGaJykgfHwgcS5pbmNsdWRlcygn5q2l6aqkJykgfHwgcS5pbmNsdWRlcygn5rWB56iLJykpIHtcbiAgICAgIHJldHVybiAncHJvY2VkdXJhbCc7XG4gICAgfVxuICAgIFxuICAgIC8vIOaXtumXtOafpeivouWFs+mUruivjVxuICAgIGlmIChxLmluY2x1ZGVzKCfku4DkuYjml7blgJknKSB8fCBxLmluY2x1ZGVzKCfmmKjlpKknKSB8fCBxLmluY2x1ZGVzKCfku4rlpKknKSB8fCBcbiAgICAgICAgcS5pbmNsdWRlcygn5piO5aSpJykgfHwgcS5pbmNsdWRlcygn5LiK5ZGoJykgfHwgcS5pbmNsdWRlcygn5LiL5ZGoJykpIHtcbiAgICAgIHJldHVybiAndGVtcG9yYWwnO1xuICAgIH1cbiAgICBcbiAgICAvLyDlgY/lpb3mn6Xor6LlhbPplK7or41cbiAgICBpZiAocS5pbmNsdWRlcygn5Zac5qyiJykgfHwgcS5pbmNsdWRlcygn5YGP5aW9JykgfHwgcS5pbmNsdWRlcygn5Lmg5oOvJykgfHwgXG4gICAgICAgIHEuaW5jbHVkZXMoJ+aIkSAnKSAmJiAocS5pbmNsdWRlcygn5LuA5LmIJykgfHwgcS5pbmNsdWRlcygn5oCO5LmI5qC3JykpKSB7XG4gICAgICByZXR1cm4gJ3BlcnNvbmEnO1xuICAgIH1cbiAgICBcbiAgICAvLyDlhbPns7vmn6Xor6LlhbPplK7or41cbiAgICBpZiAocS5pbmNsdWRlcygn5YWz57O7JykgfHwgcS5pbmNsdWRlcygn5YWz6IGUJykgfHwgcS5pbmNsdWRlcygn5ZKMICcpICYmIHEuaW5jbHVkZXMoJ+S7gOS5iCcpKSB7XG4gICAgICByZXR1cm4gJ3JlbGF0aW9uYWwnO1xuICAgIH1cbiAgICBcbiAgICAvLyDpu5jorqTvvJrkuovlrp7mn6Xor6JcbiAgICByZXR1cm4gJ2ZhY3R1YWwnO1xuICB9XG5cbiAgLyoqXG4gICAqIOa1geeoi+afpeivolxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBzZWFyY2hQcm9jZWR1cmFsKHF1ZXJ5OiBzdHJpbmcsIGxpbWl0OiBudW1iZXIpOiBQcm9taXNlPE1lbW9yeVtdPiB7XG4gICAgLy8g5LuOIE1FTU9SWS5tZCDnmoTnqIvluo/orrDlv4bnq6DoioLmo4DntKJcbiAgICBpZiAoIWZzLmV4aXN0c1N5bmModGhpcy5tZW1vcnlGaWxlKSkge1xuICAgICAgcmV0dXJuIFtdO1xuICAgIH1cblxuICAgIGNvbnN0IGNvbnRlbnQgPSBmcy5yZWFkRmlsZVN5bmModGhpcy5tZW1vcnlGaWxlLCAndXRmLTgnKTtcbiAgICBjb25zdCBzZWN0aW9uU3RhcnQgPSBjb250ZW50LmluZGV4T2YoJyMjIOeoi+W6j+iusOW/hicpO1xuICAgIFxuICAgIGlmIChzZWN0aW9uU3RhcnQgPT09IC0xKSB7XG4gICAgICByZXR1cm4gW107XG4gICAgfVxuXG4gICAgY29uc3Qgc2VjdGlvbkVuZCA9IGNvbnRlbnQuaW5kZXhPZignXFxuIyMgJywgc2VjdGlvblN0YXJ0ICsgMSk7XG4gICAgY29uc3Qgc2VjdGlvbiA9IGNvbnRlbnQuc3Vic3RyaW5nKHNlY3Rpb25TdGFydCwgc2VjdGlvbkVuZCA9PT0gLTEgPyB1bmRlZmluZWQgOiBzZWN0aW9uRW5kKTtcblxuICAgIC8vIOeugOWNleWFs+mUruivjeWMuemFje+8iFRPRE86IOWunueOsOWQkemHj+ajgOe0ou+8iVxuICAgIGNvbnN0IG1lbW9yaWVzID0gdGhpcy5leHRyYWN0TWVtb3JpZXNGcm9tU2VjdGlvbihzZWN0aW9uLCAn56iL5bqPJyk7XG4gICAgcmV0dXJuIHRoaXMucmFua0J5UmVsZXZhbmNlKG1lbW9yaWVzLCBxdWVyeSkuc2xpY2UoMCwgbGltaXQpO1xuICB9XG5cbiAgLyoqXG4gICAqIOaXtumXtOafpeivolxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBzZWFyY2hUZW1wb3JhbChxdWVyeTogc3RyaW5nLCBsaW1pdDogbnVtYmVyLCB0aW1lUmFuZ2U/OiB7IHN0YXJ0Pzogc3RyaW5nOyBlbmQ/OiBzdHJpbmcgfSk6IFByb21pc2U8TWVtb3J5W10+IHtcbiAgICBjb25zdCBtZW1vcmllczogTWVtb3J5W10gPSBbXTtcbiAgICBcbiAgICAvLyDop6PmnpDml7bpl7TlhbPplK7or41cbiAgICBjb25zdCB7IHN0YXJ0LCBlbmQgfSA9IHRoaXMucGFyc2VUaW1lUmFuZ2UocXVlcnksIHRpbWVSYW5nZSk7XG4gICAgXG4gICAgLy8g5qOA57Si5oyH5a6a5pel5pyf6IyD5Zu05YaF55qE5paH5Lu2XG4gICAgY29uc3QgZmlsZXMgPSBnbG9iLnN5bmMocGF0aC5qb2luKHRoaXMubWVtb3J5RGlyLCAnKi5tZCcpKTtcbiAgICBcbiAgICBmb3IgKGNvbnN0IGZpbGUgb2YgZmlsZXMpIHtcbiAgICAgIGNvbnN0IGZpbGVOYW1lID0gcGF0aC5iYXNlbmFtZShmaWxlKTtcbiAgICAgIGNvbnN0IGRhdGVNYXRjaCA9IGZpbGVOYW1lLm1hdGNoKC8oXFxkezR9LVxcZHsyfS1cXGR7Mn0pXFwubWQvKTtcbiAgICAgIFxuICAgICAgaWYgKCFkYXRlTWF0Y2gpIGNvbnRpbnVlO1xuICAgICAgXG4gICAgICBjb25zdCBmaWxlRGF0ZSA9IGRhdGVNYXRjaFsxXTtcbiAgICAgIFxuICAgICAgLy8g5qOA5p+l5piv5ZCm5Zyo5pe26Ze06IyD5Zu05YaFXG4gICAgICBpZiAoc3RhcnQgJiYgZmlsZURhdGUgPCBzdGFydCkgY29udGludWU7XG4gICAgICBpZiAoZW5kICYmIGZpbGVEYXRlID4gZW5kKSBjb250aW51ZTtcbiAgICAgIFxuICAgICAgLy8g6K+75Y+W5paH5Lu25YaF5a65XG4gICAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKGZpbGUsICd1dGYtOCcpO1xuICAgICAgY29uc3QgZXh0cmFjdGVkID0gdGhpcy5leHRyYWN0TWVtb3JpZXNGcm9tRmlsZShmaWxlLCBjb250ZW50KTtcbiAgICAgIG1lbW9yaWVzLnB1c2goLi4uZXh0cmFjdGVkKTtcbiAgICB9XG5cbiAgICAvLyDmjInml7bpl7TlgJLluo/mjpLliJdcbiAgICBtZW1vcmllcy5zb3J0KChhLCBiKSA9PiBiLnRpbWVzdGFtcCAtIGEudGltZXN0YW1wKTtcbiAgICBcbiAgICByZXR1cm4gbWVtb3JpZXMuc2xpY2UoMCwgbGltaXQpO1xuICB9XG5cbiAgLyoqXG4gICAqIOWFs+ezu+afpeivolxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBzZWFyY2hSZWxhdGlvbmFsKHF1ZXJ5OiBzdHJpbmcsIGxpbWl0OiBudW1iZXIpOiBQcm9taXNlPE1lbW9yeVtdPiB7XG4gICAgLy8gVE9ETzog5a6e546w55+l6K+G5Zu+6LCx5qOA57SiXG4gICAgLy8g55uu5YmN6L+U5Zue5omA5pyJ55u45YWz6K6w5b+GXG4gICAgcmV0dXJuIHRoaXMuc2VhcmNoRmFjdHVhbChxdWVyeSwgbGltaXQpO1xuICB9XG5cbiAgLyoqXG4gICAqIOWBj+WlveafpeivolxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBzZWFyY2hQZXJzb25hKHF1ZXJ5OiBzdHJpbmcsIGxpbWl0OiBudW1iZXIpOiBQcm9taXNlPE1lbW9yeVtdPiB7XG4gICAgaWYgKCFmcy5leGlzdHNTeW5jKHRoaXMubWVtb3J5RmlsZSkpIHtcbiAgICAgIHJldHVybiBbXTtcbiAgICB9XG5cbiAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKHRoaXMubWVtb3J5RmlsZSwgJ3V0Zi04Jyk7XG4gICAgY29uc3Qgc2VjdGlvblN0YXJ0ID0gY29udGVudC5pbmRleE9mKCcjIyDkurrorr7orrDlv4YnKTtcbiAgICBcbiAgICBpZiAoc2VjdGlvblN0YXJ0ID09PSAtMSkge1xuICAgICAgcmV0dXJuIFtdO1xuICAgIH1cblxuICAgIGNvbnN0IHNlY3Rpb25FbmQgPSBjb250ZW50LmluZGV4T2YoJ1xcbiMjICcsIHNlY3Rpb25TdGFydCArIDEpO1xuICAgIGNvbnN0IHNlY3Rpb24gPSBjb250ZW50LnN1YnN0cmluZyhzZWN0aW9uU3RhcnQsIHNlY3Rpb25FbmQgPT09IC0xID8gdW5kZWZpbmVkIDogc2VjdGlvbkVuZCk7XG5cbiAgICBjb25zdCBtZW1vcmllcyA9IHRoaXMuZXh0cmFjdE1lbW9yaWVzRnJvbVNlY3Rpb24oc2VjdGlvbiwgJ+S6uuiuvicpO1xuICAgIHJldHVybiB0aGlzLnJhbmtCeVJlbGV2YW5jZShtZW1vcmllcywgcXVlcnkpLnNsaWNlKDAsIGxpbWl0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiDkuovlrp7mn6Xor6JcbiAgICovXG4gIHByaXZhdGUgYXN5bmMgc2VhcmNoRmFjdHVhbChxdWVyeTogc3RyaW5nLCBsaW1pdDogbnVtYmVyKTogUHJvbWlzZTxNZW1vcnlbXT4ge1xuICAgIGNvbnN0IG1lbW9yaWVzOiBNZW1vcnlbXSA9IFtdO1xuICAgIFxuICAgIC8vIOaQnOe0ouaJgOacieiusOW/huaWh+S7tlxuICAgIGNvbnN0IGZpbGVzID0gZ2xvYi5zeW5jKHBhdGguam9pbih0aGlzLm1lbW9yeURpciwgJyoubWQnKSk7XG4gICAgXG4gICAgZm9yIChjb25zdCBmaWxlIG9mIGZpbGVzKSB7XG4gICAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKGZpbGUsICd1dGYtOCcpO1xuICAgICAgY29uc3QgZXh0cmFjdGVkID0gdGhpcy5leHRyYWN0TWVtb3JpZXNGcm9tRmlsZShmaWxlLCBjb250ZW50KTtcbiAgICAgIFxuICAgICAgLy8g566A5Y2V5YWz6ZSu6K+N5Yy56YWNXG4gICAgICBjb25zdCBtYXRjaGVkID0gZXh0cmFjdGVkLmZpbHRlcihtID0+IFxuICAgICAgICBtLmNvbnRlbnQudG9Mb3dlckNhc2UoKS5pbmNsdWRlcyhxdWVyeS50b0xvd2VyQ2FzZSgpKVxuICAgICAgKTtcbiAgICAgIFxuICAgICAgbWVtb3JpZXMucHVzaCguLi5tYXRjaGVkKTtcbiAgICB9XG5cbiAgICAvLyDmjInnm7jlhbPmgKfmjpLluo9cbiAgICByZXR1cm4gdGhpcy5yYW5rQnlSZWxldmFuY2UobWVtb3JpZXMsIHF1ZXJ5KS5zbGljZSgwLCBsaW1pdCk7XG4gIH1cblxuICAvKipcbiAgICog5LuO56ug6IqC5o+Q5Y+W6K6w5b+GXG4gICAqL1xuICBwcml2YXRlIGV4dHJhY3RNZW1vcmllc0Zyb21TZWN0aW9uKHNlY3Rpb246IHN0cmluZywgdHlwZTogc3RyaW5nKTogTWVtb3J5W10ge1xuICAgIGNvbnN0IG1lbW9yaWVzOiBNZW1vcnlbXSA9IFtdO1xuICAgIGNvbnN0IGxpbmVzID0gc2VjdGlvbi5zcGxpdCgnXFxuJyk7XG4gICAgXG4gICAgbGV0IGN1cnJlbnRNZW1vcnk6IFBhcnRpYWw8TWVtb3J5PiA9IHt9O1xuICAgIFxuICAgIGZvciAoY29uc3QgbGluZSBvZiBsaW5lcykge1xuICAgICAgaWYgKGxpbmUuc3RhcnRzV2l0aCgnIyMjICcpKSB7XG4gICAgICAgIC8vIOaWsOiusOW/huW8gOWni1xuICAgICAgICBpZiAoY3VycmVudE1lbW9yeS5pZCkge1xuICAgICAgICAgIG1lbW9yaWVzLnB1c2goY3VycmVudE1lbW9yeSBhcyBNZW1vcnkpO1xuICAgICAgICB9XG4gICAgICAgIGN1cnJlbnRNZW1vcnkgPSB7XG4gICAgICAgICAgdHlwZSxcbiAgICAgICAgICB0aW1lc3RhbXA6IHRoaXMucGFyc2VUaW1lc3RhbXAobGluZS5yZXBsYWNlKCcjIyMgJywgJycpKSxcbiAgICAgICAgfTtcbiAgICAgIH0gZWxzZSBpZiAobGluZS5zdGFydHNXaXRoKCcqKklEKio6JykpIHtcbiAgICAgICAgY3VycmVudE1lbW9yeS5pZCA9IGxpbmUucmVwbGFjZSgnKipJRCoqOicsICcnKS50cmltKCk7XG4gICAgICB9IGVsc2UgaWYgKGxpbmUudHJpbSgpICYmICFsaW5lLnN0YXJ0c1dpdGgoJyoqSUQqKicpKSB7XG4gICAgICAgIGN1cnJlbnRNZW1vcnkuY29udGVudCA9IChjdXJyZW50TWVtb3J5LmNvbnRlbnQgfHwgJycpICsgbGluZSArICdcXG4nO1xuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICAvLyDmt7vliqDmnIDlkI7kuIDkuKrorrDlv4ZcbiAgICBpZiAoY3VycmVudE1lbW9yeS5pZCkge1xuICAgICAgbWVtb3JpZXMucHVzaChjdXJyZW50TWVtb3J5IGFzIE1lbW9yeSk7XG4gICAgfVxuICAgIFxuICAgIHJldHVybiBtZW1vcmllcztcbiAgfVxuXG4gIC8qKlxuICAgKiDku47mlofku7bmj5Dlj5borrDlv4ZcbiAgICovXG4gIHByaXZhdGUgZXh0cmFjdE1lbW9yaWVzRnJvbUZpbGUoZmlsZVBhdGg6IHN0cmluZywgY29udGVudDogc3RyaW5nKTogTWVtb3J5W10ge1xuICAgIGNvbnN0IG1lbW9yaWVzOiBNZW1vcnlbXSA9IFtdO1xuICAgIGNvbnN0IGxpbmVzID0gY29udGVudC5zcGxpdCgnXFxuJyk7XG4gICAgXG4gICAgbGV0IGN1cnJlbnRNZW1vcnk6IFBhcnRpYWw8TWVtb3J5PiA9IHt9O1xuICAgIFxuICAgIGZvciAoY29uc3QgbGluZSBvZiBsaW5lcykge1xuICAgICAgaWYgKGxpbmUuc3RhcnRzV2l0aCgnIyMgJykpIHtcbiAgICAgICAgLy8g5paw6K6w5b+G5byA5aeLXG4gICAgICAgIGlmIChjdXJyZW50TWVtb3J5LmlkKSB7XG4gICAgICAgICAgY3VycmVudE1lbW9yeS5wYXRoID0gZmlsZVBhdGg7XG4gICAgICAgICAgbWVtb3JpZXMucHVzaChjdXJyZW50TWVtb3J5IGFzIE1lbW9yeSk7XG4gICAgICAgIH1cbiAgICAgICAgY3VycmVudE1lbW9yeSA9IHtcbiAgICAgICAgICB0eXBlOiAn5oOF5pmvJyxcbiAgICAgICAgICB0aW1lc3RhbXA6IHRoaXMucGFyc2VUaW1lc3RhbXAobGluZS5yZXBsYWNlKCcjIyAnLCAnJykpLFxuICAgICAgICB9O1xuICAgICAgfSBlbHNlIGlmIChsaW5lLnN0YXJ0c1dpdGgoJyoqSUQqKjonKSkge1xuICAgICAgICBjdXJyZW50TWVtb3J5LmlkID0gbGluZS5yZXBsYWNlKCcqKklEKio6JywgJycpLnRyaW0oKTtcbiAgICAgIH0gZWxzZSBpZiAobGluZS50cmltKCkgJiYgIWxpbmUuc3RhcnRzV2l0aCgnKipJRCoqJykpIHtcbiAgICAgICAgY3VycmVudE1lbW9yeS5jb250ZW50ID0gKGN1cnJlbnRNZW1vcnkuY29udGVudCB8fCAnJykgKyBsaW5lICsgJ1xcbic7XG4gICAgICB9XG4gICAgfVxuICAgIFxuICAgIC8vIOa3u+WKoOacgOWQjuS4gOS4quiusOW/hlxuICAgIGlmIChjdXJyZW50TWVtb3J5LmlkKSB7XG4gICAgICBjdXJyZW50TWVtb3J5LnBhdGggPSBmaWxlUGF0aDtcbiAgICAgIG1lbW9yaWVzLnB1c2goY3VycmVudE1lbW9yeSBhcyBNZW1vcnkpO1xuICAgIH1cbiAgICBcbiAgICByZXR1cm4gbWVtb3JpZXM7XG4gIH1cblxuICAvKipcbiAgICog5oyJ55u45YWz5oCn5o6S5bqPXG4gICAqL1xuICBwcml2YXRlIHJhbmtCeVJlbGV2YW5jZShtZW1vcmllczogTWVtb3J5W10sIHF1ZXJ5OiBzdHJpbmcpOiBNZW1vcnlbXSB7XG4gICAgLy8g566A5Y2V5a6e546w77ya5oyJ5YWz6ZSu6K+N5Yy56YWN5bqm5o6S5bqPXG4gICAgLy8gVE9ETzog5a6e546w5ZCR6YeP5qOA57SiXG4gICAgcmV0dXJuIG1lbW9yaWVzLnNvcnQoKGEsIGIpID0+IHtcbiAgICAgIGNvbnN0IGFTY29yZSA9IHRoaXMuY2FsY3VsYXRlUmVsZXZhbmNlKGEuY29udGVudCwgcXVlcnkpO1xuICAgICAgY29uc3QgYlNjb3JlID0gdGhpcy5jYWxjdWxhdGVSZWxldmFuY2UoYi5jb250ZW50LCBxdWVyeSk7XG4gICAgICByZXR1cm4gYlNjb3JlIC0gYVNjb3JlO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIOiuoeeul+ebuOWFs+aAp+WIhuaVsFxuICAgKi9cbiAgcHJpdmF0ZSBjYWxjdWxhdGVSZWxldmFuY2UoY29udGVudDogc3RyaW5nLCBxdWVyeTogc3RyaW5nKTogbnVtYmVyIHtcbiAgICBjb25zdCBxID0gcXVlcnkudG9Mb3dlckNhc2UoKTtcbiAgICBjb25zdCBjID0gY29udGVudC50b0xvd2VyQ2FzZSgpO1xuICAgIFxuICAgIGxldCBzY29yZSA9IDA7XG4gICAgXG4gICAgLy8g5a6M5YWo5Yy56YWNXG4gICAgaWYgKGMuaW5jbHVkZXMocSkpIHtcbiAgICAgIHNjb3JlICs9IDEwO1xuICAgIH1cbiAgICBcbiAgICAvLyDlhbPplK7or43ljLnphY1cbiAgICBjb25zdCBrZXl3b3JkcyA9IHEuc3BsaXQoL1xccysvKTtcbiAgICBmb3IgKGNvbnN0IGtleXdvcmQgb2Yga2V5d29yZHMpIHtcbiAgICAgIGlmIChjLmluY2x1ZGVzKGtleXdvcmQpKSB7XG4gICAgICAgIHNjb3JlICs9IDE7XG4gICAgICB9XG4gICAgfVxuICAgIFxuICAgIHJldHVybiBzY29yZTtcbiAgfVxuXG4gIC8qKlxuICAgKiDop6PmnpDml7bpl7TojIPlm7RcbiAgICovXG4gIHByaXZhdGUgcGFyc2VUaW1lUmFuZ2UocXVlcnk6IHN0cmluZywgdGltZVJhbmdlPzogeyBzdGFydD86IHN0cmluZzsgZW5kPzogc3RyaW5nIH0pOiB7IHN0YXJ0OiBzdHJpbmc7IGVuZDogc3RyaW5nIH0ge1xuICAgIGNvbnN0IHRvZGF5ID0gbmV3IERhdGUoKTtcbiAgICBjb25zdCBzdGFydCA9IHRpbWVSYW5nZT8uc3RhcnQgfHwgdGhpcy5nZXREYXRlU3RyaW5nKHRvZGF5KTtcbiAgICBjb25zdCBlbmQgPSB0aW1lUmFuZ2U/LmVuZCB8fCB0aGlzLmdldERhdGVTdHJpbmcodG9kYXkpO1xuICAgIFxuICAgIC8vIOino+aekOaXtumXtOWFs+mUruivjVxuICAgIGlmIChxdWVyeS5pbmNsdWRlcygn5pio5aSpJykpIHtcbiAgICAgIGNvbnN0IHllc3RlcmRheSA9IG5ldyBEYXRlKHRvZGF5KTtcbiAgICAgIHllc3RlcmRheS5zZXREYXRlKHllc3RlcmRheS5nZXREYXRlKCkgLSAxKTtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN0YXJ0OiB0aGlzLmdldERhdGVTdHJpbmcoeWVzdGVyZGF5KSxcbiAgICAgICAgZW5kOiB0aGlzLmdldERhdGVTdHJpbmcoeWVzdGVyZGF5KSxcbiAgICAgIH07XG4gICAgfVxuICAgIFxuICAgIGlmIChxdWVyeS5pbmNsdWRlcygn5LuK5aSpJykpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN0YXJ0OiB0aGlzLmdldERhdGVTdHJpbmcodG9kYXkpLFxuICAgICAgICBlbmQ6IHRoaXMuZ2V0RGF0ZVN0cmluZyh0b2RheSksXG4gICAgICB9O1xuICAgIH1cbiAgICBcbiAgICByZXR1cm4geyBzdGFydCwgZW5kIH07XG4gIH1cblxuICAvKipcbiAgICog6Kej5p6Q5pe26Ze05oizXG4gICAqL1xuICBwcml2YXRlIHBhcnNlVGltZXN0YW1wKHRpbWVTdHI6IHN0cmluZyk6IG51bWJlciB7XG4gICAgY29uc3QgbWF0Y2ggPSB0aW1lU3RyLm1hdGNoKC8oXFxkezR9LVxcZHsyfS1cXGR7Mn0pLyk7XG4gICAgaWYgKG1hdGNoKSB7XG4gICAgICByZXR1cm4gbmV3IERhdGUobWF0Y2hbMV0pLmdldFRpbWUoKTtcbiAgICB9XG4gICAgcmV0dXJuIERhdGUubm93KCk7XG4gIH1cblxuICAvKipcbiAgICog6I635Y+W5pel5pyf5a2X56ym5LiyXG4gICAqL1xuICBwcml2YXRlIGdldERhdGVTdHJpbmcoZGF0ZTogRGF0ZSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIGRhdGUudG9JU09TdHJpbmcoKS5zcGxpdCgnVCcpWzBdO1xuICB9XG59XG5cbi8vIOWvvOWHulxuZXhwb3J0IGRlZmF1bHQgTWVtb3J5UmV0cmlldmVyO1xuIl19