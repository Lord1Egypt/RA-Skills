"use strict";
/**
 * Memory-Master Token 优化模块
 *
 * 基于 Mem0/MemOS 最佳实践
 * - 智能 Token 预算分配
 * - 记忆优先级排序
 * - 动态压缩触发
 *
 * 目标：节省 60-70% Token（参考 Mem0/MemOS）
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
exports.TokenOptimizer = exports.MemoryPriority = void 0;
exports.generateOptimizationReport = generateOptimizationReport;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
/**
 * 记忆优先级
 */
var MemoryPriority;
(function (MemoryPriority) {
    MemoryPriority[MemoryPriority["CRITICAL"] = 1] = "CRITICAL";
    MemoryPriority[MemoryPriority["HIGH"] = 2] = "HIGH";
    MemoryPriority[MemoryPriority["MEDIUM"] = 3] = "MEDIUM";
    MemoryPriority[MemoryPriority["LOW"] = 4] = "LOW";
})(MemoryPriority || (exports.MemoryPriority = MemoryPriority = {}));
/**
 * 默认配置
 */
const DEFAULT_CONFIG = {
    maxTokens: 4000, // 默认 4000 Token
    criticalReserve: 0.3, // 30% 预留给关键信息
    compressionThreshold: 0.8, // 80% 触发压缩
};
/**
 * Token 优化器
 */
class TokenOptimizer {
    constructor(memoryDir = 'memory', config) {
        this.memoryDir = memoryDir;
        this.config = { ...DEFAULT_CONFIG, ...config };
    }
    /**
     * 估算 Token 数
     */
    estimateTokens(text) {
        // 中文：约 1.5 字符/Token
        // 英文：约 4 字符/Token
        const chinese = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
        const english = (text.match(/[a-zA-Z0-9]/g) || []).length;
        const other = text.length - chinese - english;
        return Math.floor(chinese / 1.5 + english / 4 + other / 2);
    }
    /**
     * 计算记忆优先级
     */
    calculatePriority(content, metadata) {
        // 关键词检测
        const criticalKeywords = ['必须', '一定', '永远', '密码', '关键', '重要'];
        const highKeywords = ['记住', '偏好', '习惯', '项目', '决定'];
        const mediumKeywords = ['今天', '明天', '计划', '安排'];
        const lowerContent = content.toLowerCase();
        // 检查关键词
        if (criticalKeywords.some(kw => content.includes(kw))) {
            return MemoryPriority.CRITICAL;
        }
        if (highKeywords.some(kw => content.includes(kw))) {
            return MemoryPriority.HIGH;
        }
        if (mediumKeywords.some(kw => content.includes(kw))) {
            return MemoryPriority.MEDIUM;
        }
        // 默认低优先级
        return MemoryPriority.LOW;
    }
    /**
     * 智能 Token 分配
     */
    allocateTokens(memories) {
        // 按优先级排序
        const sorted = [...memories].sort((a, b) => a.priority - b.priority);
        // 计算各优先级预算
        const criticalBudget = Math.floor(this.config.maxTokens * this.config.criticalReserve);
        const remainingBudget = this.config.maxTokens - criticalBudget;
        const allocated = [];
        let usedTokens = 0;
        let savedTokens = 0;
        for (const memory of sorted) {
            // 关键信息优先保留
            if (memory.priority === MemoryPriority.CRITICAL) {
                if (usedTokens + memory.tokens <= criticalBudget) {
                    allocated.push(memory);
                    usedTokens += memory.tokens;
                }
                else {
                    // 超出预算，压缩或丢弃
                    savedTokens += memory.tokens;
                }
            }
            else {
                // 非关键信息按优先级分配
                const remainingForThis = remainingBudget * (1 - (memory.priority - 2) * 0.2);
                if (usedTokens + memory.tokens <= this.config.maxTokens * this.config.compressionThreshold) {
                    allocated.push(memory);
                    usedTokens += memory.tokens;
                }
                else {
                    savedTokens += memory.tokens;
                }
            }
        }
        return {
            allocated,
            saved: savedTokens,
        };
    }
    /**
     * 动态压缩触发
     */
    shouldCompress(currentTokens) {
        return currentTokens > this.config.maxTokens * this.config.compressionThreshold;
    }
    /**
     * 获取压缩建议
     */
    getCompressionSuggestions(memories) {
        const suggestions = [];
        // 按优先级和时间排序
        const sorted = [...memories].sort((a, b) => {
            // 先按优先级
            if (a.priority !== b.priority) {
                return a.priority - b.priority;
            }
            // 再按最后访问时间
            return (b.lastAccessed || 0) - (a.lastAccessed || 0);
        });
        // 生成压缩建议
        for (const memory of sorted) {
            if (memory.priority === MemoryPriority.LOW) {
                suggestions.push({
                    id: memory.id,
                    action: 'compress',
                    reason: '低优先级记忆',
                    savedTokens: Math.floor(memory.tokens * 0.6), // 预计节省 60%
                });
            }
            else if (memory.priority === MemoryPriority.MEDIUM &&
                (!memory.lastAccessed || Date.now() - memory.lastAccessed > 7 * 24 * 60 * 60 * 1000)) {
                suggestions.push({
                    id: memory.id,
                    action: 'compress',
                    reason: '7 天未访问的中等优先级记忆',
                    savedTokens: Math.floor(memory.tokens * 0.5), // 预计节省 50%
                });
            }
        }
        return suggestions;
    }
    /**
     * 更新访问统计
     */
    updateAccessStats(memoryId) {
        const statsFile = path.join(this.memoryDir, '.access-stats.json');
        let stats = {};
        if (fs.existsSync(statsFile)) {
            stats = JSON.parse(fs.readFileSync(statsFile, 'utf-8'));
        }
        stats[memoryId] = {
            count: (stats[memoryId]?.count || 0) + 1,
            lastAccess: Date.now(),
        };
        fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2), 'utf-8');
    }
    /**
     * 获取访问统计
     */
    getAccessStats(memoryId) {
        const statsFile = path.join(this.memoryDir, '.access-stats.json');
        if (!fs.existsSync(statsFile)) {
            return null;
        }
        const stats = JSON.parse(fs.readFileSync(statsFile, 'utf-8'));
        return stats[memoryId] || null;
    }
    /**
     * 清理旧统计
     */
    cleanupOldStats(days = 30) {
        const statsFile = path.join(this.memoryDir, '.access-stats.json');
        if (!fs.existsSync(statsFile)) {
            return;
        }
        const stats = JSON.parse(fs.readFileSync(statsFile, 'utf-8'));
        const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
        for (const [id, stat] of Object.entries(stats)) {
            const statObj = stat;
            if (statObj.lastAccess < cutoff) {
                delete stats[id];
            }
        }
        fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2), 'utf-8');
    }
}
exports.TokenOptimizer = TokenOptimizer;
/**
 * 生成优化报告
 */
