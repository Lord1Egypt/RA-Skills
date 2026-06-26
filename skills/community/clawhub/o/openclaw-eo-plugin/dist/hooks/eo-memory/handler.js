// ============================================================================
// EO Memory Hook Handler
// 
// Handles proactive memory saving and loading for session continuity.
// Inspired by Claude Code's memdir.ts and memoryTypes.ts
// ============================================================================
// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------
const ENTRYPOINT_NAME = 'MEMORY.md';
const MAX_ENTRYPOINT_LINES = 200;
const MAX_ENTRYPOINT_BYTES = 25_000;
const TOPICS_DIR = 'topics';
const MEMORY_DIR = 'memory';
// Memory types
export const MEMORY_TYPES = ['user', 'feedback', 'project', 'reference'];
// Track in-memory state
let memoryStore = new Map();
let lastSaveTime = 0;
// ---------------------------------------------------------------------------
// Session Hook Handlers
// ---------------------------------------------------------------------------
/**
 * session_end hook
 *
 * Proactively saves key information from the session to memory.
 */
export async function handleSessionEnd(event, ctx) {
    console.log('[EO Memory Hook] Session ended:', event.sessionKey);
    // In a full implementation, this would:
    // 1. Extract key information from the session
    // 2. Update MEMORY.md with significant events
    // 3. Create/update topic files for specific memories
    // 4. Truncate MEMORY.md if it exceeds line/byte limits
    lastSaveTime = Date.now();
    // Store session summary in memory
    const sessionKey = event.sessionKey || 'default';
    const today = new Date().toISOString().slice(0, 10);
    memoryStore.set(`session-${today}`, {
        name: `Session ${today}`,
        description: `Session activities from ${today}`,
        type: 'project',
        content: `Session: ${sessionKey}\nEnded: ${new Date().toISOString()}\n`,
        created: today,
        updated: today,
    });
    console.log('[EO Memory Hook] Session memory saved');
}
/**
 * session_start hook
 *
 * Loads relevant memories when a session starts.
 */
export async function handleSessionStart(event, ctx) {
    console.log('[EO Memory Hook] Session started:', event.sessionKey);
    // In a full implementation, this would:
    // 1. Read MEMORY.md for long-term context
    // 2. Search topics/ for relevant memories
    // 3. Inject relevant context into the session
    // 4. Use semantic search to find related memories
    const relevantMemories = findRelevantMemories(event.sessionKey || '');
    if (relevantMemories.length > 0) {
        console.log(`[EO Memory Hook] Found ${relevantMemories.length} relevant memories`);
        // The actual injection would be handled by RAG context injection
    }
}
/**
 * Find memories relevant to a session
 */
function findRelevantMemories(sessionKey) {
    const memories = [];
    // Simple keyword matching
    const keywords = sessionKey.toLowerCase().split(/[/\-_]/);
    for (const [key, entry] of memoryStore) {
        const keyLower = key.toLowerCase();
        for (const keyword of keywords) {
            if (keyword.length > 2 && keyLower.includes(keyword)) {
                memories.push(entry);
                break;
            }
        }
    }
    return memories;
}
// ---------------------------------------------------------------------------
// Memory Statistics
// ---------------------------------------------------------------------------
export function getMemoryStats() {
    const byType = {};
    let sizeBytes = 0;
    for (const entry of memoryStore.values()) {
        byType[entry.type] = (byType[entry.type] || 0) + 1;
        sizeBytes += entry.content.length;
    }
    return {
        totalEntries: memoryStore.size,
        byType,
        lastSaveTime,
        sizeBytes,
    };
}
// ---------------------------------------------------------------------------
// Registration
// ---------------------------------------------------------------------------
export const eoMemoryHookHandlers = {
    'session_end': handleSessionEnd,
    'session_start': handleSessionStart,
};
//# sourceMappingURL=handler.js.map