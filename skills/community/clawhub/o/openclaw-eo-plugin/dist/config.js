/**
 * EO Plugin Configuration
 * Centralized constants for the Everything Openclaw plugin
 */
export const PLUGIN_VERSION = '3.0.3';
export const EXPERT_COUNT = 141;
export const WORKSPACE = process.cwd();
// Tool IDs
export const TOOL_IDS = {
    COLLAB: 'eo_collab',
    LIST_EXPERTS: 'eo_list_experts',
    PLAN: 'eo_plan',
    ARCHITECT: 'eo_architect',
    VERIFY: 'eo_verify',
    CODE_REVIEW: 'eo_code_review',
    DREAM: 'eo_dream',
    SELF_LEARN: 'eo_self_learn',
    RAG_QUERY: 'eo_rag_query',
    MEMORY_STATS: 'eo_memory_stats',
    EVOLVE: 'eo_evolve', // NEW: Closed-loop evolution
};
// Hook IDs
export const HOOK_IDS = {
    SESSION_START: 'eo_session_start',
    SESSION_END: 'eo_session_end',
    PROACTIVE_MONITOR: 'eo_proactive_monitor',
    DREAM_TRIGGER: 'eo_dream_trigger',
};
// Default timeouts (ms)
export const TIMEOUTS = {
    PLAN: 120000,
    ARCHITECT: 180000,
    VERIFY: 120000,
    CODE_REVIEW: 180000,
    DREAM: 300000,
};
// Architecture styles
export const ARCH_STYLES = ['layered', 'microservices', 'serverless', 'event-driven'];
// Languages
export const LANGUAGES = ['typescript', 'python', 'java', 'go', 'rust'];
// Clouds
export const CLOUDS = ['aws', 'gcp', 'azure', 'multi-cloud'];
// Review depths
export const REVIEW_DEPTHS = ['quick', 'standard', 'deep'];
// Checkpoint types
export const VERIFY_TYPES = ['code', 'architecture', 'test', 'security', 'performance'];
//# sourceMappingURL=config.js.map