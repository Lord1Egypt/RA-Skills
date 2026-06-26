"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.KnowledgeExtractor = void 0;
const embedding_1 = require("./embedding");
class KnowledgeExtractor {
    embeddingModel;
    constructor() {
        this.embeddingModel = new embedding_1.EmbeddingModel();
    }
    async initialize() {
        await this.embeddingModel.load();
    }
    // 从用户消息提取知识
    async extractFromUserMessage(content) {
        const trimmed = content.trim();
        if (trimmed.length < 3) {
            return null;
        }
        // 使用 embedding 模型提取标签
        const extractedTags = await this.embeddingModel.extractTags(trimmed);
        // 根据标签确定知识类型和重要性
        const { knowledgeType, importance } = this.determineKnowledgeType(extractedTags, trimmed);
        if (!knowledgeType) {
            return null;
        }
        return {
            shouldExtract: true,
            content: trimmed,
            knowledgeType,
            importance,
            tags: [...extractedTags, 'user']
        };
    }
    // 根据标签确定知识类型
    determineKnowledgeType(tags, content) {
        // 检查标签中是否包含特定类型
        if (tags.includes('preference') || tags.includes('food')) {
            return { knowledgeType: 'preference', importance: 0.8 };
        }
        if (tags.includes('skill') || tags.includes('programming')) {
            return { knowledgeType: 'skill', importance: 0.9 };
        }
        if (tags.includes('experience')) {
            return { knowledgeType: 'experience', importance: 0.7 };
        }
        if (tags.includes('lesson')) {
            return { knowledgeType: 'lesson', importance: 0.85 };
        }
        if (tags.includes('age') || tags.includes('identity') || tags.includes('location')) {
            return { knowledgeType: 'fact', importance: 0.6 };
        }
        // 默认类型
        return { knowledgeType: 'fact', importance: 0.5 };
    }
    // 从AI消息提取知识
    async extractFromAIMessage(content, userMessage) {
        const trimmed = content.trim();
        if (trimmed.length < 10) {
            return null;
        }
        // 使用 embedding 模型提取标签
        const extractedTags = await this.embeddingModel.extractTags(trimmed);
        // 检测解决方案
        if (this.isSolution(trimmed)) {
            return {
                shouldExtract: true,
                content: trimmed.substring(0, 500),
                knowledgeType: 'experience',
                importance: 0.85,
                tags: ['solution', 'learned', ...extractedTags],
                metadata: {
                    problemContext: userMessage?.substring(0, 100),
                    extractedAt: Date.now()
                }
            };
        }
        // 检测技术解释
        if (this.isTechnicalExplanation(trimmed)) {
            return {
                shouldExtract: true,
                content: trimmed.substring(0, 500),
                knowledgeType: 'skill',
                importance: 0.7,
                tags: ['knowledge', 'learned', ...extractedTags]
            };
        }
        return null;
    }
    // 从对话对提取知识
    async extractFromConversationPair(userMessage, aiMessage) {
        const results = [];
        const userKnowledge = await this.extractFromUserMessage(userMessage);
        if (userKnowledge) {
            results.push(userKnowledge);
        }
        const aiKnowledge = await this.extractFromAIMessage(aiMessage, userMessage);
        if (aiKnowledge) {
            results.push(aiKnowledge);
        }
        // 检测问题解决
        if (this.isProblemSolving(userMessage, aiMessage)) {
            results.push({
                shouldExtract: true,
                content: `问题: ${userMessage.substring(0, 200)}\n解决: ${aiMessage.substring(0, 300)}`,
                knowledgeType: 'experience',
                importance: 0.9,
                tags: ['problem-solved', 'experience'],
                metadata: {
                    originalProblem: userMessage,
                    solution: aiMessage
                }
            });
        }
        return results;
    }
    // 辅助方法：检测解决方案
    isSolution(content) {
        const patterns = [
            /(?:解决|修复|处理)(?:了|的)(?:问题|bug|错误)(.{5,30})/i,
            /(?:通过|使用|采用)(?:了|的)(?:方法|方案|策略)(.{5,30})/i,
            /(?:最终|最后)(?:用|采用|选择)(.{5,30})/i,
        ];
        return patterns.some(p => p.test(content));
    }
    // 辅助方法：检测技术解释
    isTechnicalExplanation(content) {
        const techIndicators = [
            /可以(?:这样|这样|这么)/,
            /步骤[:：]/,
            /首先|其次|最后|然后/,
            /原理是/,
            /原因是/,
            /实现方式/,
            /代码[:：]/,
            /示例[:：]/,
            /example|step|process|method|function/i,
        ];
        return techIndicators.some(p => p.test(content)) && content.length > 50;
    }
    // 辅助方法：检测问题解决
    isProblemSolving(userMsg, aiMsg) {
        const problemIndicators = [
            /怎么|如何|怎么办|为什么|为什么不行/,
            /解决|修复|处理|bug|错误|报错/,
            /不行|没用|不工作|失败/,
            /how (?:to|do|can)|why (?:doesn't|not)|fix|debug|error|bug/i,
        ];
        const solvedIndicators = [
            /可以|这样|试试|尝试|用这个方法/,
            /解决|修复|搞定|完成|成功/,
            /try this|use this|here's (?:how|what)/i,
            /solution|fix|resolve|fix this/i,
        ];
        const hasProblem = problemIndicators.some(p => p.test(userMsg));
        const hasSolution = solvedIndicators.some(p => p.test(aiMsg));
        return hasProblem && hasSolution;
    }
}
exports.KnowledgeExtractor = KnowledgeExtractor;
//# sourceMappingURL=extractor.js.map