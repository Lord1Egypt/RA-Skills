/**
 * Pattern Learner - Learn from Successful Execution Paths
 *
 * Analyzes historical sessions to extract successful patterns
 * and stores them in RAG L2 for reuse.
 *
 * This enables:
 * - Learning from successes (not just failures)
 * - Reducing user intervention by following proven paths
 * - Building a reusable pattern library
 */
import { getSharedRAGSystem } from '../rag/rag-system.js';
/**
 * Pattern Learner - Extracts and stores successful patterns
 */
export class PatternLearner {
    ragSystem = getSharedRAGSystem();
    patterns = [];
    /**
     * Analyze a session and extract successful patterns
     */
    async analyzeSession(sessionKey, sessionData) {
        const patterns = [];
        // Find successful task completions
        const messages = sessionData.messages || [];
        let taskStart = '';
        let taskSteps = [];
        let taskTools = [];
        let taskSuccess = true;
        for (const msg of messages) {
            if (msg.role === 'user' && this.isTaskStart(msg.content)) {
                // New task starts
                if (taskStart && taskSteps.length > 0) {
                    // Analyze previous task
                    const pattern = this.createPattern(taskStart, taskSteps, taskTools, taskSuccess);
                    if (pattern)
                        patterns.push(pattern);
                }
                taskStart = this.extractTaskDescription(msg.content);
                taskSteps = [];
                taskTools = [];
                taskSuccess = true;
            }
            if (msg.role === 'assistant' && msg.tools) {
                for (const tool of msg.tools) {
                    if (!taskTools.includes(tool)) {
                        taskTools.push(tool);
                    }
                    taskSteps.push(`tool:${tool}`);
                }
            }
            if (msg.role === 'tool_result' && msg.isError) {
                taskSuccess = false;
            }
        }
        // Don't forget the last task
        if (taskStart && taskSteps.length > 0) {
            const pattern = this.createPattern(taskStart, taskSteps, taskTools, taskSuccess);
            if (pattern)
                patterns.push(pattern);
        }
        return patterns;
    }
    /**
     * Analyze multiple sessions and build pattern library
     */
    async learnFromSessions(sessions) {
        const allPatterns = [];
        for (const session of sessions) {
            const patterns = await this.analyzeSession(session.key, session.data);
            allPatterns.push(...patterns);
        }
        // Merge similar patterns and calculate confidence
        const mergedPatterns = this.mergePatterns(allPatterns);
        // Store in RAG
        let stored = 0;
        for (const pattern of mergedPatterns) {
            if (pattern.confidence >= 0.5) { // Only store patterns with 50%+ confidence
                await this.storePattern(pattern);
                stored++;
            }
        }
        this.patterns = mergedPatterns;
        return {
            patternsLearned: mergedPatterns.length,
            highConfidence: stored,
        };
    }
    /**
     * Store pattern in RAG L2
     */
    async storePattern(pattern) {
        const content = `
## Pattern: ${pattern.name}

### Task Type
${pattern.taskType}

### Description
${pattern.description}

### Execution Steps
${pattern.pattern}

### Tools Used
${pattern.tools.join(', ')}

### Success Indicators
${pattern.successIndicators.join('\n')}

### Applicable Scenarios
${pattern.适用场景.join('\n')}

### Example Task
${pattern.示例Task || 'N/A'}

### Confidence
${(pattern.confidence * 100).toFixed(0)}% (based on ${Math.round(pattern.confidence * 10)} occurrences)

---
*Last used: ${pattern.lastUsed}*
`.trim();
        await this.ragSystem.indexChunk({
            layer: 2,
            content,
            metadata: {
                source: 'pattern-library',
                patternName: pattern.name,
                taskType: pattern.taskType,
                acl: 'public',
            },
        });
    }
    /**
     * Retrieve relevant patterns for a task
     */
    async retrievePatterns(taskQuery, topK = 3) {
        const result = await this.ragSystem.quickSearch(taskQuery, topK);
        return result.chunks
            .filter(c => c.metadata.patternName)
            .map(c => ({
            id: c.id,
            name: c.metadata.patternName || c.id,
            taskType: c.metadata.taskType || 'unknown',
            description: c.content.substring(0, 200),
            pattern: c.content,
            tools: [],
            successIndicators: [],
            适用场景: [],
            confidence: c.score || 0.5,
            lastUsed: new Date().toISOString(),
        }));
    }
    /**
     * Extract text content from message
     */
    extractText(content) {
        if (typeof content === 'string')
            return content;
        if (Array.isArray(content)) {
            return content.map(c => typeof c === 'string' ? c : c?.text || '').join(' ');
        }
        if (typeof content === 'object' && content !== null) {
            return content.text || JSON.stringify(content);
        }
        return String(content);
    }
    /**
     * Check if message indicates task start
     */
    isTaskStart(content) {
        const text = this.extractText(content);
        const keywords = [
            '帮我', '帮我做', '请完成', '开始', '执行',
            'build', 'create', 'implement', 'fix', 'write',
            '开发', '实现', '修复', '编写'
        ];
        return keywords.some(k => text.toLowerCase().includes(k));
    }
    /**
     * Extract task description from message
     */
    extractTaskDescription(content) {
        const text = this.extractText(content);
        // Remove conversation metadata and extract main task
        const lines = text.split('\n');
        const taskLines = lines.filter(l => !l.includes('metadata') && !l.includes('message_id'));
        return taskLines.join(' ').substring(0, 200);
    }
    /**
     * Create a pattern from task execution
     */
    createPattern(task, steps, tools, success) {
        if (steps.length < 2)
            return null; // Need at least 2 steps
        return {
            id: `pattern-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            name: this.generatePatternName(task),
            taskType: this.classifyTask(task),
            description: task,
            pattern: steps.join(' → '),
            tools,
            successIndicators: success ? ['任务成功完成'] : ['任务未完全成功'],
            适用场景: [this.classifyTask(task)],
            示例Task: task,
            confidence: success ? 0.7 : 0.3,
            lastUsed: new Date().toISOString(),
        };
    }
    /**
     * Classify task type
     */
    classifyTask(task) {
        const taskLower = task.toLowerCase();
        if (taskLower.includes('代码') || taskLower.includes('开发') || taskLower.includes('function')) {
            return '代码开发';
        }
        if (taskLower.includes('架构') || taskLower.includes('design')) {
            return '架构设计';
        }
        if (taskLower.includes('论文') || taskLower.includes('paper')) {
            return '论文写作';
        }
        if (taskLower.includes('规划') || taskLower.includes('plan')) {
            return '项目规划';
        }
        if (taskLower.includes('bug') || taskLower.includes('修复')) {
            return 'Bug修复';
        }
        if (taskLower.includes('部署') || taskLower.includes('deploy')) {
            return '部署发布';
        }
        if (taskLower.includes('测试') || taskLower.includes('test')) {
            return '测试验证';
        }
        return '通用任务';
    }
    /**
     * Generate pattern name
     */
    generatePatternName(task) {
        const type = this.classifyTask(task);
        return `${type}-Pattern-${Date.now().toString(36).slice(-4)}`;
    }
    /**
     * Merge similar patterns
     */
    mergePatterns(patterns) {
        const merged = new Map();
        // Group by task type
        for (const p of patterns) {
            const key = p.taskType;
            if (!merged.has(key)) {
                merged.set(key, []);
            }
            merged.get(key).push(p);
        }
        // Calculate confidence for merged patterns
        const result = [];
        for (const [taskType, group] of merged) {
            if (group.length === 0)
                continue;
            // Merge into single high-confidence pattern
            const avgConfidence = group.reduce((sum, p) => sum + p.confidence, 0) / group.length;
            result.push({
                id: group[0].id,
                name: group[0].name,
                taskType,
                description: group[0].description,
                pattern: group.map(p => p.pattern).join('\n---\n'),
                tools: [...new Set(group.flatMap(p => p.tools))],
                successIndicators: ['基于' + group.length + '个相似任务总结'],
                适用场景: [taskType],
                示例Task: group[0].示例Task,
                confidence: Math.min(avgConfidence + 0.1, 1.0), // Boost confidence for multiple occurrences
                lastUsed: new Date().toISOString(),
            });
        }
        return result;
    }
    /**
     * Get stored patterns count
     */
    async getStats() {
        const chunks = await this.ragSystem.getChunksBySource('pattern-library');
        const byType = {};
        for (const chunk of chunks) {
            const type = chunk.metadata.taskType || 'unknown';
            byType[type] = (byType[type] || 0) + 1;
        }
        return {
            totalPatterns: chunks.length,
            byType,
        };
    }
}
// Singleton
export const patternLearner = new PatternLearner();
//# sourceMappingURL=pattern-learner.js.map