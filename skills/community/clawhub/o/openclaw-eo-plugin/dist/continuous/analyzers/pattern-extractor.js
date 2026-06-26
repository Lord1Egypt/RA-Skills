/**
 * Pattern Extractor
 * Extracts patterns from analyzed sessions for the learning loop
 */
export class PatternExtractor {
    patternLibrary = new Map();
    /**
     * Extract patterns from session analysis
     */
    async extract(session) {
        const patterns = [];
        // Extract workflow patterns
        const workflowPattern = this.extractWorkflowPattern(session);
        if (workflowPattern)
            patterns.push(workflowPattern);
        // Extract expert usage patterns
        const expertPatterns = this.extractExpertPatterns(session);
        patterns.push(...expertPatterns);
        // Extract error patterns
        const errorPatterns = this.extractErrorPatterns(session);
        patterns.push(...errorPatterns);
        // Extract topic patterns
        const topicPatterns = this.extractTopicPatterns(session);
        patterns.push(...topicPatterns);
        // Update library with new patterns
        for (const pattern of patterns) {
            this.updatePatternLibrary(pattern);
        }
        return patterns;
    }
    /**
     * Extract workflow pattern
     */
    extractWorkflowPattern(session) {
        if (session.workflowType === 'unknown')
            return null;
        return {
            id: `wf-${session.workflowType}-${Date.now()}`,
            name: `${session.workflowType.charAt(0).toUpperCase() + session.workflowType.slice(1)} Workflow`,
            description: `Detected ${session.workflowType} workflow in session`,
            type: 'workflow',
            frequency: 1,
            evidence: [`Message count: ${session.messageCount}`, `Tools used: ${session.toolsUsed.join(', ')}`],
            severity: 'low',
            timestamp: Date.now(),
        };
    }
    /**
     * Extract expert usage patterns
     */
    extractExpertPatterns(session) {
        const patterns = [];
        for (const [expert, count] of session.expertUsage) {
            if (count >= 1) {
                patterns.push({
                    id: `expert-${expert}-${Date.now()}`,
                    name: `Expert Usage: ${expert}`,
                    description: `${expert} was used ${count} time(s) in this session`,
                    type: 'expert_sequence',
                    frequency: count,
                    evidence: [`Tool: ${expert}`, `Count: ${count}`],
                    severity: 'low',
                    timestamp: Date.now(),
                });
            }
        }
        return patterns;
    }
    /**
     * Extract error patterns
     */
    extractErrorPatterns(session) {
        const patterns = [];
        for (const error of session.errorIndicators) {
            patterns.push({
                id: `err-${error.type}-${Date.now()}`,
                name: `Error Pattern: ${error.type}`,
                description: error.description,
                type: 'error',
                frequency: error.count,
                evidence: [`Severity: ${error.severity}`, `Count: ${error.count}`],
                severity: error.severity,
                suggestedAction: this.getSuggestedFix(error),
                timestamp: Date.now(),
            });
        }
        return patterns;
    }
    /**
     * Extract topic patterns
     */
    extractTopicPatterns(session) {
        const patterns = [];
        for (const topic of session.keyTopics) {
            patterns.push({
                id: `topic-${topic}-${Date.now()}`,
                name: `Topic: ${topic}`,
                description: `Session covered ${topic} topic`,
                type: 'topic',
                frequency: 1,
                evidence: [`Topic: ${topic}`],
                severity: 'low',
                timestamp: Date.now(),
            });
        }
        return patterns;
    }
    /**
     * Get suggested fix for error type
     */
    getSuggestedFix(error) {
        const fixes = {
            error_keyword: 'Review error message and apply appropriate fix',
            failed_tool: 'Check tool configuration and retry with corrected parameters',
            retry: 'Retry the operation with exponential backoff',
        };
        return fixes[error.type] || 'Investigate and resolve the issue';
    }
    /**
     * Update pattern library
     */
    updatePatternLibrary(pattern) {
        const existingKey = `${pattern.type}-${pattern.name}`;
        if (this.patternLibrary.has(existingKey)) {
            const existing = this.patternLibrary.get(existingKey);
            existing.frequency += pattern.frequency;
            existing.evidence.push(...pattern.evidence.slice(0, 3)); // Keep max 3 new evidence items
        }
        else {
            this.patternLibrary.set(existingKey, { ...pattern });
        }
    }
    /**
     * Get all patterns from library
     */
    getPatterns() {
        return Array.from(this.patternLibrary.values());
    }
    /**
     * Get patterns by type
     */
    getPatternsByType(type) {
        return this.getPatterns().filter(p => p.type === type);
    }
    /**
     * Get high severity patterns
     */
    getHighSeverityPatterns() {
        return this.getPatterns().filter(p => p.severity === 'high');
    }
    /**
     * Get pattern summary
     */
    getSummary() {
        const patterns = this.getPatterns();
        const byType = {};
        for (const pattern of patterns) {
            byType[pattern.type] = (byType[pattern.type] || 0) + 1;
        }
        return {
            total: patterns.length,
            byType,
            highSeverity: patterns.filter(p => p.severity === 'high').length,
        };
    }
}
//# sourceMappingURL=pattern-extractor.js.map