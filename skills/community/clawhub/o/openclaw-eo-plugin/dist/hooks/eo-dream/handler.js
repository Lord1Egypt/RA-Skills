// ============================================================================
// EO Dream Hook Handler
// 
// Intercepts session lifecycle events to trigger dream module
// ============================================================================
// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const DREAM_CONFIG = {
    enabled: true,
    triggerOnSessionEnd: true,
    triggerOnIdle: true,
    idleTimeoutMs: 30 * 60 * 1000, // 30 minutes
    maxSessionsPerDream: 50,
};
// Track session state
let lastSessionTime = 0;
let sessionCount = 0;
let pendingDreamTrigger = false;
// ---------------------------------------------------------------------------
// Session Hook Handlers
// ---------------------------------------------------------------------------
/**
 * session_end hook
 *
 * Triggered when a session ends. Collects session data for dream analysis.
 */
export async function handleSessionEnd(event, ctx) {
    if (!DREAM_CONFIG.enabled)
        return;
    console.log('[EO Dream Hook] Session ended:', event.sessionKey);
    // Update session tracking
    sessionCount++;
    lastSessionTime = Date.now();
    // Mark that we have pending session data for dream
    pendingDreamTrigger = true;
    // Could trigger immediate dream here, but typically dreams run on schedule
    // The actual dream trigger is handled by the eo_dream tool
}
/**
 * session_start hook
 *
 * Triggered when a session starts. Could load relevant memories.
 */
export async function handleSessionStart(event, ctx) {
    if (!DREAM_CONFIG.enabled)
        return;
    console.log('[EO Dream Hook] Session started:', event.sessionKey);
    // Could inject relevant context from memory here
    // This is handled by the RAG context injection system
}
// ---------------------------------------------------------------------------
// Tool Hook Handlers (for dream-related tools)
// ---------------------------------------------------------------------------
/**
 * before_tool_call hook for dream tools
 */
export async function handleBeforeToolCall(event, ctx) {
    const { toolName } = event;
    // Only intercept dream-related tools
    if (!toolName.startsWith('eo_dream') && toolName !== 'eo_collab')
        return;
    console.log('[EO Dream Hook] Routing dream-related tool:', toolName);
    return;
}
/**
 * after_tool_call hook for dream tools
 */
export async function handleAfterToolCall(event, ctx) {
    const { toolName, result, durationMs, error } = event;
    // Only log dream-related tools
    if (!toolName.startsWith('eo_dream'))
        return;
    const status = error ? '❌' : '✅';
    const duration = durationMs ? `(${(durationMs / 1000).toFixed(1)}s)` : '';
    console.log(`[EO Dream Hook] ${toolName} completed ${status} ${duration}`);
}
// ---------------------------------------------------------------------------
// Status
// ---------------------------------------------------------------------------
export function getDreamHookStatus() {
    return {
        enabled: DREAM_CONFIG.enabled,
        pendingDreamTrigger,
        sessionCount,
        lastSessionTime,
        timeSinceLastSession: Date.now() - lastSessionTime,
    };
}
export function clearPendingDreamTrigger() {
    pendingDreamTrigger = false;
}
// ---------------------------------------------------------------------------
// Registration
// ---------------------------------------------------------------------------
export const eoDreamHookHandlers = {
    'session_end': handleSessionEnd,
    'session_start': handleSessionStart,
    'before_tool_call': handleBeforeToolCall,
    'after_tool_call': handleAfterToolCall,
};
//# sourceMappingURL=handler.js.map