/**
 * EO Plugin Configuration
 * Centralized constants for the Everything Openclaw plugin
 */
export declare const PLUGIN_VERSION = "3.0.3";
export declare const EXPERT_COUNT = 141;
export declare const WORKSPACE: string;
export declare const TOOL_IDS: {
    readonly COLLAB: "eo_collab";
    readonly LIST_EXPERTS: "eo_list_experts";
    readonly PLAN: "eo_plan";
    readonly ARCHITECT: "eo_architect";
    readonly VERIFY: "eo_verify";
    readonly CODE_REVIEW: "eo_code_review";
    readonly DREAM: "eo_dream";
    readonly SELF_LEARN: "eo_self_learn";
    readonly RAG_QUERY: "eo_rag_query";
    readonly MEMORY_STATS: "eo_memory_stats";
    readonly EVOLVE: "eo_evolve";
};
export declare const HOOK_IDS: {
    readonly SESSION_START: "eo_session_start";
    readonly SESSION_END: "eo_session_end";
    readonly PROACTIVE_MONITOR: "eo_proactive_monitor";
    readonly DREAM_TRIGGER: "eo_dream_trigger";
};
export declare const TIMEOUTS: {
    readonly PLAN: 120000;
    readonly ARCHITECT: 180000;
    readonly VERIFY: 120000;
    readonly CODE_REVIEW: 180000;
    readonly DREAM: 300000;
};
export declare const ARCH_STYLES: readonly ["layered", "microservices", "serverless", "event-driven"];
export declare const LANGUAGES: readonly ["typescript", "python", "java", "go", "rust"];
export declare const CLOUDS: readonly ["aws", "gcp", "azure", "multi-cloud"];
export declare const REVIEW_DEPTHS: readonly ["quick", "standard", "deep"];
export declare const VERIFY_TYPES: readonly ["code", "architecture", "test", "security", "performance"];
//# sourceMappingURL=config.d.ts.map