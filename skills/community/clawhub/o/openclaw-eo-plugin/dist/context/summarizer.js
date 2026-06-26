/**
 * Smart Context Summarizer
 * Compresses old conversation into key points while preserving critical info
 */
export class ContextSummarizer {
    minImportanceThreshold;
    constructor(minImportanceThreshold = 30) {
        this.minImportanceThreshold = minImportanceThreshold;
    }
    /**
     * Generate a unique ID
     */
    generateId() {
        return `sum_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    }
    /**
     * Extract key information from items
     */
    extractKeyInfo(items) {
        const keyPoints = [];
        for (const item of items) {
            if (item.importance >= this.minImportanceThreshold && item.keyInfo) {
                keyPoints.push(...item.keyInfo);
            }
            else if (item.importance >= 70) {
                // High importance items - extract first 100 chars as summary
                const summary = item.content.substring(0, 100).trim();
                if (summary)
                    keyPoints.push(`[${item.type}] ${summary}...`);
            }
        }
        return [...new Set(keyPoints)].slice(0, 20); // Dedupe and limit
    }
    /**
     * Identify key decisions from conversation
     */
    extractDecisions(items) {
        const decisions = [];
        const decisionPatterns = [
            /decided to/i,
            /chose to/i,
            /will use/i,
            /going with/i,
            /selected/i,
            /approved/i,
            /agreed on/i,
            /conclusion:*/i,
        ];
        for (const item of items) {
            if (item.type === 'message' || item.type === 'result') {
                for (const pattern of decisionPatterns) {
                    if (pattern.test(item.content)) {
                        decisions.push(item.content.substring(0, 150).trim());
                        break;
                    }
                }
            }
        }
        return decisions.slice(0, 10);
    }
    /**
     * Extract user preferences from conversation
     */
    extractPreferences(items) {
        const prefs = {};
        const prefPatterns = [
            { pattern: /prefer[s]? (.+)/i, key: 'general' },
            { pattern: /like[s]? (.+)/i, key: 'general' },
            { pattern: /use[s]? (.+)/i, key: 'technology' },
            { pattern: /want[s]? (.+)/i, key: 'requirements' },
        ];
        for (const item of items) {
            if (item.type === 'message' && item.importance >= 50) {
                for (const { pattern, key } of prefPatterns) {
                    const match = item.content.match(pattern);
                    if (match && !prefs[key]) {
                        prefs[key] = match[1].substring(0, 100);
                    }
                }
            }
        }
        return prefs;
    }
    /**
     * Determine current task state from recent items
     */
    extractTaskState(items) {
        const recentMessages = items
            .filter(i => i.type === 'message')
            .sort((a, b) => b.timestamp - a.timestamp)
            .slice(0, 3);
        if (recentMessages.length === 0)
            return 'No active task';
        const lastMessage = recentMessages[0].content;
        // Return last 200 chars as state indicator
        return lastMessage.substring(0, 200).trim() + (lastMessage.length > 200 ? '...' : '');
    }
    /**
     * Create a summary from a list of items
     */
    summarize(items) {
        const sortedItems = [...items].sort((a, b) => a.timestamp - b.timestamp);
        return {
            id: this.generateId(),
            originalCount: items.length,
            condensedCount: Math.ceil(items.length * 0.2), // Compress to ~20%
            keyPoints: this.extractKeyInfo(sortedItems),
            preservedDecisions: this.extractDecisions(sortedItems),
            userPreferences: this.extractPreferences(sortedItems),
            currentTaskState: this.extractTaskState(sortedItems),
            timestamp: Date.now(),
        };
    }
    /**
     * Mark a message as having key info
     */
    static markAsKeyInfo(item, keyInfo) {
        return { ...item, keyInfo };
    }
}
//# sourceMappingURL=summarizer.js.map