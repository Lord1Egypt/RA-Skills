/**
 * Hooks Index
 * Unified exports for all hooks
 */
// Hook creators (accept api parameter)
export { createSessionStartHook, initMemorySync, getMemorySync } from './session-start.js';
export { createSessionEndHook, onSessionEnd } from './session-end.js';
export { createProactiveMonitorHook } from './proactive-monitor.js';
export { createDreamTriggerHook } from './dream-trigger.js';
// Hook utilities
export { configureProactiveMonitor, checkMessage } from './proactive-monitor.js';
export { configureDreamTrigger, incrementSession, shouldTriggerDream, triggerDream } from './dream-trigger.js';
// Context and Workflow hooks (v2.6)
export { initContextWorkflowHooks, onMessageHook, afterToolCallHook, getContextManager, getActiveWorkflows, } from './context-workflow.js';
// After Outcome Hook (v2.8)
export { AfterOutcomeHook, afterOutcomeHook } from './after-outcome.js';
// Rule Enforcement Hook (v3.1 - Hybrid Architecture)
export { createRuleEnforcementHook, configureRuleEnforcement, getEnforcementStats } from './rule-enforcement-hook.js';
// New Conversation Hook (v3.2 - Auto Workspace Allocation)
export { createNewConversationHook, needsAllocation, getAllocationHint, } from './new-conversation.js';
//# sourceMappingURL=index.js.map