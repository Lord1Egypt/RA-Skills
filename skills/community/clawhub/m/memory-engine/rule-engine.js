"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RuleEngine = void 0;
class RuleEngine {
    rules = [];
    constructor() {
        this.initRules();
    }
    initRules() {
        // 偏好类规则
        this.rules.push({
            pattern: /我(?:喜欢|爱|讨厌|偏好)/i,
            tags: ['preference', 'user'],
            knowledgeType: 'preference',
            importance: 0.8
        });
        // 食物类规则
        this.rules.push({
            pattern: /(?:鱼|虾|肉|菜|饭|面|汤|水果|甜点|披萨|汉堡|川菜|粤菜)/i,
            tags: ['food', 'preference'],
            knowledgeType: 'preference',
            importance: 0.8
        });
        // 技能类规则
        this.rules.push({
            pattern: /我(?:擅长|精通|掌握|会|懂)/i,
            tags: ['skill', 'user'],
            knowledgeType: 'skill',
            importance: 0.9
        });
        // 编程类规则
        this.rules.push({
            pattern: /(?:python|java|javascript|react|vue|node|go|rust|代码|编程|开发)/i,
            tags: ['programming', 'skill'],
            knowledgeType: 'skill',
            importance: 0.9
        });
        // 经验类规则
        this.rules.push({
            pattern: /我(?:之前|那次|曾经|以前|经历过|遇到过)/i,
            tags: ['experience', 'user'],
            knowledgeType: 'experience',
            importance: 0.7
        });
        // 教训类规则
        this.rules.push({
            pattern: /(?:不要|避免|记住|注意|必须|不能)/i,
            tags: ['lesson', 'warning'],
            knowledgeType: 'lesson',
            importance: 0.85
        });
        // 年龄类规则
        this.rules.push({
            pattern: /我今年?\d+岁|我\d+岁/i,
            tags: ['age', 'fact'],
            knowledgeType: 'fact',
            importance: 0.6
        });
        // 身份类规则
        this.rules.push({
            pattern: /我是|我在|工作|职业|职位/i,
            tags: ['identity', 'fact'],
            knowledgeType: 'fact',
            importance: 0.6
        });
        // 位置类规则
        this.rules.push({
            pattern: /(?:住在|来自|在|居住|家乡)/i,
            tags: ['location', 'fact'],
            knowledgeType: 'fact',
            importance: 0.6
        });
    }
    // 从文本提取标签
    extractTags(text) {
        const tags = new Set();
        for (const rule of this.rules) {
            if (rule.pattern.test(text)) {
                rule.tags.forEach(tag => tags.add(tag));
            }
        }
        return Array.from(tags);
    }
    // 从文本提取知识
    extractKnowledge(content) {
        const tags = this.extractTags(content);
        if (tags.length === 0) {
            return null;
        }
        // 根据标签确定类型和重要性
        let knowledgeType = 'fact';
        let importance = 0.5;
        if (tags.includes('preference')) {
            knowledgeType = 'preference';
            importance = 0.8;
        }
        else if (tags.includes('skill')) {
            knowledgeType = 'skill';
            importance = 0.9;
        }
        else if (tags.includes('experience')) {
            knowledgeType = 'experience';
            importance = 0.7;
        }
        else if (tags.includes('lesson')) {
            knowledgeType = 'lesson';
            importance = 0.85;
        }
        return {
            shouldExtract: true,
            content,
            knowledgeType,
            importance,
            tags: [...tags, 'user']
        };
    }
}
exports.RuleEngine = RuleEngine;
//# sourceMappingURL=rule-engine.js.map