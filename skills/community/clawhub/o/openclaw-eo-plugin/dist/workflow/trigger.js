/**
 * Workflow Trigger
 * Detects when workflows should be invoked
 */
export class WorkflowTrigger {
    /**
     * Check if a message matches trigger conditions
     */
    static matchesMessage(trigger, message) {
        if (trigger.type !== 'message')
            return false;
        const lowerMessage = message.toLowerCase();
        // Check keywords
        if (trigger.keywords && trigger.keywords.length > 0) {
            const hasKeyword = trigger.keywords.some(kw => lowerMessage.includes(kw.toLowerCase()));
            if (hasKeyword)
                return true;
        }
        // Check regex pattern
        if (trigger.pattern) {
            try {
                const regex = new RegExp(trigger.pattern, 'i');
                if (regex.test(message))
                    return true;
            }
            catch {
                // Invalid regex, skip
            }
        }
        return false;
    }
    /**
     * Check if a tool call matches trigger conditions
     */
    static matchesToolCall(trigger, toolName) {
        if (trigger.type !== 'tool_call')
            return false;
        if (trigger.toolCall) {
            return toolName === trigger.toolCall || toolName.includes(trigger.toolCall);
        }
        return false;
    }
    /**
     * Check if trigger type matches
     */
    static matchesType(trigger, type) {
        return trigger.type === type;
    }
    /**
     * Find matching workflows for a given context
     */
    static findMatchingWorkflows(workflows, context) {
        const matches = [];
        for (const workflow of workflows) {
            if (!workflow.trigger)
                continue;
            if (workflow.status !== 'idle' && workflow.status !== 'paused')
                continue;
            let isMatch = false;
            switch (workflow.trigger.type) {
                case 'message':
                    if (context.message) {
                        isMatch = this.matchesMessage(workflow.trigger, context.message);
                    }
                    break;
                case 'tool_call':
                    if (context.toolCall) {
                        isMatch = this.matchesToolCall(workflow.trigger, context.toolCall);
                    }
                    break;
                case 'context_level':
                    if (context.contextLevel) {
                        isMatch = workflow.trigger.custom === context.contextLevel;
                    }
                    break;
                case 'manual':
                    // Manual triggers are never auto-matched
                    break;
            }
            if (isMatch)
                matches.push(workflow);
        }
        return matches;
    }
    /**
     * Create a simple keyword trigger
     */
    static keywordTrigger(keywords) {
        return {
            type: 'message',
            keywords,
        };
    }
    /**
     * Create a tool call trigger
     */
    static toolTrigger(toolName) {
        return {
            type: 'tool_call',
            toolCall: toolName,
        };
    }
    /**
     * Create a context level trigger
     */
    static contextLevelTrigger(level) {
        return {
            type: 'context_level',
            custom: level,
        };
    }
}
//# sourceMappingURL=trigger.js.map