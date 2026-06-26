"use strict";
/**
 * Memory-Master 技能自进化模块
 *
 * 基于 AutoSkill / SkillRL 论文
 * - 从错误中学习
 * - 技能蒸馏
 * - 经验驱动的终身学习
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
exports.SkillEvolver = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
/**
 * 默认配置
 */
const DEFAULT_CONFIG = {
    minSuccesses: 3, // 3 次成功触发蒸馏
    minFailures: 2, // 2 次失败触发学习
    retentionDays: 30, // 保留 30 天经验
};
/**
 * 技能进化器
 */
class SkillEvolver {
    constructor(memoryDir = 'memory', config) {
        this.config = { ...DEFAULT_CONFIG, ...config };
        this.skillsFile = path.join(memoryDir, 'skills.json');
        this.experiencesFile = path.join(memoryDir, 'experiences.json');
        // 初始化文件
        this.initFiles();
    }
    /**
     * 初始化文件
     */
    initFiles() {
        if (!fs.existsSync(this.skillsFile)) {
            fs.writeFileSync(this.skillsFile, JSON.stringify([], null, 2), 'utf-8');
        }
        if (!fs.existsSync(this.experiencesFile)) {
            fs.writeFileSync(this.experiencesFile, JSON.stringify([], null, 2), 'utf-8');
        }
    }
    /**
     * 记录经验
     */
    async recordExperience(context, action, result, feedback, skillId) {
        const experiences = this.loadExperiences();
        const experience = {
            id: this.generateId(),
            skillId,
            context,
            action,
            result,
            feedback,
            timestamp: Date.now(),
        };
        // 从失败中学习
        if (result === 'failure') {
            experience.lessons = await this.learnFromFailure(experience);
            // 更新关联技能的失败计数
            if (skillId) {
                this.updateSkillStats(skillId, { failure: true });
            }
        }
        else {
            // 更新关联技能的成功计数
            if (skillId) {
                this.updateSkillStats(skillId, { success: true });
            }
        }
        experiences.push(experience);
        this.saveExperiences(experiences);
        return experience;
    }
    /**
     * 从失败中学习
     */
    async learnFromFailure(experience) {
        const lessons = [];
        // 简单实现：提取关键错误信息
        // TODO: 使用 LLM 分析失败原因
        if (experience.feedback) {
            const errorPatterns = [
                { pattern: /超时|timeout/i, lesson: '增加超时时间或重试机制' },
                { pattern: /权限|permission/i, lesson: '检查权限配置' },
                { pattern: /格式|format/i, lesson: '验证输入格式' },
                { pattern: /不存在|not found/i, lesson: '添加存在性检查' },
            ];
            for (const { pattern, lesson } of errorPatterns) {
                if (pattern.test(experience.feedback)) {
                    lessons.push(lesson);
                }
            }
        }
        // 如果没有检测到具体错误，添加通用教训
        if (lessons.length === 0) {
            lessons.push('记录详细错误日志以便后续分析');
        }
        return lessons;
    }
    /**
     * 技能蒸馏（从成功经验中提取）
     */
    async distillSkills() {
        const experiences = this.loadExperiences();
        const skills = this.loadSkills();
        // 按动作分组成功经验
        const successByAction = new Map();
        for (const exp of experiences) {
            if (exp.result === 'success') {
                const actionKey = exp.action;
                if (!successByAction.has(actionKey)) {
                    successByAction.set(actionKey, []);
                }
                successByAction.get(actionKey).push(exp);
            }
        }
        const newSkills = [];
        // 为频繁成功的动作创建技能
        for (const [action, exps] of successByAction.entries()) {
            if (exps.length >= this.config.minSuccesses) {
                // 检查是否已存在相同技能的技能
                const existingSkill = skills.find(s => s.action === action);
                if (!existingSkill) {
                    // 创建新技能
                    const skill = {
                        id: this.generateId(),
                        name: `Skill-${action.substring(0, 20)}`,
                        description: `从 ${exps.length} 次成功经验中蒸馏`,
                        pattern: this.extractPattern(exps),
                        action,
                        successCount: exps.length,
                        failureCount: 0,
                        createdAt: Date.now(),
                        updatedAt: Date.now(),
                    };
                    newSkills.push(skill);
                }
                else {
                    // 更新现有技能
                    existingSkill.successCount += exps.length;
                    existingSkill.updatedAt = Date.now();
                }
            }
        }
        // 保存新技能
        if (newSkills.length > 0) {
            skills.push(...newSkills);
            this.saveSkills(skills);
        }
        return newSkills;
    }
    /**
     * 提取触发模式
     */
    extractPattern(experiences) {
        // 简单实现：提取共同上下文
        // TODO: 使用 LLM 提取通用模式
        const contexts = experiences.map(e => e.context);
        const commonWords = this.findCommonWords(contexts);
        return commonWords.join(' ') || '*';
    }
    /**
     * 查找共同词汇
     */
    findCommonWords(texts) {
        const wordCount = new Map();
        for (const text of texts) {
            const words = text.split(/\s+/);
            const uniqueWords = new Set(words);
            for (const word of uniqueWords) {
                if (word.length > 2) { // 忽略短词
                    wordCount.set(word, (wordCount.get(word) || 0) + 1);
                }
            }
        }
        // 返回出现频率高的词
        const threshold = Math.ceil(texts.length * 0.5);
        return Array.from(wordCount.entries())
            .filter(([_, count]) => count >= threshold)
            .map(([word]) => word);
    }
    /**
     * 更新技能统计
     */
    updateSkillStats(skillId, stats) {
        const skills = this.loadSkills();
        const skill = skills.find(s => s.id === skillId);
        if (skill) {
            if (stats.success) {
                skill.successCount++;
            }
            if (stats.failure) {
                skill.failureCount++;
            }
            skill.updatedAt = Date.now();
            this.saveSkills(skills);
        }
    }
    /**
     * 获取技能建议
     */
    getSkillSuggestions(context) {
        const skills = this.loadSkills();
        // 简单匹配：检查上下文是否包含技能模式
        return skills.filter(skill => {
            if (skill.pattern === '*')
                return true;
            return context.toLowerCase().includes(skill.pattern.toLowerCase());
        }).sort((a, b) => {
            // 按成功率排序
            const aRate = a.successCount / (a.successCount + a.failureCount || 1);
            const bRate = b.successCount / (b.successCount + b.failureCount || 1);
            return bRate - aRate;
        });
    }
    /**
     * 清理旧经验
     */
    cleanupOldExperiences() {
        const experiences = this.loadExperiences();
        const cutoff = Date.now() - this.config.retentionDays * 24 * 60 * 60 * 1000;
        const filtered = experiences.filter(exp => exp.timestamp > cutoff);
        if (filtered.length !== experiences.length) {
            this.saveExperiences(filtered);
        }
    }
    /**
     * 加载技能
     */
    loadSkills() {
        const content = fs.readFileSync(this.skillsFile, 'utf-8');
        return JSON.parse(content);
    }
    /**
     * 保存技能
     */
    saveSkills(skills) {
        fs.writeFileSync(this.skillsFile, JSON.stringify(skills, null, 2), 'utf-8');
    }
    /**
     * 加载经验
     */
    loadExperiences() {
        const content = fs.readFileSync(this.experiencesFile, 'utf-8');
        return JSON.parse(content);
    }
    /**
     * 保存经验
     */
    saveExperiences(experiences) {
        fs.writeFileSync(this.experiencesFile, JSON.stringify(experiences, null, 2), 'utf-8');
    }
    /**
     * 生成 ID
     */
    generateId() {
        return `skill-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
    }
    /**
     * 获取统计信息
     */
    getStats() {
        const skills = this.loadSkills();
        const experiences = this.loadExperiences();
        const successes = experiences.filter(e => e.result === 'success').length;
        const failures = experiences.filter(e => e.result === 'failure').length;
        const total = successes + failures;
        return {
            totalSkills: skills.length,
            totalExperiences: experiences.length,
            successRate: total > 0 ? successes / total : 0,
        };
    }
}
exports.SkillEvolver = SkillEvolver;
// 导出
exports.default = SkillEvolver;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoic2tpbGwtZXZvbHZlci5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NyYy9za2lsbC1ldm9sdmVyLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7QUFBQTs7Ozs7OztHQU9HOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFFSCx1Q0FBeUI7QUFDekIsMkNBQTZCO0FBeUM3Qjs7R0FFRztBQUNILE1BQU0sY0FBYyxHQUF5QjtJQUMzQyxZQUFZLEVBQUUsQ0FBQyxFQUFVLFlBQVk7SUFDckMsV0FBVyxFQUFFLENBQUMsRUFBVyxZQUFZO0lBQ3JDLGFBQWEsRUFBRSxFQUFFLEVBQVEsWUFBWTtDQUN0QyxDQUFDO0FBRUY7O0dBRUc7QUFDSCxNQUFhLFlBQVk7SUFLdkIsWUFBWSxZQUFvQixRQUFRLEVBQUUsTUFBc0M7UUFDOUUsSUFBSSxDQUFDLE1BQU0sR0FBRyxFQUFFLEdBQUcsY0FBYyxFQUFFLEdBQUcsTUFBTSxFQUFFLENBQUM7UUFDL0MsSUFBSSxDQUFDLFVBQVUsR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLFNBQVMsRUFBRSxhQUFhLENBQUMsQ0FBQztRQUN0RCxJQUFJLENBQUMsZUFBZSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsU0FBUyxFQUFFLGtCQUFrQixDQUFDLENBQUM7UUFFaEUsUUFBUTtRQUNSLElBQUksQ0FBQyxTQUFTLEVBQUUsQ0FBQztJQUNuQixDQUFDO0lBRUQ7O09BRUc7SUFDSyxTQUFTO1FBQ2YsSUFBSSxDQUFDLEVBQUUsQ0FBQyxVQUFVLENBQUMsSUFBSSxDQUFDLFVBQVUsQ0FBQyxFQUFFLENBQUM7WUFDcEMsRUFBRSxDQUFDLGFBQWEsQ0FBQyxJQUFJLENBQUMsVUFBVSxFQUFFLElBQUksQ0FBQyxTQUFTLENBQUMsRUFBRSxFQUFFLElBQUksRUFBRSxDQUFDLENBQUMsRUFBRSxPQUFPLENBQUMsQ0FBQztRQUMxRSxDQUFDO1FBRUQsSUFBSSxDQUFDLEVBQUUsQ0FBQyxVQUFVLENBQUMs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eS1NYXN0ZXIg5oqA6IO96Ieq6L+b5YyW5qih5Z2XXG4gKiBcbiAqIOWfuuS6jiBBdXRvU2tpbGwgLyBTa2lsbFJMIOiuuuaWh1xuICogLSDku47plJnor6/kuK3lrabkuaBcbiAqIC0g5oqA6IO96JK46aaPXG4gKiAtIOe7j+mqjOmpseWKqOeahOe7iOi6q+WtpuS5oFxuICovXG5cbmltcG9ydCAqIGFzIGZzIGZyb20gJ2ZzJztcbmltcG9ydCAqIGFzIHBhdGggZnJvbSAncGF0aCc7XG5cbi8qKlxuICog5oqA6IO95p2h55uuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgU2tpbGwge1xuICBpZDogc3RyaW5nO1xuICBuYW1lOiBzdHJpbmc7XG4gIGRlc2NyaXB0aW9uOiBzdHJpbmc7XG4gIHBhdHRlcm46IHN0cmluZzsgICAgICAgICAvLyDop6blj5HmqKHlvI9cbiAgYWN0aW9uOiBzdHJpbmc7ICAgICAgICAgIC8vIOaJp+ihjOWKqOS9nFxuICBzdWNjZXNzQ291bnQ6IG51bWJlcjsgICAgLy8g5oiQ5Yqf5qyh5pWwXG4gIGZhaWx1cmVDb3VudDogbnVtYmVyOyAgICAvLyDlpLHotKXmrKHmlbBcbiAgbGFzdFVzZWQ/OiBudW1iZXI7ICAgICAgIC8vIOacgOWQjuS9v+eUqOaXtumXtFxuICBjcmVhdGVkQXQ6IG51bWJlcjsgICAgICAgLy8g5Yib5bu65pe26Ze0XG4gIHVwZGF0ZWRBdDogbnVtYmVyOyAgICAgICAvLyDmm7TmlrDml7bpl7Rcbn1cblxuLyoqXG4gKiDnu4/pqozorrDlvZVcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBFeHBlcmllbmNlIHtcbiAgaWQ6IHN0cmluZztcbiAgc2tpbGxJZD86IHN0cmluZzsgICAgICAgIC8vIOWFs+iBlOaKgOiDvVxuICBjb250ZXh0OiBzdHJpbmc7ICAgICAgICAgLy8g5LiK5LiL5paHXG4gIGFjdGlvbjogc3RyaW5nOyAgICAgICAgICAvLyDmiafooYznmoTliqjkvZxcbiAgcmVzdWx0OiAnc3VjY2VzcycgfCAnZmFpbHVyZSc7XG4gIGZlZWRiYWNrPzogc3RyaW5nOyAgICAgICAvLyDlj43ppohcbiAgdGltZXN0YW1wOiBudW1iZXI7XG4gIGxlc3NvbnM/OiBzdHJpbmdbXTsgICAgICAvLyDlrabliLDnmoTmlZnorq1cbn1cblxuLyoqXG4gKiDmioDog73ov5vljJbphY3nva5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBTa2lsbEV2b2x1dGlvbkNvbmZpZyB7XG4gIG1pblN1Y2Nlc3NlczogbnVtYmVyOyAgICAvLyDmnIDlsI/miJDlip/mrKHmlbDvvIjnlKjkuo7okrjppo/vvIlcbiAgbWluRmFpbHVyZXM6IG51bWJlcjsgICAgIC8vIOacgOWwj+Wksei0peasoeaVsO+8iOinpuWPkeWtpuS5oO+8iVxuICByZXRlbnRpb25EYXlzOiBudW1iZXI7ICAgLy8g57uP6aqM5L+d55WZ5aSp5pWwXG59XG5cbi8qKlxuICog6buY6K6k6YWN572uXG4gKi9cbmNvbnN0IERFRkFVTFRfQ09ORklHOiBTa2lsbEV2b2x1dGlvbkNvbmZpZyA9IHtcbiAgbWluU3VjY2Vzc2VzOiAzLCAgICAgICAgIC8vIDMg5qyh5oiQ5Yqf6Kem5Y+R6JK46aaPXG4gIG1pbkZhaWx1cmVzOiAyLCAgICAgICAgICAvLyAyIOasoeWksei0peinpuWPkeWtpuS5oFxuICByZXRlbnRpb25EYXlzOiAzMCwgICAgICAgLy8g5L+d55WZIDMwIOWkqee7j+mqjFxufTtcblxuLyoqXG4gKiDmioDog73ov5vljJblmahcbiAqL1xuZXhwb3J0IGNsYXNzIFNraWxsRXZvbHZlciB7XG4gIHByaXZhdGUgY29uZmlnOiBTa2lsbEV2b2x1dGlvbkNvbmZpZztcbiAgcHJpdmF0ZSBza2lsbHNGaWxlOiBzdHJpbmc7XG4gIHByaXZhdGUgZXhwZXJpZW5jZXNGaWxlOiBzdHJpbmc7XG5cbiAgY29uc3RydWN0b3IobWVtb3J5RGlyOiBzdHJpbmcgPSAnbWVtb3J5JywgY29uZmlnPzogUGFydGlhbDxTa2lsbEV2b2x1dGlvbkNvbmZpZz4pIHtcbiAgICB0aGlzLmNvbmZpZyA9IHsgLi4uREVGQVVMVF9DT05GSUcsIC4uLmNvbmZpZyB9O1xuICAgIHRoaXMuc2tpbGxzRmlsZSA9IHBhdGguam9pbihtZW1vcnlEaXIsICdza2lsbHMuanNvbicpO1xuICAgIHRoaXMuZXhwZXJpZW5jZXNGaWxlID0gcGF0aC5qb2luKG1lbW9yeURpciwgJ2V4cGVyaWVuY2VzLmpzb24nKTtcbiAgICBcbiAgICAvLyDliJ3lp4vljJbmlofku7ZcbiAgICB0aGlzLmluaXRGaWxlcygpO1xuICB9XG5cbiAgLyoqXG4gICAqIOWIneWni+WMluaWh+S7tlxuICAgKi9cbiAgcHJpdmF0ZSBpbml0RmlsZXMoKTogdm9pZCB7XG4gICAgaWYgKCFmcy5leGlzdHNTeW5jKHRoaXMuc2tpbGxzRmlsZSkpIHtcbiAgICAgIGZzLndyaXRlRmlsZVN5bmModGhpcy5za2lsbHNGaWxlLCBKU09OLnN0cmluZ2lmeShbXSwgbnVsbCwgMiksICd1dGYtOCcpO1xuICAgIH1cbiAgICBcbiAgICBpZiAoIWZzLmV4aXN0c1N5bmModGhpcy5leHBlcmllbmNlc0ZpbGUpKSB7XG4gICAgICBmcy53cml0ZUZpbGVTeW5jKHRoaXMuZXhwZXJpZW5jZXNGaWxlLCBKU09OLnN0cmluZ2lmeShbXSwgbnVsbCwgMiksICd1dGYtOCcpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiDorrDlvZXnu4/pqoxcbiAgICovXG4gIGFzeW5jIHJlY29yZEV4cGVyaWVuY2UoXG4gICAgY29udGV4dDogc3RyaW5nLFxuICAgIGFjdGlvbjogc3RyaW5nLFxuICAgIHJlc3VsdDogJ3N1Y2Nlc3MnIHwgJ2ZhaWx1cmUnLFxuICAgIGZlZWRiYWNrPzogc3RyaW5nLFxuICAgIHNraWxsSWQ/OiBzdHJpbmdcbiAgKTogUHJvbWlzZTxFeHBlcmllbmNlPiB7XG4gICAgY29uc3QgZXhwZXJpZW5jZXMgPSB0aGlzLmxvYWRFeHBlcmllbmNlcygpO1xuICAgIFxuICAgIGNvbnN0IGV4cGVyaWVuY2U6IEV4cGVyaWVuY2UgPSB7XG4gICAgICBpZDogdGhpcy5nZW5lcmF0ZUlkKCksXG4gICAgICBza2lsbElkLFxuICAgICAgY29udGV4dCxcbiAgICAgIGFjdGlvbixcbiAgICAgIHJlc3VsdCxcbiAgICAgIGZlZWRiYWNrLFxuICAgICAgdGltZXN0YW1wOiBEYXRlLm5vdygpLFxuICAgIH07XG4gICAgXG4gICAgLy8g5LuO5aSx6LSl5Lit5a2m5LmgXG4gICAgaWYgKHJlc3VsdCA9PT0gJ2ZhaWx1cmUnKSB7XG4gICAgICBleHBlcmllbmNlLmxlc3NvbnMgPSBhd2FpdCB0aGlzLmxlYXJuRnJvbUZhaWx1cmUoZXhwZXJpZW5jZSk7XG4gICAgICBcbiAgICAgIC8vIOabtOaWsOWFs+iBlOaKgOiDveeahOWksei0peiuoeaVsFxuICAgICAgaWYgKHNraWxsSWQpIHtcbiAgICAgICAgdGhpcy51cGRhdGVTa2lsbFN0YXRzKHNraWxsSWQsIHsgZmFpbHVyZTogdHJ1ZSB9KTtcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgLy8g5pu05paw5YWz6IGU5oqA6IO955qE5oiQ5Yqf6K6h5pWwXG4gICAgICBpZiAoc2tpbGxJZCkge1xuICAgICAgICB0aGlzLnVwZGF0ZVNraWxsU3RhdHMoc2tpbGxJZCwgeyBzdWNjZXNzOiB0cnVlIH0pO1xuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICBleHBlcmllbmNlcy5wdXNoKGV4cGVyaWVuY2UpO1xuICAgIHRoaXMuc2F2ZUV4cGVyaWVuY2VzKGV4cGVyaWVuY2VzKTtcbiAgICBcbiAgICByZXR1cm4gZXhwZXJpZW5jZTtcbiAgfVxuXG4gIC8qKlxuICAgKiDku47lpLHotKXkuK3lrabkuaBcbiAgICovXG4gIHByaXZhdGUgYXN5bmMgbGVhcm5Gcm9tRmFpbHVyZShleHBlcmllbmNlOiBFeHBlcmllbmNlKTogUHJvbWlzZTxzdHJpbmdbXT4ge1xuICAgIGNvbnN0IGxlc3NvbnM6IHN0cmluZ1tdID0gW107XG4gICAgXG4gICAgLy8g566A5Y2V5a6e546w77ya5o+Q5Y+W5YWz6ZSu6ZSZ6K+v5L+h5oGvXG4gICAgLy8gVE9ETzog5L2/55SoIExMTSDliIbmnpDlpLHotKXljp/lm6BcbiAgICBpZiAoZXhwZXJpZW5jZS5mZWVkYmFjaykge1xuICAgICAgY29uc3QgZXJyb3JQYXR0ZXJucyA9IFtcbiAgICAgICAgeyBwYXR0ZXJuOiAv6LaF5pe2fHRpbWVvdXQvaSwgbGVzc29uOiAn5aKe5Yqg6LaF5pe25pe26Ze05oiW6YeN6K+V5py65Yi2JyB9LFxuICAgICAgICB7IHBhdHRlcm46IC/mnYPpmZB8cGVybWlzc2lvbi9pLCBsZXNzb246ICfmo4Dmn6XmnYPpmZDphY3nva4nIH0sXG4gICAgICAgIHsgcGF0dGVybjogL+agvOW8j3xmb3JtYXQvaSwgbGVzc29uOiAn6aqM6K+B6L6T5YWl5qC85byPJyB9LFxuICAgICAgICB7IHBhdHRlcm46IC/kuI3lrZjlnKh8bm90IGZvdW5kL2ksIGxlc3NvbjogJ+a3u+WKoOWtmOWcqOaAp+ajgOafpScgfSxcbiAgICAgIF07XG4gICAgICBcbiAgICAgIGZvciAoY29uc3QgeyBwYXR0ZXJuLCBsZXNzb24gfSBvZiBlcnJvclBhdHRlcm5zKSB7XG4gICAgICAgIGlmIChwYXR0ZXJuLnRlc3QoZXhwZXJpZW5jZS5mZWVkYmFjaykpIHtcbiAgICAgICAgICBsZXNzb25zLnB1c2gobGVzc29uKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICAvLyDlpoLmnpzmsqHmnInmo4DmtYvliLDlhbfkvZPplJnor6/vvIzmt7vliqDpgJrnlKjmlZnorq1cbiAgICBpZiAobGVzc29ucy5sZW5ndGggPT09IDApIHtcbiAgICAgIGxlc3NvbnMucHVzaCgn6K6w5b2V6K+m57uG6ZSZ6K+v5pel5b+X5Lul5L6/5ZCO57ut5YiG5p6QJyk7XG4gICAgfVxuICAgIFxuICAgIHJldHVybiBsZXNzb25zO1xuICB9XG5cbiAgLyoqXG4gICAqIOaKgOiDveiSuOmmj++8iOS7juaIkOWKn+e7j+mqjOS4reaPkOWPlu+8iVxuICAgKi9cbiAgYXN5bmMgZGlzdGlsbFNraWxscygpOiBQcm9taXNlPFNraWxsW10+IHtcbiAgICBjb25zdCBleHBlcmllbmNlcyA9IHRoaXMubG9hZEV4cGVyaWVuY2VzKCk7XG4gICAgY29uc3Qgc2tpbGxzID0gdGhpcy5sb2FkU2tpbGxzKCk7XG4gICAgXG4gICAgLy8g5oyJ5Yqo5L2c5YiG57uE5oiQ5Yqf57uP6aqMXG4gICAgY29uc3Qgc3VjY2Vzc0J5QWN0aW9uID0gbmV3IE1hcDxzdHJpbmcsIEV4cGVyaWVuY2VbXT4oKTtcbiAgICBcbiAgICBmb3IgKGNvbnN0IGV4cCBvZiBleHBlcmllbmNlcykge1xuICAgICAgaWYgKGV4cC5yZXN1bHQgPT09ICdzdWNjZXNzJykge1xuICAgICAgICBjb25zdCBhY3Rpb25LZXkgPSBleHAuYWN0aW9uO1xuICAgICAgICBpZiAoIXN1Y2Nlc3NCeUFjdGlvbi5oYXMoYWN0aW9uS2V5KSkge1xuICAgICAgICAgIHN1Y2Nlc3NCeUFjdGlvbi5zZXQoYWN0aW9uS2V5LCBbXSk7XG4gICAgICAgIH1cbiAgICAgICAgc3VjY2Vzc0J5QWN0aW9uLmdldChhY3Rpb25LZXkpIS5wdXNoKGV4cCk7XG4gICAgICB9XG4gICAgfVxuICAgIFxuICAgIGNvbnN0IG5ld1NraWxsczogU2tpbGxbXSA9IFtdO1xuICAgIFxuICAgIC8vIOS4uumikee5geaIkOWKn+eahOWKqOS9nOWIm+W7uuaKgOiDvVxuICAgIGZvciAoY29uc3QgW2FjdGlvbiwgZXhwc10gb2Ygc3VjY2Vzc0J5QWN0aW9uLmVudHJpZXMoKSkge1xuICAgICAgaWYgKGV4cHMubGVuZ3RoID49IHRoaXMuY29uZmlnLm1pblN1Y2Nlc3Nlcykge1xuICAgICAgICAvLyDmo4Dmn6XmmK/lkKblt7LlrZjlnKjnm7jlkIzmioDog73nmoTmioDog71cbiAgICAgICAgY29uc3QgZXhpc3RpbmdTa2lsbCA9IHNraWxscy5maW5kKHMgPT4gcy5hY3Rpb24gPT09IGFjdGlvbik7XG4gICAgICAgIFxuICAgICAgICBpZiAoIWV4aXN0aW5nU2tpbGwpIHtcbiAgICAgICAgICAvLyDliJvlu7rmlrDmioDog71cbiAgICAgICAgICBjb25zdCBza2lsbDogU2tpbGwgPSB7XG4gICAgICAgICAgICBpZDogdGhpcy5nZW5lcmF0ZUlkKCksXG4gICAgICAgICAgICBuYW1lOiBgU2tpbGwtJHthY3Rpb24uc3Vic3RyaW5nKDAsIDIwKX1gLFxuICAgICAgICAgICAgZGVzY3JpcHRpb246IGDku44gJHtleHBzLmxlbmd0aH0g5qyh5oiQ5Yqf57uP6aqM5Lit6JK46aaPYCxcbiAgICAgICAgICAgIHBhdHRlcm46IHRoaXMuZXh0cmFjdFBhdHRlcm4oZXhwcyksXG4gICAgICAgICAgICBhY3Rpb24sXG4gICAgICAgICAgICBzdWNjZXNzQ291bnQ6IGV4cHMubGVuZ3RoLFxuICAgICAgICAgICAgZmFpbHVyZUNvdW50OiAwLFxuICAgICAgICAgICAgY3JlYXRlZEF0OiBEYXRlLm5vdygpLFxuICAgICAgICAgICAgdXBkYXRlZEF0OiBEYXRlLm5vdygpLFxuICAgICAgICAgIH07XG4gICAgICAgICAgXG4gICAgICAgICAgbmV3U2tpbGxzLnB1c2goc2tpbGwpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIC8vIOabtOaWsOeOsOacieaKgOiDvVxuICAgICAgICAgIGV4aXN0aW5nU2tpbGwuc3VjY2Vzc0NvdW50ICs9IGV4cHMubGVuZ3RoO1xuICAgICAgICAgIGV4aXN0aW5nU2tpbGwudXBkYXRlZEF0ID0gRGF0ZS5ub3coKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICAvLyDkv53lrZjmlrDmioDog71cbiAgICBpZiAobmV3U2tpbGxzLmxlbmd0aCA+IDApIHtcbiAgICAgIHNraWxscy5wdXNoKC4uLm5ld1NraWxscyk7XG4gICAgICB0aGlzLnNhdmVTa2lsbHMoc2tpbGxzKTtcbiAgICB9XG4gICAgXG4gICAgcmV0dXJuIG5ld1NraWxscztcbiAgfVxuXG4gIC8qKlxuICAgKiDmj5Dlj5bop6blj5HmqKHlvI9cbiAgICovXG4gIHByaXZhdGUgZXh0cmFjdFBhdHRlcm4oZXhwZXJpZW5jZXM6IEV4cGVyaWVuY2VbXSk6IHN0cmluZyB7XG4gICAgLy8g566A5Y2V5a6e546w77ya5o+Q5Y+W5YWx5ZCM5LiK5LiL5paHXG4gICAgLy8gVE9ETzog5L2/55SoIExMTSDmj5Dlj5bpgJrnlKjmqKHlvI9cbiAgICBjb25zdCBjb250ZXh0cyA9IGV4cGVyaWVuY2VzLm1hcChlID0+IGUuY29udGV4dCk7XG4gICAgY29uc3QgY29tbW9uV29yZHMgPSB0aGlzLmZpbmRDb21tb25Xb3Jkcyhjb250ZXh0cyk7XG4gICAgcmV0dXJuIGNvbW1vbldvcmRzLmpvaW4oJyAnKSB8fCAnKic7XG4gIH1cblxuICAvKipcbiAgICog5p+l5om+5YWx5ZCM6K+N5rGHXG4gICAqL1xuICBwcml2YXRlIGZpbmRDb21tb25Xb3Jkcyh0ZXh0czogc3RyaW5nW10pOiBzdHJpbmdbXSB7XG4gICAgY29uc3Qgd29yZENvdW50ID0gbmV3IE1hcDxzdHJpbmcsIG51bWJlcj4oKTtcbiAgICBcbiAgICBmb3IgKGNvbnN0IHRleHQgb2YgdGV4dHMpIHtcbiAgICAgIGNvbnN0IHdvcmRzID0gdGV4dC5zcGxpdCgvXFxzKy8pO1xuICAgICAgY29uc3QgdW5pcXVlV29yZHMgPSBuZXcgU2V0KHdvcmRzKTtcbiAgICAgIFxuICAgICAgZm9yIChjb25zdCB3b3JkIG9mIHVuaXF1ZVdvcmRzKSB7XG4gICAgICAgIGlmICh3b3JkLmxlbmd0aCA+IDIpIHsgLy8g5b+955Wl55+t6K+NXG4gICAgICAgICAgd29yZENvdW50LnNldCh3b3JkLCAod29yZENvdW50LmdldCh3b3JkKSB8fCAwKSArIDEpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICAgIFxuICAgIC8vIOi/lOWbnuWHuueOsOmikeeOh+mrmOeahOivjVxuICAgIGNvbnN0IHRocmVzaG9sZCA9IE1hdGguY2VpbCh0ZXh0cy5sZW5ndGggKiAwLjUpO1xuICAgIHJldHVybiBBcnJheS5mcm9tKHdvcmRDb3VudC5lbnRyaWVzKCkpXG4gICAgICAuZmlsdGVyKChbXywgY291bnRdKSA9PiBjb3VudCA+PSB0aHJlc2hvbGQpXG4gICAgICAubWFwKChbd29yZF0pID0+IHdvcmQpO1xuICB9XG5cbiAgLyoqXG4gICAqIOabtOaWsOaKgOiDvee7n+iuoVxuICAgKi9cbiAgcHJpdmF0ZSB1cGRhdGVTa2lsbFN0YXRzKFxuICAgIHNraWxsSWQ6IHN0cmluZyxcbiAgICBzdGF0czogeyBzdWNjZXNzPzogYm9vbGVhbjsgZmFpbHVyZT86IGJvb2xlYW4gfVxuICApOiB2b2lkIHtcbiAgICBjb25zdCBza2lsbHMgPSB0aGlzLmxvYWRTa2lsbHMoKTtcbiAgICBjb25zdCBza2lsbCA9IHNraWxscy5maW5kKHMgPT4gcy5pZCA9PT0gc2tpbGxJZCk7XG4gICAgXG4gICAgaWYgKHNraWxsKSB7XG4gICAgICBpZiAoc3RhdHMuc3VjY2Vzcykge1xuICAgICAgICBza2lsbC5zdWNjZXNzQ291bnQrKztcbiAgICAgIH1cbiAgICAgIGlmIChzdGF0cy5mYWlsdXJlKSB7XG4gICAgICAgIHNraWxsLmZhaWx1cmVDb3VudCsrO1xuICAgICAgfVxuICAgICAgc2tpbGwudXBkYXRlZEF0ID0gRGF0ZS5ub3coKTtcbiAgICAgIFxuICAgICAgdGhpcy5zYXZlU2tpbGxzKHNraWxscyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIOiOt+WPluaKgOiDveW7uuiurlxuICAgKi9cbiAgZ2V0U2tpbGxTdWdnZXN0aW9ucyhjb250ZXh0OiBzdHJpbmcpOiBTa2lsbFtdIHtcbiAgICBjb25zdCBza2lsbHMgPSB0aGlzLmxvYWRTa2lsbHMoKTtcbiAgICBcbiAgICAvLyDnroDljZXljLnphY3vvJrmo4Dmn6XkuIrkuIvmlofmmK/lkKbljIXlkKvmioDog73mqKHlvI9cbiAgICByZXR1cm4gc2tpbGxzLmZpbHRlcihza2lsbCA9PiB7XG4gICAgICBpZiAoc2tpbGwucGF0dGVybiA9PT0gJyonKSByZXR1cm4gdHJ1ZTtcbiAgICAgIHJldHVybiBjb250ZXh0LnRvTG93ZXJDYXNlKCkuaW5jbHVkZXMoc2tpbGwucGF0dGVybi50b0xvd2VyQ2FzZSgpKTtcbiAgICB9KS5zb3J0KChhLCBiKSA9PiB7XG4gICAgICAvLyDmjInmiJDlip/njofmjpLluo9cbiAgICAgIGNvbnN0IGFSYXRlID0gYS5zdWNjZXNzQ291bnQgLyAoYS5zdWNjZXNzQ291bnQgKyBhLmZhaWx1cmVDb3VudCB8fCAxKTtcbiAgICAgIGNvbnN0IGJSYXRlID0gYi5zdWNjZXNzQ291bnQgLyAoYi5zdWNjZXNzQ291bnQgKyBiLmZhaWx1cmVDb3VudCB8fCAxKTtcbiAgICAgIHJldHVybiBiUmF0ZSAtIGFSYXRlO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIOa4heeQhuaXp+e7j+mqjFxuICAgKi9cbiAgY2xlYW51cE9sZEV4cGVyaWVuY2VzKCk6IHZvaWQge1xuICAgIGNvbnN0IGV4cGVyaWVuY2VzID0gdGhpcy5sb2FkRXhwZXJpZW5jZXMoKTtcbiAgICBjb25zdCBjdXRvZmYgPSBEYXRlLm5vdygpIC0gdGhpcy5jb25maWcucmV0ZW50aW9uRGF5cyAqIDI0ICogNjAgKiA2MCAqIDEwMDA7XG4gICAgXG4gICAgY29uc3QgZmlsdGVyZWQgPSBleHBlcmllbmNlcy5maWx0ZXIoZXhwID0+IGV4cC50aW1lc3RhbXAgPiBjdXRvZmYpO1xuICAgIFxuICAgIGlmIChmaWx0ZXJlZC5sZW5ndGggIT09IGV4cGVyaWVuY2VzLmxlbmd0aCkge1xuICAgICAgdGhpcy5zYXZlRXhwZXJpZW5jZXMoZmlsdGVyZWQpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiDliqDovb3mioDog71cbiAgICovXG4gIHByaXZhdGUgbG9hZFNraWxscygpOiBTa2lsbFtdIHtcbiAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKHRoaXMuc2tpbGxzRmlsZSwgJ3V0Zi04Jyk7XG4gICAgcmV0dXJuIEpTT04ucGFyc2UoY29udGVudCk7XG4gIH1cblxuICAvKipcbiAgICog5L+d5a2Y5oqA6IO9XG4gICAqL1xuICBwcml2YXRlIHNhdmVTa2lsbHMoc2tpbGxzOiBTa2lsbFtdKTogdm9pZCB7XG4gICAgZnMud3JpdGVGaWxlU3luYyh0aGlzLnNraWxsc0ZpbGUsIEpTT04uc3RyaW5naWZ5KHNraWxscywgbnVsbCwgMiksICd1dGYtOCcpO1xuICB9XG5cbiAgLyoqXG4gICAqIOWKoOi9vee7j+mqjFxuICAgKi9cbiAgcHJpdmF0ZSBsb2FkRXhwZXJpZW5jZXMoKTogRXhwZXJpZW5jZVtdIHtcbiAgICBjb25zdCBjb250ZW50ID0gZnMucmVhZEZpbGVTeW5jKHRoaXMuZXhwZXJpZW5jZXNGaWxlLCAndXRmLTgnKTtcbiAgICByZXR1cm4gSlNPTi5wYXJzZShjb250ZW50KTtcbiAgfVxuXG4gIC8qKlxuICAgKiDkv53lrZjnu4/pqoxcbiAgICovXG4gIHByaXZhdGUgc2F2ZUV4cGVyaWVuY2VzKGV4cGVyaWVuY2VzOiBFeHBlcmllbmNlW10pOiB2b2lkIHtcbiAgICBmcy53cml0ZUZpbGVTeW5jKHRoaXMuZXhwZXJpZW5jZXNGaWxlLCBKU09OLnN0cmluZ2lmeShleHBlcmllbmNlcywgbnVsbCwgMiksICd1dGYtOCcpO1xuICB9XG5cbiAgLyoqXG4gICAqIOeUn+aIkCBJRFxuICAgKi9cbiAgcHJpdmF0ZSBnZW5lcmF0ZUlkKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIGBza2lsbC0ke0RhdGUubm93KCl9LSR7TWF0aC5yYW5kb20oKS50b1N0cmluZygzNikuc3Vic3RyaW5nKDIsIDgpfWA7XG4gIH1cblxuICAvKipcbiAgICog6I635Y+W57uf6K6h5L+h5oGvXG4gICAqL1xuICBnZXRTdGF0cygpOiB7XG4gICAgdG90YWxTa2lsbHM6IG51bWJlcjtcbiAgICB0b3RhbEV4cGVyaWVuY2VzOiBudW1iZXI7XG4gICAgc3VjY2Vzc1JhdGU6IG51bWJlcjtcbiAgfSB7XG4gICAgY29uc3Qgc2tpbGxzID0gdGhpcy5sb2FkU2tpbGxzKCk7XG4gICAgY29uc3QgZXhwZXJpZW5jZXMgPSB0aGlzLmxvYWRFeHBlcmllbmNlcygpO1xuICAgIFxuICAgIGNvbnN0IHN1Y2Nlc3NlcyA9IGV4cGVyaWVuY2VzLmZpbHRlcihlID0+IGUucmVzdWx0ID09PSAnc3VjY2VzcycpLmxlbmd0aDtcbiAgICBjb25zdCBmYWlsdXJlcyA9IGV4cGVyaWVuY2VzLmZpbHRlcihlID0+IGUucmVzdWx0ID09PSAnZmFpbHVyZScpLmxlbmd0aDtcbiAgICBjb25zdCB0b3RhbCA9IHN1Y2Nlc3NlcyArIGZhaWx1cmVzO1xuICAgIFxuICAgIHJldHVybiB7XG4gICAgICB0b3RhbFNraWxsczogc2tpbGxzLmxlbmd0aCxcbiAgICAgIHRvdGFsRXhwZXJpZW5jZXM6IGV4cGVyaWVuY2VzLmxlbmd0aCxcbiAgICAgIHN1Y2Nlc3NSYXRlOiB0b3RhbCA+IDAgPyBzdWNjZXNzZXMgLyB0b3RhbCA6IDAsXG4gICAgfTtcbiAgfVxufVxuXG4vLyDlr7zlh7pcbmV4cG9ydCBkZWZhdWx0IFNraWxsRXZvbHZlcjtcbiJdfQ==