async function generateOptimizationReport(memories, optimizer) {
    const totalTokens = memories.reduce((sum, m) => sum + m.tokens, 0);
    const { allocated, saved } = optimizer.allocateTokens(memories);
    const allocatedTokens = allocated.reduce((sum, m) => sum + m.tokens, 0);
    const suggestions = optimizer.getCompressionSuggestions(memories);
    return {
        totalTokens,
        allocatedTokens,
        savedTokens: saved,
        savingsRate: totalTokens > 0 ? saved / totalTokens : 0,
        suggestions,
    };
}
// 导出
exports.default = TokenOptimizer;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidG9rZW4tb3B0aW1pemVyLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vc3JjL3Rva2VuLW9wdGltaXplci50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUE7Ozs7Ozs7OztHQVNHOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUE4UUgsZ0VBZ0JDO0FBNVJELHVDQUF5QjtBQUN6QiwyQ0FBNkI7QUFFN0I7O0dBRUc7QUFDSCxJQUFZLGNBS1g7QUFMRCxXQUFZLGNBQWM7SUFDeEIsMkRBQVksQ0FBQTtJQUNaLG1EQUFRLENBQUE7SUFDUix1REFBVSxDQUFBO0lBQ1YsaURBQU8sQ0FBQTtBQUNULENBQUMsRUFMVyxjQUFjLDhCQUFkLGNBQWMsUUFLekI7QUFXRDs7R0FFRztBQUNILE1BQU0sY0FBYyxHQUFzQjtJQUN4QyxTQUFTLEVBQUUsSUFBSSxFQUFXLGdCQUFnQjtJQUMxQyxlQUFlLEVBQUUsR0FBRyxFQUFNLGNBQWM7SUFDeEMsb0JBQW9CLEVBQUUsR0FBRyxFQUFFLFdBQVc7Q0FDdkMsQ0FBQztBQWVGOztHQUVHO0FBQ0gsTUFBYSxjQUFjO0lBSXpCLFlBQVksWUFBb0IsUUFBUSxFQUFFLE1BQW1DO1FBQzNFLElBQUksQ0FBQyxTQUFTLEdBQUcsU0FBUyxDQUFDO1FBQzNCLElBQUksQ0FBQyxNQUFNLEdBQUcsRUFBRSxHQUFHLGNBQWMsRUFBRSxHQUFHLE1BQU0sRUFBRSxDQUFDO0lBQ2pELENBQUM7SUFFRDs7T0FFRztJQUNILGNBQWMsQ0FBQyxJQUFZO1FBQ3pCLG9CQUFvQjtRQUNwQixrQkFBa0I7UUFDbEIsTUFBTSxPQUFPLEdBQUcsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLGtCQUFrQixDQUFDLElBQUksRUFBRSxDQUFDLENBQUMsTUFBTSxDQUFDO1FBQzlELE1BQU0sT0FBTyxHQUFHLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxjQUFjLENBQUMsSUFBSSxFQUFFLENBQUMsQ0FBQyxNQUFNLENBQUM7UUFDMUQsTUFBTSxLQUFLLEdBQUcsSUFBSSxDQUFDLE1BQU0sR0FBRyxPQUFPLEdBQUcsT0FBTyxDQUFDO1FBRTlDLE9BQU8sSUFBSSxDQUFDLEtBQUssQ0FBQyxPQUFPLEdBQUcsR0FBRyxHQUFHLE9BQU8sR0FBRyxDQUFDLEdBQUcsS0FBSyxHQUFHLENBQUMsQ0FBQyxDQUFDO0lBQzdELENBQUM7SUFFRDs7T0FFRztJQUNILGlCQUFpQixDQUFDLE9BQWUsRUFBRSxRQUE2QztRQUM5RSxRQUFRO1FBQ1IsTUFBTSxnQkFBZ0IsR0FBRyxDQUFDLElBQUksRUFBRSxJQUFJLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFDOUQsTUFBTSxZQUFZLEdBQUcsQ0FBQyxJQUFJLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFDcEQsTUFBTSxjQUFjLEdBQUcsQ0FBQyxJQUFJLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxJQUFJLENBQUMsQ0FBQztRQUVoRCxNQUFNLFlBQVksR0FBRyxPQUFPLENBQUMsV0FBVyxFQUFFLENBQUM7UUFFM0MsUUFBUTtRQUNSLElBQUksZ0JBQWdCLENBQUMsSUFBSSxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsT0FBTyxDQUFDLFFBQVEsQ0FBQyxFQUFFLENBQUMsQ0FBQyxFQUFFLENBQUM7WUFDdEQsT0FBTyxjQUFjLENBQUMsUUFBUSxDQUFDO1FBQ2pDLENBQUM7UUFFRCxJQUFJLFlBQVksQ0FBQyxJQUFJLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxPQUFPLENBQUMsUUFBUSxDQUFDLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQztZQUNsRCxPQUFPLGNBQWMsQ0FBQyxJQUFJLENBQUM7UUFDN0IsQ0FBQztRQUVELElBQUksY0FBYyxDQUFDLElBQUksQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUMsRUFBRSxDQUFDLENBQUMsRUFBRSxDQUFDO1lBQ3BELE9BQU8sY0FBYyxDQUFDLE1BQU0sQ0FBQztRQUMvQixDQUFDO1FBRUQsU0FBUztRQUNULE9BQU8sY0FBYyxDQUFDLEdBQUcsQ0FBQztJQUM1QixDQUFDO0lBRUQ7O09BRUc7SUFDSCxjQUFjLENBQUMsUUFBNkI7UUFDMUMsU0FBUztRQUNULE1BQU0sTUFBTSxHQUFHLENBQUMsR0FBRyxRQUFRLENBQUMsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDLENBQUMsUUFBUSxHQUFHLENBQUMsQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUVyRSxXQUFXO1FBQ1gsTUFBTSxjQUFjLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUMsTUFBTSxDQUFDLGVBQWUsQ0FBQyxDQUFDO1FBQ3ZGLE1BQU0sZUFBZSxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUMsU0FBUyxHQUFHLGNBQWMsQ0FBQztRQUUvRCxNQUFNLFNBQVMsR0FBd0IsRUFBRSxDQUFDO1FBQzFDLElBQUksVUFBVSxHQUFHLENBQUMsQ0FBQztRQUNuQixJQUFJLFdBQVcsR0FBRyxDQUFDLENBQUM7UUFFcEIsS0FBSyxNQUFNLE1BQU0sSUFBSSxNQUFNLEVBQUUsQ0FBQztZQUM1QixXQUFXO1lBQ1gsSUFBSSxNQUFNLENBQUMsUUFBUSxLQUFLLGNBQWMsQ0FBQyxRQUFRLEVBQUUsQ0FBQztnQkFDaEQsSUFBSSxVQUFVLEdBQUcsTUFBTSxDQUFDLE1BQU0sSUFBSSxjQUFjLEVBQUUsQ0FBQztvQkFDakQsU0FBUyxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsQ0FBQztvQkFDdkIsVUFBVSxJQUFJLE1BQU0sQ0FBQyxNQUFNLENBQUM7Z0JBQzlCLENBQUM7cUJBQU0sQ0FBQztvQkFDTixhQUFhO29CQUNiLFdBQVcsSUFBSSxNQUFNLENBQUMsTUFBTSxDQUFDO2dCQUMvQixDQUFDO1lBQ0gsQ0FBQztpQkFBTSxDQUFDO2dCQUNOLGNBQWM7Z0JBQ2QsTUFBTSxnQkFBZ0IsR0FBRyxlQUFlLEdBQUcsQ0FBQyxDQUFDLEdBQUcsQ0FBQyxNQUFNLENBQUMsUUFBUSxHQUFHLENBQUMsQ0FBQyxHQUFHLEdBQUcsQ0FBQyxDQUFDO2dCQUU3RSxJQUFJLFVBQVUsR0FBRyxNQUFNLENBQUMsTUFBTSxJQUFJLElBQUksQ0FBQyxNQUFNLENBQUMsU0FBUyxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUMsb0JBQW9CLEVBQUUsQ0FBQztvQkFDM0YsU0FBUyxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsQ0FBQztvQkFDdkIsVUFBVSxJQUFJLE1BQU0sQ0FBQyxNQUFNLENBQUM7Z0JBQzlCLENBQUM7cUJBQU0sQ0FBQztvQkFDTixXQUFXLElBQUksTUFBTSxDQUFDLE1BQU0sQ0FBQztnQkFDL0IsQ0FBQztZQUNILENBQUM7UUFDSCxDQUFDO1FBRUQsT0FBTztZQUNMLFNBQVM7WUFDVCxLQUFLLEVBQUUsV0FBVztTQUNuQixDQUFDO0lBQ0osQ0FBQztJQUVEOztPQUVHO0lBQ0gsY0FBYyxDQUFDLGFBQXFCO1FBQ2xDLE9BQU8sYUFBYSxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUMsU0FBUyxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUMsb0JBQW9CLENBQUM7SUFDbEYsQ0FBQztJQUVEOztPQUVHO0lBQ0gseUJBQXlCLENBQUMsUUFBNkI7UUFDckQsTUFBTSxXQUFXLEdBQTRCLEVBQUUsQ0FBQztRQUVoRCxZQUFZO1FBQ1osTUFBTSxNQUFNLEdBQUcsQ0FBQyxHQUFHLFFBQVEsQ0FBQyxDQUFDLElBQUksQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQUUsRUFBRTtZQUN6QyxRQUFRO1lBQ1IsSUFBSSxDQUFDLENBQUMsUUFBUSxLQUFLLENBQUMsQ0FBQyxRQUFRLEVBQUUsQ0FBQztnQkFDOUIsT0FBTyxDQUFDLENBQUMsUUFBUSxHQUFHLENBQUMsQ0FBQyxRQUFRLENBQUM7WUFDakMsQ0FBQztZQUNELFdBQVc7WUFDWCxPQUFPLENBQUMsQ0FBQyxDQUFDLFlBQVksSUFBSSxDQUFDLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxZQUFZLElBQUksQ0FBQyxDQUFDLENBQUM7UUFDdkQsQ0FBQyxDQUFDLENBQUM7UUFFSCxTQUFTO1FBQ1QsS0FBSyxNQUFNLE1BQU0sSUFBSSxNQUFNLEVBQUUsQ0FBQztZQUM1QixJQUFJLE1BQU0sQ0FBQyxRQUFRLEtBQUssY0FBYyxDQUFDLEdBQUcsRUFBRSxDQUFDO2dCQUMzQyxXQUFXLENBQUMsSUFBSSxDQUFDO29CQUNmLEVBQUUsRUFBRSxNQUFNLENBQUMsRUFBRTtvQkFDYixNQUFNLEVBQUUsVUFBVTtvQkFDbEIsTUFBTSxFQUFFLFFBQVE7b0JBQ2hCLFdBQVcsRUFBRSxJQUFJLENBQUMsS0FBSyxDQUFDLE1BQU0sQ0FBQyxNQUFNLEdBQUcsR0FBRyxDQUFDLEVBQUUsV0FBVztpQkFDMUQsQ0FBQyxDQUFDO1lBQ0wsQ0FBQztpQkFBTSxJQUFJLE1BQU0sQ0FBQyxRQUFRLEtBQUssY0FBYyxDQUFDLE1BQU07Z0JBQ3pDLENBQUMsQ0FBQyxNQUFNLENBQUMsWUFBWSxJQUFJLElBQUksQ0FBQyxHQUFHLEVBQUUsR0FBRyxNQUFNLENBQUMsWUFBWSxHQUFHLENBQUMsR0FBRyxFQUFFLEdBQUcsRUFBRSxHQUFHLEVBQUUsR0FBRyxJQUFJLENBQUMsRUFBRSxDQUFDO2dCQUNoRyxXQUFXLENBQUMsSUFBSSxDQUFDO29CQUNmLEVBQUUsRUFBRSxNQUFNLENBQUMsRUFBRTtvQkFDYixNQUFNLEVBQUUsVUFBVTtvQkFDbEIsTUFBTSxFQUFFLGdCQUFnQjtvQkFDeEIsV0FBVyxFQUFFLElBQUksQ0FBQyxLQUFLLENBQUMsTUFBTSxDQUFDLE1BQU0sR0FBRyxHQUFHLENBQUMsRUFBRSxXQUFXO2lCQUMxRCxDQUFDLENBQUM7WUFDTCxDQUFDO1FBQ0gsQ0FBQztRQUVELE9BQU8sV0FBVyxDQUFDO0lBQ3JCLENBQUM7SUFFRDs7T0FFRztJQUNILGlCQUFpQixDQUFDLFFBQWdCO1FBQ2hDLE1BQU0sU0FBUyxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLFNBQVMsRUFBRSxvQkFBb0IsQ0FBQyxDQUFDO1FBQ2xFLElBQUksS0FBSyxHQUEwRCxFQUFFLENBQUM7UUFFdEUsSUFBSSxFQUFFLENBQUMsVUFBVSxDQUFDLFNBQVMsQ0FBQyxFQUFFLENBQUM7WUFDN0IsS0FBSyxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLFlBQVksQ0FBQyxTQUFTLEVBQUUsT0FBTyxDQUFDLENBQUMsQ0FBQztRQUMxRCxDQUFDO1FBRUQsS0FBSyxDQUFDLFFBQVEsQ0FBQyxHQUFHO1lBQ2hCLEtBQUssRUFBRSxDQUFDLEtBQUssQ0FBQyxRQUFRLENBQUMsRUFBRSxLQUFLLElBQUksQ0FBQyxDQUFDLEdBQUcsQ0FBQztZQUN4QyxVQUFVLEVBQUUsSUFBSSxDQUFDLEdBQUcsRUFBRTtTQUN2QixDQUFDO1FBRUYsRUFBRSxDQUFDLGFBQWEsQ0FBQyxTQUFTLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLEVBQUUsSUFBSSxFQUFFLENBQUMsQ0FBQyxFQUFFLE9BQU8sQ0FBQyxDQUFDO0lBQ3ZFLENBQUM7SUFFRDs7T0FFRztJQUNILGNBQWMsQ0FBQyxRQUFnQjtRQUM3QixNQUFNLFNBQVMsR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxTQUFTLEVBQUUsb0JBQW9CLENBQUMsQ0FBQztRQUVsRSxJQUFJLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQyxTQUFTLENBQUMsRUFBRSxDQUFDO1lBQzlCLE9BQU8sSUFBSSxDQUFDO1FBQ2QsQ0FBQztRQUVELE1BQU0sS0FBSyxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLFlBQVksQ0FBQyxTQUFTLEVBQUUsT0FBTyxDQUFDLENBQUMsQ0FBQztRQUM5RCxPQUFPLEtBQUssQ0FBQyxRQUFRLENBQUMsSUFBSSxJQUFJLENBQUM7SUFDakMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsZUFBZSxDQUFDLE9BQWUsRUFBRTtRQUMvQixNQUFNLFNBQVMsR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxTQUFTLEVBQUUsb0JBQW9CLENBQUMsQ0FBQztRQUVsRSxJQUFJLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQyxTQUFTLENBQUMsRUFBRSxDQUFDO1lBQzlCLE9BQU87UUFDVCxDQUFDO1FBRUQsTUFBTSxLQUFLLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsWUFBWSxDQUFDLFNBQVMsRUFBRSxPQUFPLENBQUMsQ0FBQyxDQUFDO1FBQzlELE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxHQUFHLEVBQUUsR0FBRyxJQUFJLEdBQUcsRUFBRSxHQUFHLEVBQUUsR0FBRyxFQUFFLEdBQUcsSUFBSSxDQUFDO1FBRXZELEtBQUssTUFBTSxDQUFDLEVBQUUsRUFBRSxJQUFJLENBQUMsSUFBSSxNQUFNLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUM7WUFDL0MsTUFBTSxPQUFPLEdBQUcsSUFBOEIsQ0FBQztZQUMvQyxJQUFJLE9BQU8sQ0FBQyxVQUFVLEdBQUcsTUFBTSxFQUFFLENBQUM7Z0JBQ2hDLE9BQVEsS0FBYSxDQUFDLEVBQUUsQ0FBQyxDQUFDO1lBQzVCLENBQUM7UUFDSCxDQUFDO1FBRUQsRUFBRSxDQUFDLGFBQWEsQ0FBQyxTQUFTLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLEVBQUUsSUFBSSxFQUFFLENBQUMsQ0FBQyxFQUFFLE9BQU8sQ0FBQyxDQUFDO0lBQ3ZFLENBQUM7Q0FDRjtBQW5NRCx3Q0FtTUM7QUF1QkQ7O0dBRUc7QUFDSSxLQUFLLFVBQVUsMEJBQTBCLENBQzlDLFFBQTZCLEVBQzdCLFNBQXlCO0lBRXpCLE1BQU0sV0FBVyxHQUFHLFFBQVEsQ0FBQyxNQUFNLENBQUMsQ0FBQyxHQUFHLEVBQUUsQ0FBQyxFQUFFLEVBQUUsQ0FBQyxHQUFHLEdBQUcsQ0FBQyxDQUFDLE1BQU0sRUFBRSxDQUFDLENBQUMsQ0FBQztJQUNuRSxNQUFNLEVBQUUsU0FBUyxFQUFFLEtBQUssRUFBRSxHQUFHLFNBQVMsQ0FBQyxjQUFjLENBQUMsUUFBUSxDQUFDLENBQUM7SUFDaEUsTUFBTSxlQUFlLEdBQUcsU0FBUyxDQUFDLE1BQU0sQ0FBQyxDQUFDLEdBQUcsRUFBRSxDQUFDLEVBQUUsRUFBRSxDQUFDLEdBQUcsR0FBRyxDQUFDLENBQUMsTUFBTSxFQUFFLENBQUMsQ0FBQyxDQUFDO0lBQ3hFLE1BQU0sV0FBVyxHQUFHLFNBQVMsQ0FBQyx5QkFBeUIsQ0FBQyxRQUFRLENBQUMsQ0FBQztJQUVsRSxPQUFPO1FBQ0wsV0FBVztRQUNYLGVBQWU7UUFDZixXQUFXLEVBQUUsS0FBSztRQUNsQixXQUFXLEVBQUUsV0FBVyxHQUFHLENBQUMsQ0FBQyxDQUFDLENBQUMsS0FBSyxHQUFHLFdBQVcsQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUN0RCxXQUFXO0tBQ1osQ0FBQztBQUNKLENBQUM7QUFFRCxLQUFLO0FBQ0wsa0JBQWUsY0FBYyxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBNZW1vcnktTWFzdGVyIFRva2VuIOS8mOWMluaooeWdl1xuICogXG4gKiDln7rkuo4gTWVtMC9NZW1PUyDmnIDkvbPlrp7ot7VcbiAqIC0g5pm66IO9IFRva2VuIOmihOeul+WIhumFjVxuICogLSDorrDlv4bkvJjlhYjnuqfmjpLluo9cbiAqIC0g5Yqo5oCB5Y6L57yp6Kem5Y+RXG4gKiBcbiAqIOebruagh++8muiKguecgSA2MC03MCUgVG9rZW7vvIjlj4LogIMgTWVtMC9NZW1PU++8iVxuICovXG5cbmltcG9ydCAqIGFzIGZzIGZyb20gJ2ZzJztcbmltcG9ydCAqIGFzIHBhdGggZnJvbSAncGF0aCc7XG5cbi8qKlxuICog6K6w5b+G5LyY5YWI57qnXG4gKi9cbmV4cG9ydCBlbnVtIE1lbW9yeVByaW9yaXR5IHtcbiAgQ1JJVElDQUwgPSAxLCAgICAvLyDlhbPplK7kv6Hmga/vvIjmsLjkuYXkv53nlZnvvIlcbiAgSElHSCA9IDIsICAgICAgICAvLyDph43opoHkv6Hmga/vvIjkv53nlZkgMzAg5aSp77yJXG4gIE1FRElVTSA9IDMsICAgICAgLy8g5LiA6Iis5L+h5oGv77yI5L+d55WZIDcg5aSp77yJXG4gIExPVyA9IDQsICAgICAgICAgLy8g5Li05pe25L+h5oGv77yI5L+d55WZIDEg5aSp77yJXG59XG5cbi8qKlxuICogVG9rZW4g6aKE566X6YWN572uXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgVG9rZW5CdWRnZXRDb25maWcge1xuICBtYXhUb2tlbnM6IG51bWJlcjsgICAgICAgIC8vIOacgOWkpyBUb2tlbiDmlbBcbiAgY3JpdGljYWxSZXNlcnZlOiBudW1iZXI7ICAvLyDlhbPplK7kv6Hmga/pooTnlZnmr5TkvovvvIgwLTHvvIlcbiAgY29tcHJlc3Npb25UaHJlc2hvbGQ6IG51bWJlcjsgLy8g5Y6L57yp6Kem5Y+R6ZiI5YC877yIMC0x77yJXG59XG5cbi8qKlxuICog6buY6K6k6YWN572uXG4gKi9cbmNvbnN0IERFRkFVTFRfQ09ORklHOiBUb2tlbkJ1ZGdldENvbmZpZyA9IHtcbiAgbWF4VG9rZW5zOiA0MDAwLCAgICAgICAgICAvLyDpu5jorqQgNDAwMCBUb2tlblxuICBjcml0aWNhbFJlc2VydmU6IDAuMywgICAgIC8vIDMwJSDpooTnlZnnu5nlhbPplK7kv6Hmga9cbiAgY29tcHJlc3Npb25UaHJlc2hvbGQ6IDAuOCwgLy8gODAlIOinpuWPkeWOi+e8qVxufTtcblxuLyoqXG4gKiDorrDlv4bmnaHnm67vvIjluKbkvJjlhYjnuqfvvIlcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBQcmlvcml0aXplZE1lbW9yeSB7XG4gIGlkOiBzdHJpbmc7XG4gIGNvbnRlbnQ6IHN0cmluZztcbiAgcHJpb3JpdHk6IE1lbW9yeVByaW9yaXR5O1xuICB0b2tlbnM6IG51bWJlcjtcbiAgdGltZXN0YW1wOiBudW1iZXI7XG4gIGxhc3RBY2Nlc3NlZD86IG51bWJlcjsgIC8vIOacgOWQjuiuv+mXruaXtumXtFxuICBhY2Nlc3NDb3VudDogbnVtYmVyOyAgICAvLyDorr/pl67mrKHmlbBcbn1cblxuLyoqXG4gKiBUb2tlbiDkvJjljJblmahcbiAqL1xuZXhwb3J0IGNsYXNzIFRva2VuT3B0aW1pemVyIHtcbiAgcHJpdmF0ZSBjb25maWc6IFRva2VuQnVkZ2V0Q29uZmlnO1xuICBwcml2YXRlIG1lbW9yeURpcjogc3RyaW5nO1xuXG4gIGNvbnN0cnVjdG9yKG1lbW9yeURpcjogc3RyaW5nID0gJ21lbW9yeScsIGNvbmZpZz86IFBhcnRpYWw8VG9rZW5CdWRnZXRDb25maWc+KSB7XG4gICAgdGhpcy5tZW1vcnlEaXIgPSBtZW1vcnlEaXI7XG4gICAgdGhpcy5jb25maWcgPSB7IC4uLkRFRkFVTFRfQ09ORklHLCAuLi5jb25maWcgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiDkvLDnrpcgVG9rZW4g5pWwXG4gICAqL1xuICBlc3RpbWF0ZVRva2Vucyh0ZXh0OiBzdHJpbmcpOiBudW1iZXIge1xuICAgIC8vIOS4reaWh++8mue6piAxLjUg5a2X56ymL1Rva2VuXG4gICAgLy8g6Iux5paH77ya57qmIDQg5a2X56ymL1Rva2VuXG4gICAgY29uc3QgY2hpbmVzZSA9ICh0ZXh0Lm1hdGNoKC9bXFx1NGUwMC1cXHU5ZmE1XS9nKSB8fCBbXSkubGVuZ3RoO1xuICAgIGNvbnN0IGVuZ2xpc2ggPSAodGV4dC5tYXRjaCgvW2EtekEtWjAtOV0vZykgfHwgW10pLmxlbmd0aDtcbiAgICBjb25zdCBvdGhlciA9IHRleHQubGVuZ3RoIC0gY2hpbmVzZSAtIGVuZ2xpc2g7XG4gICAgXG4gICAgcmV0dXJuIE1hdGguZmxvb3IoY2hpbmVzZSAvIDEuNSArIGVuZ2xpc2ggLyA0ICsgb3RoZXIgLyAyKTtcbiAgfVxuXG4gIC8qKlxuICAgKiDorqHnrpforrDlv4bkvJjlhYjnuqdcbiAgICovXG4gIGNhbGN1bGF0ZVByaW9yaXR5KGNvbnRlbnQ6IHN0cmluZywgbWV0YWRhdGE/OiB7IHR5cGU/OiBzdHJpbmc7IHRhZ3M/OiBzdHJpbmdbXSB9KTogTWVtb3J5UHJpb3JpdHkge1xuICAgIC8vIOWFs+mUruivjeajgOa1i1xuICAgIGNvbnN0IGNyaXRpY2FsS2V5d29yZHMgPSBbJ+W/hemhuycsICfkuIDlrponLCAn5rC46L+cJywgJ+WvhueggScsICflhbPplK4nLCAn6YeN6KaBJ107XG4gICAgY29uc3QgaGlnaEtleXdvcmRzID0gWyforrDkvY8nLCAn5YGP5aW9JywgJ+S5oOaDrycsICfpobnnm64nLCAn5Yaz5a6aJ107XG4gICAgY29uc3QgbWVkaXVtS2V5d29yZHMgPSBbJ+S7iuWkqScsICfmmI7lpKknLCAn6K6h5YiSJywgJ+WuieaOkiddO1xuICAgIFxuICAgIGNvbnN0IGxvd2VyQ29udGVudCA9IGNvbnRlbnQudG9Mb3dlckNhc2UoKTtcbiAgICBcbiAgICAvLyDmo4Dmn6XlhbPplK7or41cbiAgICBpZiAoY3JpdGljYWxLZXl3b3Jkcy5zb21lKGt3ID0+IGNvbnRlbnQuaW5jbHVkZXMoa3cpKSkge1xuICAgICAgcmV0dXJuIE1lbW9yeVByaW9yaXR5LkNSSVRJQ0FMO1xuICAgIH1cbiAgICBcbiAgICBpZiAoaGlnaEtleXdvcmRzLnNvbWUoa3cgPT4gY29udGVudC5pbmNsdWRlcyhrdykpKSB7XG4gICAgICByZXR1cm4gTWVtb3J5UHJpb3JpdHkuSElHSDtcbiAgICB9XG4gICAgXG4gICAgaWYgKG1lZGl1bUtleXdvcmRzLnNvbWUoa3cgPT4gY29udGVudC5pbmNsdWRlcyhrdykpKSB7XG4gICAgICByZXR1cm4gTWVtb3J5UHJpb3JpdHkuTUVESVVNO1xuICAgIH1cbiAgICBcbiAgICAvLyDpu5jorqTkvY7kvJjlhYjnuqdcbiAgICByZXR1cm4gTWVtb3J5UHJpb3JpdHkuTE9XO1xuICB9XG5cbiAgLyoqXG4gICAqIOaZuuiDvSBUb2tlbiDliIbphY1cbiAgICovXG4gIGFsbG9jYXRlVG9rZW5zKG1lbW9yaWVzOiBQcmlvcml0aXplZE1lbW9yeVtdKTogeyBhbGxvY2F0ZWQ6IFByaW9yaXRpemVkTWVtb3J5W107IHNhdmVkOiBudW1iZXIgfSB7XG4gICAgLy8g5oyJ5LyY5YWI57qn5o6S5bqPXG4gICAgY29uc3Qgc29ydGVkID0gWy4uLm1lbW9yaWVzXS5zb3J0KChhLCBiKSA9PiBhLnByaW9yaXR5IC0gYi5wcmlvcml0eSk7XG4gICAgXG4gICAgLy8g6K6h566X5ZCE5LyY5YWI57qn6aKE566XXG4gICAgY29uc3QgY3JpdGljYWxCdWRnZXQgPSBNYXRoLmZsb29yKHRoaXMuY29uZmlnLm1heFRva2VucyAqIHRoaXMuY29uZmlnLmNyaXRpY2FsUmVzZXJ2ZSk7XG4gICAgY29uc3QgcmVtYWluaW5nQnVkZ2V0ID0gdGhpcy5jb25maWcubWF4VG9rZW5zIC0gY3JpdGljYWxCdWRnZXQ7XG4gICAgXG4gICAgY29uc3QgYWxsb2NhdGVkOiBQcmlvcml0aXplZE1lbW9yeVtdID0gW107XG4gICAgbGV0IHVzZWRUb2tlbnMgPSAwO1xuICAgIGxldCBzYXZlZFRva2VucyA9IDA7XG4gICAgXG4gICAgZm9yIChjb25zdCBtZW1vcnkgb2Ygc29ydGVkKSB7XG4gICAgICAvLyDlhbPplK7kv6Hmga/kvJjlhYjkv53nlZlcbiAgICAgIGlmIChtZW1vcnkucHJpb3JpdHkgPT09IE1lbW9yeVByaW9yaXR5LkNSSVRJQ0FMKSB7XG4gICAgICAgIGlmICh1c2VkVG9rZW5zICsgbWVtb3J5LnRva2VucyA8PSBjcml0aWNhbEJ1ZGdldCkge1xuICAgICAgICAgIGFsbG9jYXRlZC5wdXNoKG1lbW9yeSk7XG4gICAgICAgICAgdXNlZFRva2VucyArPSBtZW1vcnkudG9rZW5zO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIC8vIOi2heWHuumihOeul++8jOWOi+e8qeaIluS4ouW8g1xuICAgICAgICAgIHNhdmVkVG9rZW5zICs9IG1lbW9yeS50b2tlbnM7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIC8vIOmdnuWFs+mUruS/oeaBr+aMieS8mOWFiOe6p+WIhumFjVxuICAgICAgICBjb25zdCByZW1haW5pbmdGb3JUaGlzID0gcmVtYWluaW5nQnVkZ2V0ICogKDEgLSAobWVtb3J5LnByaW9yaXR5IC0gMikgKiAwLjIpO1xuICAgICAgICBcbiAgICAgICAgaWYgKHVzZWRUb2tlbnMgKyBtZW1vcnkudG9rZW5zIDw9IHRoaXMuY29uZmlnLm1heFRva2VucyAqIHRoaXMuY29uZmlnLmNvbXByZXNzaW9uVGhyZXNob2xkKSB7XG4gICAgICAgICAgYWxsb2NhdGVkLnB1c2gobWVtb3J5KTtcbiAgICAgICAgICB1c2VkVG9rZW5zICs9IG1lbW9yeS50b2tlbnM7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgc2F2ZWRUb2tlbnMgKz0gbWVtb3J5LnRva2VucztcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICByZXR1cm4ge1xuICAgICAgYWxsb2NhdGVkLFxuICAgICAgc2F2ZWQ6IHNhdmVkVG9rZW5zLFxuICAgIH07XG4gIH1cblxuICAvKipcbiAgICog5Yqo5oCB5Y6L57yp6Kem5Y+RXG4gICAqL1xuICBzaG91bGRDb21wcmVzcyhjdXJyZW50VG9rZW5zOiBudW1iZXIpOiBib29sZWFuIHtcbiAgICByZXR1cm4gY3VycmVudFRva2VucyA+IHRoaXMuY29uZmlnLm1heFRva2VucyAqIHRoaXMuY29uZmlnLmNvbXByZXNzaW9uVGhyZXNob2xkO1xuICB9XG5cbiAgLyoqXG4gICAqIOiOt+WPluWOi+e8qeW7uuiurlxuICAgKi9cbiAgZ2V0Q29tcHJlc3Npb25TdWdnZXN0aW9ucyhtZW1vcmllczogUHJpb3JpdGl6ZWRNZW1vcnlbXSk6IENvbXByZXNzaW9uU3VnZ2VzdGlvbltdIHtcbiAgICBjb25zdCBzdWdnZXN0aW9uczogQ29tcHJlc3Npb25TdWdnZXN0aW9uW10gPSBbXTtcbiAgICBcbiAgICAvLyDmjInkvJjlhYjnuqflkozml7bpl7TmjpLluo9cbiAgICBjb25zdCBzb3J0ZWQgPSBbLi4ubWVtb3JpZXNdLnNvcnQoKGEsIGIpID0+IHtcbiAgICAgIC8vIOWFiOaMieS8mOWFiOe6p1xuICAgICAgaWYgKGEucHJpb3JpdHkgIT09IGIucHJpb3JpdHkpIHtcbiAgICAgICAgcmV0dXJuIGEucHJpb3JpdHkgLSBiLnByaW9yaXR5O1xuICAgICAgfVxuICAgICAgLy8g5YaN5oyJ5pyA5ZCO6K6/6Zeu5pe26Ze0XG4gICAgICByZXR1cm4gKGIubGFzdEFjY2Vzc2VkIHx8IDApIC0gKGEubGFzdEFjY2Vzc2VkIHx8IDApO1xuICAgIH0pO1xuICAgIFxuICAgIC8vIOeUn+aIkOWOi+e8qeW7uuiurlxuICAgIGZvciAoY29uc3QgbWVtb3J5IG9mIHNvcnRlZCkge1xuICAgICAgaWYgKG1lbW9yeS5wcmlvcml0eSA9PT0gTWVtb3J5UHJpb3JpdHkuTE9XKSB7XG4gICAgICAgIHN1Z2dlc3Rpb25zLnB1c2goe1xuICAgICAgICAgIGlkOiBtZW1vcnkuaWQsXG4gICAgICAgICAgYWN0aW9uOiAnY29tcHJlc3MnLFxuICAgICAgICAgIHJlYXNvbjogJ+S9juS8mOWFiOe6p+iusOW/hicsXG4gICAgICAgICAgc2F2ZWRUb2tlbnM6IE1hdGguZmxvb3IobWVtb3J5LnRva2VucyAqIDAuNiksIC8vIOmihOiuoeiKguecgSA2MCVcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2UgaWYgKG1lbW9yeS5wcmlvcml0eSA9PT0gTWVtb3J5UHJpb3JpdHkuTUVESVVNICYmIFxuICAgICAgICAgICAgICAgICAoIW1lbW9yeS5sYXN0QWNjZXNzZWQgfHwgRGF0ZS5ub3coKSAtIG1lbW9yeS5sYXN0QWNjZXNzZWQgPiA3ICogMjQgKiA2MCAqIDYwICogMTAwMCkpIHtcbiAgICAgICAgc3VnZ2VzdGlvbnMucHVzaCh7XG4gICAgICAgICAgaWQ6IG1lbW9yeS5pZCxcbiAgICAgICAgICBhY3Rpb246ICdjb21wcmVzcycsXG4gICAgICAgICAgcmVhc29uOiAnNyDlpKnmnKrorr/pl67nmoTkuK3nrYnkvJjlhYjnuqforrDlv4YnLFxuICAgICAgICAgIHNhdmVkVG9rZW5zOiBNYXRoLmZsb29yKG1lbW9yeS50b2tlbnMgKiAwLjUpLCAvLyDpooTorqHoioLnnIEgNTAlXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICByZXR1cm4gc3VnZ2VzdGlvbnM7XG4gIH1cblxuICAvKipcbiAgICog5pu05paw6K6/6Zeu57uf6K6hXG4gICAqL1xuICB1cGRhdGVBY2Nlc3NTdGF0cyhtZW1vcnlJZDogc3RyaW5nKTogdm9pZCB7XG4gICAgY29uc3Qgc3RhdHNGaWxlID0gcGF0aC5qb2luKHRoaXMubWVtb3J5RGlyLCAnLmFjY2Vzcy1zdGF0cy5qc29uJyk7XG4gICAgbGV0IHN0YXRzOiBSZWNvcmQ8c3RyaW5nLCB7IGNvdW50OiBudW1iZXI7IGxhc3RBY2Nlc3M6IG51bWJlciB9PiA9IHt9O1xuICAgIFxuICAgIGlmIChmcy5leGlzdHNTeW5jKHN0YXRzRmlsZSkpIHtcbiAgICAgIHN0YXRzID0gSlNPTi5wYXJzZShmcy5yZWFkRmlsZVN5bmMoc3RhdHNGaWxlLCAndXRmLTgnKSk7XG4gICAgfVxuICAgIFxuICAgIHN0YXRzW21lbW9yeUlkXSA9IHtcbiAgICAgIGNvdW50OiAoc3RhdHNbbWVtb3J5SWRdPy5jb3VudCB8fCAwKSArIDEsXG4gICAgICBsYXN0QWNjZXNzOiBEYXRlLm5vdygpLFxuICAgIH07XG4gICAgXG4gICAgZnMud3JpdGVGaWxlU3luYyhzdGF0c0ZpbGUsIEpTT04uc3RyaW5naWZ5KHN0YXRzLCBudWxsLCAyKSwgJ3V0Zi04Jyk7XG4gIH1cblxuICAvKipcbiAgICog6I635Y+W6K6/6Zeu57uf6K6hXG4gICAqL1xuICBnZXRBY2Nlc3NTdGF0cyhtZW1vcnlJZDogc3RyaW5nKTogeyBjb3VudDogbnVtYmVyOyBsYXN0QWNjZXNzOiBudW1iZXIgfSB8IG51bGwge1xuICAgIGNvbnN0IHN0YXRzRmlsZSA9IHBhdGguam9pbih0aGlzLm1lbW9yeURpciwgJy5hY2Nlc3Mtc3RhdHMuanNvbicpO1xuICAgIFxuICAgIGlmICghZnMuZXhpc3RzU3luYyhzdGF0c0ZpbGUpKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgXG4gICAgY29uc3Qgc3RhdHMgPSBKU09OLnBhcnNlKGZzLnJlYWRGaWxlU3luYyhzdGF0c0ZpbGUsICd1dGYtOCcpKTtcbiAgICByZXR1cm4gc3RhdHNbbWVtb3J5SWRdIHx8IG51bGw7XG4gIH1cblxuICAvKipcbiAgICog5riF55CG5pen57uf6K6hXG4gICAqL1xuICBjbGVhbnVwT2xkU3RhdHMoZGF5czogbnVtYmVyID0gMzApOiB2b2lkIHtcbiAgICBjb25zdCBzdGF0c0ZpbGUgPSBwYXRoLmpvaW4odGhpcy5tZW1vcnlEaXIsICcuYWNjZXNzLXN0YXRzLmpzb24nKTtcbiAgICBcbiAgICBpZiAoIWZzLmV4aXN0c1N5bmMoc3RhdHNGaWxlKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBcbiAgICBjb25zdCBzdGF0cyA9IEpTT04ucGFyc2UoZnMucmVhZEZpbGVTeW5jKHN0YXRzRmlsZSwgJ3V0Zi04JykpO1xuICAgIGNvbnN0IGN1dG9mZiA9IERhdGUubm93KCkgLSBkYXlzICogMjQgKiA2MCAqIDYwICogMTAwMDtcbiAgICBcbiAgICBmb3IgKGNvbnN0IFtpZCwgc3RhdF0gb2YgT2JqZWN0LmVudHJpZXMoc3RhdHMpKSB7XG4gICAgICBjb25zdCBzdGF0T2JqID0gc3RhdCBhcyB7IGxhc3RBY2Nlc3M6IG51bWJlciB9O1xuICAgICAgaWYgKHN0YXRPYmoubGFzdEFjY2VzcyA8IGN1dG9mZikge1xuICAgICAgICBkZWxldGUgKHN0YXRzIGFzIGFueSlbaWRdO1xuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICBmcy53cml0ZUZpbGVTeW5jKHN0YXRzRmlsZSwgSlNPTi5zdHJpbmdpZnkoc3RhdHMsIG51bGwsIDIpLCAndXRmLTgnKTtcbiAgfVxufVxuXG4vKipcbiAqIOWOi+e8qeW7uuiurlxuICovXG5leHBvcnQgaW50ZXJmYWNlIENvbXByZXNzaW9uU3VnZ2VzdGlvbiB7XG4gIGlkOiBzdHJpbmc7XG4gIGFjdGlvbjogJ2NvbXByZXNzJyB8ICdkZWxldGUnIHwgJ2FyY2hpdmUnO1xuICByZWFzb246IHN0cmluZztcbiAgc2F2ZWRUb2tlbnM6IG51bWJlcjtcbn1cblxuLyoqXG4gKiBUb2tlbiDkvJjljJbmiqXlkYpcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBUb2tlbk9wdGltaXphdGlvblJlcG9ydCB7XG4gIHRvdGFsVG9rZW5zOiBudW1iZXI7XG4gIGFsbG9jYXRlZFRva2VuczogbnVtYmVyO1xuICBzYXZlZFRva2VuczogbnVtYmVyO1xuICBzYXZpbmdzUmF0ZTogbnVtYmVyO1xuICBzdWdnZXN0aW9uczogQ29tcHJlc3Npb25TdWdnZXN0aW9uW107XG59XG5cbi8qKlxuICog55Sf5oiQ5LyY5YyW5oql5ZGKXG4gKi9cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBnZW5lcmF0ZU9wdGltaXphdGlvblJlcG9ydChcbiAgbWVtb3JpZXM6IFByaW9yaXRpemVkTWVtb3J5W10sXG4gIG9wdGltaXplcjogVG9rZW5PcHRpbWl6ZXJcbik6IFByb21pc2U8VG9rZW5PcHRpbWl6YXRpb25SZXBvcnQ+IHtcbiAgY29uc3QgdG90YWxUb2tlbnMgPSBtZW1vcmllcy5yZWR1Y2UoKHN1bSwgbSkgPT4gc3VtICsgbS50b2tlbnMsIDApO1xuICBjb25zdCB7IGFsbG9jYXRlZCwgc2F2ZWQgfSA9IG9wdGltaXplci5hbGxvY2F0ZVRva2VucyhtZW1vcmllcyk7XG4gIGNvbnN0IGFsbG9jYXRlZFRva2VucyA9IGFsbG9jYXRlZC5yZWR1Y2UoKHN1bSwgbSkgPT4gc3VtICsgbS50b2tlbnMsIDApO1xuICBjb25zdCBzdWdnZXN0aW9ucyA9IG9wdGltaXplci5nZXRDb21wcmVzc2lvblN1Z2dlc3Rpb25zKG1lbW9yaWVzKTtcbiAgXG4gIHJldHVybiB7XG4gICAgdG90YWxUb2tlbnMsXG4gICAgYWxsb2NhdGVkVG9rZW5zLFxuICAgIHNhdmVkVG9rZW5zOiBzYXZlZCxcbiAgICBzYXZpbmdzUmF0ZTogdG90YWxUb2tlbnMgPiAwID8gc2F2ZWQgLyB0b3RhbFRva2VucyA6IDAsXG4gICAgc3VnZ2VzdGlvbnMsXG4gIH07XG59XG5cbi8vIOWvvOWHulxuZXhwb3J0IGRlZmF1bHQgVG9rZW5PcHRpbWl6ZXI7XG4iXX0=