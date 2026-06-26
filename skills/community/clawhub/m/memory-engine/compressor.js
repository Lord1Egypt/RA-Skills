"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ContextCompressor = void 0;
// 无意义消息模式
const MEANINGLESS_PATTERNS = [
    /^(?:好的|明白|收到|嗯|啊|哦|ok|好|是的|yes|ok|okay|yep|nope|thanks|thank you|你好|再见|辛苦|麻烦|抱歉|对不起|好吧|行|知道了)$/i,
    /^[\s]*$/,
    /^(?:嗯嗯|啊哈|哦哦|好好|是的是的)$/i,
];
// 确认消息模式
const CONFIRMATION_PATTERNS = [
    /^(?:好的|明白|收到|好的没问题|明白了|收到)$/,
    /^(?:ok|okay|yep|yeah|got it|will do|on it)$/i,
];
// 问候消息模式
const GREETING_PATTERNS = [
    /^(?:你好|您好|嗨|hello|hi|hey|早上好|下午好|晚上好)$/i,
    /^(?:再见|拜拜|下次见|bye|see you)$/i,
];
class ContextCompressor {
    maxMessages = 50;
    keepRecentCount = 10;
    enableCompression = true;
    setMaxMessages(max) {
        this.maxMessages = max;
    }
    setKeepRecentCount(count) {
        this.keepRecentCount = count;
    }
    setEnableCompression(enabled) {
        this.enableCompression = enabled;
    }
    // 压缩消息
    compress(messages) {
        if (!this.enableCompression || messages.length <= this.maxMessages) {
            return {
                messages: messages.map((m, i) => ({
                    role: m.role,
                    content: m.content,
                    originalIndex: i,
                    preserved: true
                })),
                originalCount: messages.length,
                compressedCount: messages.length,
                compressionRate: 1,
                removedCount: 0
            };
        }
        const classified = this.classifyMessages(messages);
        const compressed = this.compressMessages(classified);
        const result = {
            messages: compressed,
            originalCount: messages.length,
            compressedCount: compressed.filter(m => m.preserved).length,
            compressionRate: compressed.filter(m => m.preserved).length / messages.length,
            removedCount: messages.length - compressed.filter(m => m.preserved).length
        };
        return result;
    }
    // 分类消息
    classifyMessages(messages) {
        const classified = [];
        for (let i = 0; i < messages.length; i++) {
            const msg = messages[i];
            const category = this.categorizeMessage(msg, i, messages);
            classified.push({ message: msg, category, index: i });
        }
        return classified;
    }
    // 消息分类
    categorizeMessage(msg, index, allMessages) {
        const content = msg.content.trim();
        if (this.isMeaningless(content)) {
            return 'meaningless';
        }
        if (this.isGreeting(content)) {
            return 'greeting';
        }
        if (this.isConfirmation(content)) {
            return 'confirmation';
        }
        if (msg.role === 'system') {
            return 'system';
        }
        if (content.length > 500) {
            return 'important-long';
        }
        if (index >= allMessages.length - this.keepRecentCount) {
            return 'recent';
        }
        if (this.containsKeywords(content, ['记住', '喜欢', '帮我', '请', 'prefer', 'remember', 'please'])) {
            return 'instruction';
        }
        if (this.containsKeywords(content, ['bug', '错误', '问题', '解决', 'error', 'fix', 'issue'])) {
            return 'technical';
        }
        return 'normal';
    }
    // 压缩消息
    compressMessages(classified) {
        const result = [];
        let confirmationCount = 0;
        let greetingCount = 0;
        for (const item of classified) {
            const preserved = this.shouldPreserve(item.category, confirmationCount, greetingCount);
            if (!preserved) {
                if (item.category === 'confirmation')
                    confirmationCount++;
                if (item.category === 'greeting')
                    greetingCount++;
            }
            result.push({
                role: item.message.role,
                content: item.message.content,
                originalIndex: item.index,
                preserved,
                summary: !preserved && item.message.content.length > 20
                    ? this.summarize(item.message.content)
                    : undefined
            });
        }
        return result;
    }
    // 判断是否保留
    shouldPreserve(category, confirmationCount, greetingCount) {
        switch (category) {
            case 'system':
                return true;
            case 'recent':
                return true;
            case 'important-long':
                return true;
            case 'instruction':
                return true;
            case 'technical':
                return true;
            case 'meaningless':
                return false;
            case 'greeting':
                return greetingCount === 0;
            case 'confirmation':
                return confirmationCount < 3;
            default:
                return true;
        }
    }
    // 生成摘要
    summarize(content) {
        const sentences = content.split(/[。！？.!?]/).filter(s => s.trim());
        if (sentences.length <= 2) {
            return content.substring(0, 30) + '...';
        }
        return sentences[0].substring(0, 30) + '...';
    }
    // 获取保留的消息
    getPreservedMessages(compressed) {
        return compressed
            .filter(m => m.preserved)
            .map(m => ({ role: m.role, content: m.content }));
    }
    // 辅助方法
    isMeaningless(content) {
        return MEANINGLESS_PATTERNS.some(p => p.test(content));
    }
    isGreeting(content) {
        return GREETING_PATTERNS.some(p => p.test(content));
    }
    isConfirmation(content) {
        return CONFIRMATION_PATTERNS.some(p => p.test(content));
    }
    containsKeywords(content, keywords) {
        const lower = content.toLowerCase();
        return keywords.some(k => lower.includes(k.toLowerCase()));
    }
}
exports.ContextCompressor = ContextCompressor;
//# sourceMappingURL=compressor.js.map