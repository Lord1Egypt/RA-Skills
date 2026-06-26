/**
 * Context Module Types
 * Type definitions for proactive context management
 */
export const DEFAULT_THRESHOLDS = {
    warning: 70,
    compress: 85,
    critical: 95,
};
export var ContextLevel;
(function (ContextLevel) {
    ContextLevel["NORMAL"] = "normal";
    ContextLevel["WARNING"] = "warning";
    ContextLevel["COMPRESS"] = "compress";
    ContextLevel["CRITICAL"] = "critical";
})(ContextLevel || (ContextLevel = {}));
export const DEFAULT_EVICTION_POLICY = {
    name: 'default',
    minImportance: 30,
    maxAge: 30 * 60 * 1000, // 30 minutes
    preserveRecent: 5,
};
//# sourceMappingURL=types.js.map