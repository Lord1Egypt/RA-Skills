/**
 * Hooks Index
 * Unified exports for all hooks
 */
export { createSessionStartHook, initMemorySync, getMemorySync, type SessionStartContext } from './session-start.js';
export { createSessionEndHook, onSessionEnd, type SessionEndData } from './session-end.js';
export { createProactiveMonitorHook } from './proactive-monitor.js';
export { createDreamTriggerHook } from './dream-trigger.js';
export { configureProactiveMonitor, checkMessage } from './proactive-monitor.js';
export { configureDreamTrigger, incrementSession, shouldTriggerDream, triggerDream } from './dream-trigger.js';
export { initContextWorkflowHooks, onMessageHook, afterToolCallHook, getContextManager, getActiveWorkflows, } from './context-workflow.js';
export { AfterOutcomeHook, afterOutcomeHook, type OutcomeHookEvent } from './after-outcome.js';
export { createRuleEnforcementHook, configureRuleEnforcement, getEnforcementStats } from './rule-enforcement-hook.js';
export { createNewConversationHook, needsAllocation, getAllocationHint, type NewConversationContext, } from './new-conversation.js';
//# sourceMappingURL=index.d.ts.map