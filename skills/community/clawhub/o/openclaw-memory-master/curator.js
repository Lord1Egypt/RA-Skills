"use strict";
/**
 * Memory-Master 记忆压缩模块
 *
 * 基于 Claude Code 六层压缩设计
 * 简化为 3 阶段压缩：
 * - L1: 原始记录（保留 7 天）
 * - L2: 摘要提炼（保留 30 天）
 * - L3: 关键事实（永久保留）
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
exports.MemoryCompactor = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const glob = __importStar(require("glob"));
/**
 * 记忆压缩器
 */
class MemoryCompactor {
    constructor(memoryDir = 'memory') {
        this.memoryDir = memoryDir;
    }
    /**
     * 执行压缩
     */
    async compact(options = {}) {
        const { force = false, level = 'L2', dryRun = false, } = options;
        const details = [];
        let totalCompressed = 0;
        let totalSavedTokens = 0;
        let totalOriginalTokens = 0;
        // 1. 获取所有记忆文件
        const files = glob.sync(path.join(this.memoryDir, '*.md'));
        // 2. 遍历文件
        for (const file of files) {
            const fileName = path.basename(file);
            // 跳过 MEMORY.md（长期记忆不自动压缩）
            if (fileName === 'MEMORY.md') {
                continue;
            }
            // 解析日期
            const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})\.md/);
            if (!dateMatch)
                continue;
            const fileDate = dateMatch[1];
            const daysOld = this.getDaysOld(fileDate);
            // 3. 根据天数决定压缩级别
            let targetLevel;
            if (daysOld <= 7) {
                targetLevel = 'L1'; // 7 天内保留原始
            }
            else if (daysOld <= 30) {
                targetLevel = 'L2'; // 30 天内摘要
            }
            else {
                targetLevel = 'L3'; // 30 天以上关键事实
            }
            // 如果指定了级别，使用指定级别
            if (level) {
                targetLevel = level;
            }
            // 4. 执行压缩
            const content = fs.readFileSync(file, 'utf-8');
            const compressed = await this.compressContent(content, targetLevel, file);
            if (compressed) {
                details.push(...compressed);
                for (const detail of compressed) {
                    totalCompressed++;
                    totalSavedTokens += detail.savedTokens;
                    const compressionRate = targetLevel === 'L1' ? 0 : targetLevel === 'L2' ? 0.5 : 0.8;
                    totalOriginalTokens += detail.savedTokens / (1 - compressionRate);
                }
                // 5. 写入文件（如果不是 dryRun）
                if (!dryRun) {
                    const newContent = this.applyCompression(content, compressed);
                    fs.writeFileSync(file, newContent, 'utf-8');
                }
            }
        }
        // 6. 返回结果
        return {
            success: true,
            compressed: totalCompressed,
            savedTokens: totalSavedTokens,
            compressionRate: totalOriginalTokens > 0 ? totalSavedTokens / totalOriginalTokens : 0,
            details: dryRun ? details : undefined,
        };
    }
    /**
     * 压缩内容
     */
    async compressContent(content, level, filePath) {
        const details = [];
        // 提取记忆块
        const memories = this.extractMemories(content);
        for (const memory of memories) {
            const compressed = this.compressMemory(memory.content, level);
            if (compressed && compressed.to !== memory.content) {
                const savedTokens = this.estimateTokens(memory.content) - this.estimateTokens(compressed.to);
                details.push({
                    id: memory.id,
                    from: memory.content,
                    to: compressed.to,
                    savedTokens,
                    level,
                });
            }
        }
        return details.length > 0 ? details : null;
    }
    /**
     * 压缩单条记忆
     */
    compressMemory(content, level) {
        const original = content;
        switch (level) {
            case 'L1':
                // L1: 保留原始，不做压缩
                return null;
            case 'L2':
                // L2: 摘要提炼
                const summary = this.generateSummary(original);
                return {
                    from: original,
                    to: summary,
                };
            case 'L3':
                // L3: 只保留关键事实
                const facts = this.extractKeyFacts(original);
                return {
                    from: original,
                    to: facts,
                };
            default:
                return null;
        }
    }
    /**
     * 生成摘要
     */
    generateSummary(content) {
        // 简单实现：提取前 3 个非空行
        // TODO: 使用 LLM 生成摘要
        const lines = content.split('\n').filter(line => line.trim());
        const summary = lines.slice(0, 3).join('\n');
        return summary + '\n\n[摘要 - 原始内容已压缩]';
    }
    /**
     * 提取关键事实
     */
    extractKeyFacts(content) {
        // 简单实现：提取包含关键词的行
        // TODO: 使用 LLM 提取关键事实
        const keywords = ['记住', '重要', '必须', '关键', '决定', '结论'];
        const lines = content.split('\n');
        const keyLines = lines.filter(line => keywords.some(keyword => line.includes(keyword)));
        if (keyLines.length === 0) {
            // 如果没有关键词，保留第一行
            return lines[0] + '\n\n[关键事实 - 原始内容已压缩]';
        }
        return keyLines.join('\n') + '\n\n[关键事实 - 原始内容已压缩]';
    }
    /**
     * 应用压缩
     */
    applyCompression(content, details) {
        let result = content;
        for (const detail of details) {
            result = result.replace(detail.from, detail.to);
        }
        return result;
    }
    /**
     * 提取记忆
     */
    extractMemories(content) {
        const memories = [];
        const lines = content.split('\n');
        let currentId = '';
        let currentContent = '';
        for (const line of lines) {
            if (line.startsWith('**ID**:')) {
                currentId = line.replace('**ID**:', '').trim();
            }
            else if (line.startsWith('## ') || line.startsWith('### ')) {
                if (currentId && currentContent) {
                    memories.push({ id: currentId, content: currentContent });
                }
                currentContent = line + '\n';
            }
            else if (currentId) {
                currentContent += line + '\n';
            }
        }
        if (currentId && currentContent) {
            memories.push({ id: currentId, content: currentContent });
        }
        return memories;
    }
    /**
     * 估算 token 数
     */
    estimateTokens(text) {
        // 简单估算：中文字符数 / 2 + 英文字符数
        const chinese = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
        const english = (text.match(/[a-zA-Z0-9]/g) || []).length;
        return Math.floor(chinese / 2 + english / 4);
    }
    /**
     * 计算文件天数
     */
    getDaysOld(dateStr) {
        const fileDate = new Date(dateStr);
        const today = new Date();
        const diff = today.getTime() - fileDate.getTime();
        return Math.floor(diff / (1000 * 60 * 60 * 24));
    }
}
exports.MemoryCompactor = MemoryCompactor;
// 导出
exports.default = MemoryCompactor;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29tcGFjdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NyYy9jb21wYWN0LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7QUFBQTs7Ozs7Ozs7R0FRRzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBRUgsdUNBQXlCO0FBQ3pCLDJDQUE2QjtBQUM3QiwyQ0FBNkI7QUFzQzdCOztHQUVHO0FBQ0gsTUFBYSxlQUFlO0lBRzFCLFlBQVksWUFBb0IsUUFBUTtRQUN0QyxJQUFJLENBQUMsU0FBUyxHQUFHLFNBQVMsQ0FBQztJQUM3QixDQUFDO0lBRUQ7O09BRUc7SUFDSCxLQUFLLENBQUMsT0FBTyxDQUFDLFVBQTBCLEVBQUU7UUFDeEMsTUFBTSxFQUNKLEtBQUssR0FBRyxLQUFLLEVBQ2IsS0FBSyxHQUFHLElBQUksRUFDWixNQUFNLEdBQUcsS0FBSyxHQUNmLEdBQUcsT0FBTyxDQUFDO1FBRVosTUFBTSxPQUFPLEdBQW9CLEVBQUUsQ0FBQztRQUNwQyxJQUFJLGVBQWUsR0FBRyxDQUFDLENBQUM7UUFDeEIsSUFBSSxnQkFBZ0IsR0FBRyxDQUFDLENBQUM7UUFDekIsSUFBSSxtQkFBbUIsR0FBRyxDQUFDLENBQUM7UUFFNUIsY0FBYztRQUNkLE1BQU0sS0FBSyxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxFQUFFLE1BQU0sQ0FBQyxDQUFDLENBQUM7UUFFM0QsVUFBVTtRQUNWLEtBQUssTUFBTSxJQUFJLElBQUksS0FBSyxFQUFFLENBQUM7WUFDekIsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUVyQywwQkFBMEI7WUFDMUIsSUFBSSxRQUFRLEtBQUssV0FBVyxFQUFFLENBQUM7Z0JBQzdCLFNBQVM7WUFDWCxDQUFDO1lBRUQsT0FBTztZQUNQLE1BQU0sU0FBUyxHQUFHLFFBQVEsQ0FBQyxLQUFLLENBQUMseUJB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UUFFRCxJQUFJLFNBQVMsSUFBSSxjQUFjLEVBQUUsQ0FBQztZQUNoQyxRQUFRLENBQUMsSUFBSSxDQUFDLEVBQUUsRUFBRSxFQUFFLFNBQVMsRUFBRSxPQUFPLEVBQUUsY0FBYyxFQUFFLENBQUMsQ0FBQztRQUM1RCxDQUFDO1FBRUQsT0FBTyxRQUFRLENBQUM7SUFDbEIsQ0FBQztJQUVEOztPQUVHO0lBQ0ssY0FBYyxDQUFDLElBQVk7UUFDakMseUJBQXlCO1FBQ3pCLE1BQU0sT0FBTyxHQUFHLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxrQkFBa0IsQ0FBQyxJQUFJLEVBQUUsQ0FBQyxDQUFDLE1BQU0sQ0FBQztRQUM5RCxNQUFNLE9BQU8sR0FBRyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsY0FBYyxDQUFDLElBQUksRUFBRSxDQUFDLENBQUMsTUFBTSxDQUFDO1FBQzFELE9BQU8sSUFBSSxDQUFDLEtBQUssQ0FBQyxPQUFPLEdBQUcsQ0FBQyxHQUFHLE9BQU8sR0FBRyxDQUFDLENBQUMsQ0FBQztJQUMvQyxDQUFDO0lBRUQ7O09BRUc7SUFDSyxVQUFVLENBQUMsT0FBZTtRQUNoQyxNQUFNLFFBQVEsR0FBRyxJQUFJLElBQUksQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUNuQyxNQUFNLEtBQUssR0FBRyxJQUFJLElBQUksRUFBRSxDQUFDO1FBQ3pCLE1BQU0sSUFBSSxHQUFHLEtBQUssQ0FBQyxPQUFPLEVBQUUsR0FBRyxRQUFRLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDbEQsT0FBTyxJQUFJLENBQUMsS0FBSyxDQUFDLElBQUksR0FBRyxDQUFDLElBQUksR0FBRyxFQUFFLEdBQUcsRUFBRSxHQUFHLEVBQUUsQ0FBQyxDQUFDLENBQUM7SUFDbEQsQ0FBQztDQUNGO0FBMVBELDBDQTBQQztBQUVELEtBQUs7QUFDTCxrQkFBZSxlQUFlLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIE1lbW9yeS1NYXN0ZXIg6K6w5b+G5Y6L57yp5qih5Z2XXG4gKiBcbiAqIOWfuuS6jiBDbGF1ZGUgQ29kZSDlha3lsYLljovnvKnorr7orqFcbiAqIOeugOWMluS4uiAzIOmYtuauteWOi+e8qe+8mlxuICogLSBMMTog5Y6f5aeL6K6w5b2V77yI5L+d55WZIDcg5aSp77yJXG4gKiAtIEwyOiDmkZjopoHmj5DngrzvvIjkv53nlZkgMzAg5aSp77yJXG4gKiAtIEwzOiDlhbPplK7kuovlrp7vvIjmsLjkuYXkv53nlZnvvIlcbiAqL1xuXG5pbXBvcnQgKiBhcyBmcyBmcm9tICdmcyc7XG5pbXBvcnQgKiBhcyBwYXRoIGZyb20gJ3BhdGgnO1xuaW1wb3J0ICogYXMgZ2xvYiBmcm9tICdnbG9iJztcblxuLyoqXG4gKiDljovnvKnnuqfliKtcbiAqL1xuZXhwb3J0IHR5cGUgQ29tcGFjdExldmVsID0gJ0wxJyB8ICdMMicgfCAnTDMnO1xuXG4vKipcbiAqIOWOi+e8qemAiemhuVxuICovXG5leHBvcnQgaW50ZXJmYWNlIENvbXBhY3RPcHRpb25zIHtcbiAgZm9yY2U/OiBib29sZWFuOyAgICAgICAgLy8g5by65Yi25Y6L57ypXG4gIGxldmVsPzogQ29tcGFjdExldmVsOyAgIC8vIOWOi+e8qee6p+WIq1xuICBkcnlSdW4/OiBib29sZWFuOyAgICAgICAvLyDku4XpooTop4hcbn1cblxuLyoqXG4gKiDljovnvKnnu5PmnpxcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBDb21wYWN0UmVzdWx0IHtcbiAgc3VjY2VzczogYm9vbGVhbjtcbiAgY29tcHJlc3NlZDogbnVtYmVyOyAgICAgLy8g5Y6L57yp55qE6K6w5b+G5pWwXG4gIHNhdmVkVG9rZW5zOiBudW1iZXI7ICAgIC8vIOiKguecgeeahCB0b2tlbiDmlbBcbiAgY29tcHJlc3Npb25SYXRlOiBudW1iZXI7IC8vIOWOi+e8qeeOh++8iDAtMe+8iVxuICBkZXRhaWxzPzogQ29tcGFjdERldGFpbFtdO1xufVxuXG4vKipcbiAqIOWOi+e8qeivpuaDhVxuICovXG5leHBvcnQgaW50ZXJmYWNlIENvbXBhY3REZXRhaWwge1xuICBpZDogc3RyaW5nO1xuICBmcm9tOiBzdHJpbmc7XG4gIHRvOiBzdHJpbmc7XG4gIHNhdmVkVG9rZW5zOiBudW1iZXI7XG4gIGxldmVsOiBDb21wYWN0TGV2ZWw7XG59XG5cbi8qKlxuICog6K6w5b+G5Y6L57yp5ZmoXG4gKi9cbmV4cG9ydCBjbGFzcyBNZW1vcnlDb21wYWN0b3Ige1xuICBwcml2YXRlIG1lbW9yeURpcjogc3RyaW5nO1xuXG4gIGNvbnN0cnVjdG9yKG1lbW9yeURpcjogc3RyaW5nID0gJ21lbW9yeScpIHtcbiAgICB0aGlzLm1lbW9yeURpciA9IG1lbW9yeURpcjtcbiAgfVxuXG4gIC8qKlxuICAgKiDmiafooYzljovnvKlcbiAgICovXG4gIGFzeW5jIGNvbXBhY3Qob3B0aW9uczogQ29tcGFjdE9wdGlvbnMgPSB7fSk6IFByb21pc2U8Q29tcGFjdFJlc3VsdD4ge1xuICAgIGNvbnN0IHtcbiAgICAgIGZvcmNlID0gZmFsc2UsXG4gICAgICBsZXZlbCA9ICdMMicsXG4gICAgICBkcnlSdW4gPSBmYWxzZSxcbiAgICB9ID0gb3B0aW9ucztcblxuICAgIGNvbnN0IGRldGFpbHM6IENvbXBhY3REZXRhaWxbXSA9IFtdO1xuICAgIGxldCB0b3RhbENvbXByZXNzZWQgPSAwO1xuICAgIGxldCB0b3RhbFNhdmVkVG9rZW5zID0gMDtcbiAgICBsZXQgdG90YWxPcmlnaW5hbFRva2VucyA9IDA7XG5cbiAgICAvLyAxLiDojrflj5bmiYDmnInorrDlv4bmlofku7ZcbiAgICBjb25zdCBmaWxlcyA9IGdsb2Iuc3luYyhwYXRoLmpvaW4odGhpcy5tZW1vcnlEaXIsICcqLm1kJykpO1xuICAgIFxuICAgIC8vIDIuIOmBjeWOhuaWh+S7tlxuICAgIGZvciAoY29uc3QgZmlsZSBvZiBmaWxlcykge1xuICAgICAgY29uc3QgZmlsZU5hbWUgPSBwYXRoLmJhc2VuYW1lKGZpbGUpO1xuICAgICAgXG4gICAgICAvLyDot7Pov4cgTUVNT1JZLm1k77yI6ZW/5pyf6K6w5b+G5LiN6Ieq5Yqo5Y6L57yp77yJXG4gICAgICBpZiAoZmlsZU5hbWUgPT09ICdNRU1PUlkubWQnKSB7XG4gICAgICAgIGNvbnRpbnVlO1xuICAgICAgfVxuICAgICAgXG4gICAgICAvLyDop6PmnpDml6XmnJ9cbiAgICAgIGNvbnN0IGRhdGVNYXRjaCA9IGZpbGVOYW1lLm1hdGNoKC8oXFxkezR9LVxcZHsyfS1cXGR7Mn0pXFwubWQvKTtcbiAgICAgIGlmICghZGF0ZU1hdGNoKSBjb250aW51ZTtcbiAgICAgIFxuICAgICAgY29uc3QgZmlsZURhdGUgPSBkYXRlTWF0Y2hbMV07XG4gICAgICBjb25zdCBkYXlzT2xkID0gdGhpcy5nZXREYXlzT2xkKGZpbGVEYXRlKTtcbiAgICAgIFxuICAgICAgLy8gMy4g5qC55o2u5aSp5pWw5Yaz5a6a5Y6L57yp57qn5YirXG4gICAgICBsZXQgdGFyZ2V0TGV2ZWw6IENvbXBhY3RMZXZlbDtcbiAgICAgIFxuICAgICAgaWYgKGRheXNPbGQgPD0gNykge1xuICAgICAgICB0YXJnZXRMZXZlbCA9ICdMMSc7IC8vIDcg5aSp5YaF5L+d55WZ5Y6f5aeLXG4gICAgICB9IGVsc2UgaWYgKGRheXNPbGQgPD0gMzApIHtcbiAgICAgICAgdGFyZ2V0TGV2ZWwgPSAnTDInOyAvLyAzMCDlpKnlhoXmkZjopoFcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRhcmdldExldmVsID0gJ0wzJzsgLy8gMzAg5aSp5Lul5LiK5YWz6ZSu5LqL5a6eXG4gICAgICB9XG4gICAgICBcbiAgICAgIC8vIOWmguaenOaMh+WumuS6hue6p+WIq++8jOS9v+eUqOaMh+Wumue6p+WIq1xuICAgICAgaWYgKGxldmVsKSB7XG4gICAgICAgIHRhcmdldExldmVsID0gbGV2ZWw7XG4gICAgICB9XG4gICAgICBcbiAgICAgIC8vIDQuIOaJp+ihjOWOi+e8qVxuICAgICAgY29uc3QgY29udGVudCA9IGZzLnJlYWRGaWxlU3luYyhmaWxlLCAndXRmLTgnKTtcbiAgICAgIGNvbnN0IGNvbXByZXNzZWQgPSBhd2FpdCB0aGlzLmNvbXByZXNzQ29udGVudChjb250ZW50LCB0YXJnZXRMZXZlbCwgZmlsZSk7XG4gICAgICBcbiAgICAgIGlmIChjb21wcmVzc2VkKSB7XG4gICAgICAgIGRldGFpbHMucHVzaCguLi5jb21wcmVzc2VkKTtcbiAgICAgICAgXG4gICAgICAgIGZvciAoY29uc3QgZGV0YWlsIG9mIGNvbXByZXNzZWQpIHtcbiAgICAgICAgICB0b3RhbENvbXByZXNzZWQrKztcbiAgICAgICAgICB0b3RhbFNhdmVkVG9rZW5zICs9IGRldGFpbC5zYXZlZFRva2VucztcbiAgICAgICAgICBjb25zdCBjb21wcmVzc2lvblJhdGUgPSB0YXJnZXRMZXZlbCA9PT0gJ0wxJyA/IDAgOiB0YXJnZXRMZXZlbCA9PT0gJ0wyJyA/IDAuNSA6IDAuODtcbiAgICAgICAgICB0b3RhbE9yaWdpbmFsVG9rZW5zICs9IGRldGFpbC5zYXZlZFRva2VucyAvICgxIC0gY29tcHJlc3Npb25SYXRlKTtcbiAgICAgICAgfVxuICAgICAgICBcbiAgICAgICAgLy8gNS4g5YaZ5YWl5paH5Lu277yI5aaC5p6c5LiN5pivIGRyeVJ1bu+8iVxuICAgICAgICBpZiAoIWRyeVJ1bikge1xuICAgICAgICAgIGNvbnN0IG5ld0NvbnRlbnQgPSB0aGlzLmFwcGx5Q29tcHJlc3Npb24oY29udGVudCwgY29tcHJlc3NlZCk7XG4gICAgICAgICAgZnMud3JpdGVGaWxlU3luYyhmaWxlLCBuZXdDb250ZW50LCAndXRmLTgnKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cblxuICAgIC8vIDYuIOi/lOWbnue7k+aenFxuICAgIHJldHVybiB7XG4gICAgICBzdWNjZXNzOiB0cnVlLFxuICAgICAgY29tcHJlc3NlZDogdG90YWxDb21wcmVzc2VkLFxuICAgICAgc2F2ZWRUb2tlbnM6IHRvdGFsU2F2ZWRUb2tlbnMsXG4gICAgICBjb21wcmVzc2lvblJhdGU6IHRvdGFsT3JpZ2luYWxUb2tlbnMgPiAwID8gdG90YWxTYXZlZFRva2VucyAvIHRvdGFsT3JpZ2luYWxUb2tlbnMgOiAwLFxuICAgICAgZGV0YWlsczogZHJ5UnVuID8gZGV0YWlscyA6IHVuZGVmaW5lZCxcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIOWOi+e8qeWGheWuuVxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBjb21wcmVzc0NvbnRlbnQoXG4gICAgY29udGVudDogc3RyaW5nLFxuICAgIGxldmVsOiBDb21wYWN0TGV2ZWwsXG4gICAgZmlsZVBhdGg6IHN0cmluZ1xuICApOiBQcm9taXNlPENvbXBhY3REZXRhaWxbXSB8IG51bGw+IHtcbiAgICBjb25zdCBkZXRhaWxzOiBDb21wYWN0RGV0YWlsW10gPSBbXTtcbiAgICBcbiAgICAvLyDmj5Dlj5borrDlv4blnZdcbiAgICBjb25zdCBtZW1vcmllcyA9IHRoaXMuZXh0cmFjdE1lbW9yaWVzKGNvbnRlbnQpO1xuICAgIFxuICAgIGZvciAoY29uc3QgbWVtb3J5IG9mIG1lbW9yaWVzKSB7XG4gICAgICBjb25zdCBjb21wcmVzc2VkID0gdGhpcy5jb21wcmVzc01lbW9yeShtZW1vcnkuY29udGVudCwgbGV2ZWwpO1xuICAgICAgXG4gICAgICBpZiAoY29tcHJlc3NlZCAmJiBjb21wcmVzc2VkLnRvICE9PSBtZW1vcnkuY29udGVudCkge1xuICAgICAgICBjb25zdCBzYXZlZFRva2VucyA9IHRoaXMuZXN0aW1hdGVUb2tlbnMobWVtb3J5LmNvbnRlbnQpIC0gdGhpcy5lc3RpbWF0ZVRva2Vucyhjb21wcmVzc2VkLnRvKTtcbiAgICAgICAgXG4gICAgICAgIGRldGFpbHMucHVzaCh7XG4gICAgICAgICAgaWQ6IG1lbW9yeS5pZCxcbiAgICAgICAgICBmcm9tOiBtZW1vcnkuY29udGVudCxcbiAgICAgICAgICB0bzogY29tcHJlc3NlZC50byxcbiAgICAgICAgICBzYXZlZFRva2VucyxcbiAgICAgICAgICBsZXZlbCxcbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfVxuICAgIFxuICAgIHJldHVybiBkZXRhaWxzLmxlbmd0aCA+IDAgPyBkZXRhaWxzIDogbnVsbDtcbiAgfVxuXG4gIC8qKlxuICAgKiDljovnvKnljZXmnaHorrDlv4ZcbiAgICovXG4gIHByaXZhdGUgY29tcHJlc3NNZW1vcnkoXG4gICAgY29udGVudDogc3RyaW5nLFxuICAgIGxldmVsOiBDb21wYWN0TGV2ZWxcbiAgKTogeyBmcm9tOiBzdHJpbmc7IHRvOiBzdHJpbmcgfSB8IG51bGwge1xuICAgIGNvbnN0IG9yaWdpbmFsID0gY29udGVudDtcbiAgICBcbiAgICBzd2l0Y2ggKGxldmVsKSB7XG4gICAgICBjYXNlICdMMSc6XG4gICAgICAgIC8vIEwxOiDkv53nlZnljp/lp4vvvIzkuI3lgZrljovnvKlcbiAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICBcbiAgICAgIGNhc2UgJ0wyJzpcbiAgICAgICAgLy8gTDI6IOaRmOimgeaPkOeCvFxuICAgICAgICBjb25zdCBzdW1tYXJ5ID0gdGhpcy5nZW5lcmF0ZVN1bW1hcnkob3JpZ2luYWwpO1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIGZyb206IG9yaWdpbmFsLFxuICAgICAgICAgIHRvOiBzdW1tYXJ5LFxuICAgICAgICB9O1xuICAgICAgXG4gICAgICBjYXNlICdMMyc6XG4gICAgICAgIC8vIEwzOiDlj6rkv53nlZnlhbPplK7kuovlrp5cbiAgICAgICAgY29uc3QgZmFjdHMgPSB0aGlzLmV4dHJhY3RLZXlGYWN0cyhvcmlnaW5hbCk7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgZnJvbTogb3JpZ2luYWwsXG4gICAgICAgICAgdG86IGZhY3RzLFxuICAgICAgICB9O1xuICAgICAgXG4gICAgICBkZWZhdWx0OlxuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICog55Sf5oiQ5pGY6KaBXG4gICAqL1xuICBwcml2YXRlIGdlbmVyYXRlU3VtbWFyeShjb250ZW50OiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIC8vIOeugOWNleWunueOsO+8muaPkOWPluWJjSAzIOS4qumdnuepuuihjFxuICAgIC8vIFRPRE86IOS9v+eUqCBMTE0g55Sf5oiQ5pGY6KaBXG4gICAgY29uc3QgbGluZXMgPSBjb250ZW50LnNwbGl0KCdcXG4nKS5maWx0ZXIobGluZSA9PiBsaW5lLnRyaW0oKSk7XG4gICAgY29uc3Qgc3VtbWFyeSA9IGxpbmVzLnNsaWNlKDAsIDMpLmpvaW4oJ1xcbicpO1xuICAgIHJldHVybiBzdW1tYXJ5ICsgJ1xcblxcblvmkZjopoEgLSDljp/lp4vlhoXlrrnlt7LljovnvKldJztcbiAgfVxuXG4gIC8qKlxuICAgKiDmj5Dlj5blhbPplK7kuovlrp5cbiAgICovXG4gIHByaXZhdGUgZXh0cmFjdEtleUZhY3RzKGNvbnRlbnQ6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgLy8g566A5Y2V5a6e546w77ya5o+Q5Y+W5YyF5ZCr5YWz6ZSu6K+N55qE6KGMXG4gICAgLy8gVE9ETzog5L2/55SoIExMTSDmj5Dlj5blhbPplK7kuovlrp5cbiAgICBjb25zdCBrZXl3b3JkcyA9IFsn6K6w5L2PJywgJ+mHjeimgScsICflv4XpobsnLCAn5YWz6ZSuJywgJ+WGs+WumicsICfnu5PorronXTtcbiAgICBjb25zdCBsaW5lcyA9IGNvbnRlbnQuc3BsaXQoJ1xcbicpO1xuICAgIFxuICAgIGNvbnN0IGtleUxpbmVzID0gbGluZXMuZmlsdGVyKGxpbmUgPT4gXG4gICAgICBrZXl3b3Jkcy5zb21lKGtleXdvcmQgPT4gbGluZS5pbmNsdWRlcyhrZXl3b3JkKSlcbiAgICApO1xuICAgIFxuICAgIGlmIChrZXlMaW5lcy5sZW5ndGggPT09IDApIHtcbiAgICAgIC8vIOWmguaenOayoeacieWFs+mUruivje+8jOS/neeVmeesrOS4gOihjFxuICAgICAgcmV0dXJuIGxpbmVzWzBdICsgJ1xcblxcblvlhbPplK7kuovlrp4gLSDljp/lp4vlhoXlrrnlt7LljovnvKldJztcbiAgICB9XG4gICAgXG4gICAgcmV0dXJuIGtleUxpbmVzLmpvaW4oJ1xcbicpICsgJ1xcblxcblvlhbPplK7kuovlrp4gLSDljp/lp4vlhoXlrrnlt7LljovnvKldJztcbiAgfVxuXG4gIC8qKlxuICAgKiDlupTnlKjljovnvKlcbiAgICovXG4gIHByaXZhdGUgYXBwbHlDb21wcmVzc2lvbihjb250ZW50OiBzdHJpbmcsIGRldGFpbHM6IENvbXBhY3REZXRhaWxbXSk6IHN0cmluZyB7XG4gICAgbGV0IHJlc3VsdCA9IGNvbnRlbnQ7XG4gICAgXG4gICAgZm9yIChjb25zdCBkZXRhaWwgb2YgZGV0YWlscykge1xuICAgICAgcmVzdWx0ID0gcmVzdWx0LnJlcGxhY2UoZGV0YWlsLmZyb20sIGRldGFpbC50byk7XG4gICAgfVxuICAgIFxuICAgIHJldHVybiByZXN1bHQ7XG4gIH1cblxuICAvKipcbiAgICog5o+Q5Y+W6K6w5b+GXG4gICAqL1xuICBwcml2YXRlIGV4dHJhY3RNZW1vcmllcyhjb250ZW50OiBzdHJpbmcpOiB7IGlkOiBzdHJpbmc7IGNvbnRlbnQ6IHN0cmluZyB9W10ge1xuICAgIGNvbnN0IG1lbW9yaWVzOiB7IGlkOiBzdHJpbmc7IGNvbnRlbnQ6IHN0cmluZyB9W10gPSBbXTtcbiAgICBjb25zdCBsaW5lcyA9IGNvbnRlbnQuc3BsaXQoJ1xcbicpO1xuICAgIFxuICAgIGxldCBjdXJyZW50SWQgPSAnJztcbiAgICBsZXQgY3VycmVudENvbnRlbnQgPSAnJztcbiAgICBcbiAgICBmb3IgKGNvbnN0IGxpbmUgb2YgbGluZXMpIHtcbiAgICAgIGlmIChsaW5lLnN0YXJ0c1dpdGgoJyoqSUQqKjonKSkge1xuICAgICAgICBjdXJyZW50SWQgPSBsaW5lLnJlcGxhY2UoJyoqSUQqKjonLCAnJykudHJpbSgpO1xuICAgICAgfSBlbHNlIGlmIChsaW5lLnN0YXJ0c1dpdGgoJyMjICcpIHx8IGxpbmUuc3RhcnRzV2l0aCgnIyMjICcpKSB7XG4gICAgICAgIGlmIChjdXJyZW50SWQgJiYgY3VycmVudENvbnRlbnQpIHtcbiAgICAgICAgICBtZW1vcmllcy5wdXNoKHsgaWQ6IGN1cnJlbnRJZCwgY29udGVudDogY3VycmVudENvbnRlbnQgfSk7XG4gICAgICAgIH1cbiAgICAgICAgY3VycmVudENvbnRlbnQgPSBsaW5lICsgJ1xcbic7XG4gICAgICB9IGVsc2UgaWYgKGN1cnJlbnRJZCkge1xuICAgICAgICBjdXJyZW50Q29udGVudCArPSBsaW5lICsgJ1xcbic7XG4gICAgICB9XG4gICAgfVxuICAgIFxuICAgIGlmIChjdXJyZW50SWQgJiYgY3VycmVudENvbnRlbnQpIHtcbiAgICAgIG1lbW9yaWVzLnB1c2goeyBpZDogY3VycmVudElkLCBjb250ZW50OiBjdXJyZW50Q29udGVudCB9KTtcbiAgICB9XG4gICAgXG4gICAgcmV0dXJuIG1lbW9yaWVzO1xuICB9XG5cbiAgLyoqXG4gICAqIOS8sOeulyB0b2tlbiDmlbBcbiAgICovXG4gIHByaXZhdGUgZXN0aW1hdGVUb2tlbnModGV4dDogc3RyaW5nKTogbnVtYmVyIHtcbiAgICAvLyDnroDljZXkvLDnrpfvvJrkuK3mloflrZfnrKbmlbAgLyAyICsg6Iux5paH5a2X56ym5pWwXG4gICAgY29uc3QgY2hpbmVzZSA9ICh0ZXh0Lm1hdGNoKC9bXFx1NGUwMC1cXHU5ZmE1XS9nKSB8fCBbXSkubGVuZ3RoO1xuICAgIGNvbnN0IGVuZ2xpc2ggPSAodGV4dC5tYXRjaCgvW2EtekEtWjAtOV0vZykgfHwgW10pLmxlbmd0aDtcbiAgICByZXR1cm4gTWF0aC5mbG9vcihjaGluZXNlIC8gMiArIGVuZ2xpc2ggLyA0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiDorqHnrpfmlofku7blpKnmlbBcbiAgICovXG4gIHByaXZhdGUgZ2V0RGF5c09sZChkYXRlU3RyOiBzdHJpbmcpOiBudW1iZXIge1xuICAgIGNvbnN0IGZpbGVEYXRlID0gbmV3IERhdGUoZGF0ZVN0cik7XG4gICAgY29uc3QgdG9kYXkgPSBuZXcgRGF0ZSgpO1xuICAgIGNvbnN0IGRpZmYgPSB0b2RheS5nZXRUaW1lKCkgLSBmaWxlRGF0ZS5nZXRUaW1lKCk7XG4gICAgcmV0dXJuIE1hdGguZmxvb3IoZGlmZiAvICgxMDAwICogNjAgKiA2MCAqIDI0KSk7XG4gIH1cbn1cblxuLy8g5a+85Ye6XG5leHBvcnQgZGVmYXVsdCBNZW1vcnlDb21wYWN0b3I7XG4iXX0=