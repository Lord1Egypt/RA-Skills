/**
 * Continuous Learner
 * Ongoing learning loop that improves EO performance
 */
import { minePatterns, extractTopics } from './pattern-miner.js';
export class ContinuousLearner {
    sessions = [];
    patterns = [];
    workspace;
    constructor(workspace) {
        this.workspace = workspace;
    }
    addSession(toolsUsed, message) {
        const topics = extractTopics(message);
        this.sessions.push({
            toolsUsed,
            commonTopics: topics,
            expertInvocations: toolsUsed.filter(t => t.startsWith('eo_') && t !== 'eo_collab' && t !== 'eo_list_experts').length,
            timestamp: Date.now(),
        });
        // Re-mine patterns periodically
        if (this.sessions.length % 5 === 0) {
            this.patterns = minePatterns(this.sessions);
        }
    }
    getPatterns() {
        return this.patterns;
    }
    getReport() {
        const topicsLearned = [...new Set(this.sessions.flatMap(s => s.commonTopics))];
        return {
            sessionsAnalyzed: this.sessions.length,
            newPatterns: this.patterns.length,
            topicsLearned,
            suggestions: this.generateSuggestions(),
        };
    }
    generateSuggestions() {
        const suggestions = [];
        // Suggest based on common tool sequences
        const toolSeqs = this.patterns.filter(p => p.type === 'tool_sequence');
        if (toolSeqs.length > 0) {
            suggestions.push(`Common workflow: ${toolSeqs[0].pattern}`);
        }
        // Suggest based on frequent topics
        const topics = this.patterns.filter(p => p.type === 'topic');
        if (topics.length > 0) {
            suggestions.push(`Frequently worked on: ${topics.map(t => t.pattern).join(', ')}`);
        }
        return suggestions;
    }
}
//# sourceMappingURL=continuous-learner.js.map