/**
 * Pattern Miner
 * Extracts patterns from session history for learning
 */
export function minePatterns(sessions) {
    const patterns = [];
    // Tool sequence patterns
    const toolSequences = new Map();
    for (const session of sessions) {
        if (session.toolsUsed.length >= 2) {
            for (let i = 0; i < session.toolsUsed.length - 1; i++) {
                const seq = `${session.toolsUsed[i]} -> ${session.toolsUsed[i + 1]}`;
                toolSequences.set(seq, (toolSequences.get(seq) || 0) + 1);
            }
        }
    }
    for (const [seq, freq] of toolSequences) {
        if (freq >= 2) {
            patterns.push({ type: 'tool_sequence', pattern: seq, frequency: freq });
        }
    }
    // Topic patterns
    const topicCounts = new Map();
    for (const session of sessions) {
        for (const topic of session.commonTopics) {
            topicCounts.set(topic, (topicCounts.get(topic) || 0) + 1);
        }
    }
    for (const [topic, freq] of topicCounts) {
        if (freq >= 2) {
            patterns.push({ type: 'topic', pattern: topic, frequency: freq });
        }
    }
    return patterns.sort((a, b) => b.frequency - a.frequency);
}
export function extractTopics(message) {
    const topics = [];
    const lower = message.toLowerCase();
    const topicKeywords = {
        'project-planning': ['plan', 'project', 'milestone', 'wbs', 'schedule'],
        'architecture': ['architecture', 'design', 'microservices', 'system design'],
        'code-review': ['review', 'code', 'quality', 'security'],
        'frontend': ['frontend', 'react', 'vue', 'ui', 'css'],
        'backend': ['backend', 'api', 'database', 'server'],
        'devops': ['deploy', 'docker', 'kubernetes', 'ci/cd', 'pipeline'],
        'testing': ['test', 'qa', 'automation', 'performance'],
        'security': ['security', 'auth', 'vulnerability', 'pen test'],
    };
    for (const [topic, keywords] of Object.entries(topicKeywords)) {
        for (const kw of keywords) {
            if (lower.includes(kw)) {
                topics.push(topic);
                break;
            }
        }
    }
    return [...new Set(topics)];
}
//# sourceMappingURL=pattern-miner.js.map