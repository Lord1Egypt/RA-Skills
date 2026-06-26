/**
 * Memory Types - Cross-Session Memory System
 * Defines all types for the EO memory architecture
 */
// Memory Priority Levels
export var MemoryPriority;
(function (MemoryPriority) {
    MemoryPriority[MemoryPriority["P0_CRITICAL"] = 0] = "P0_CRITICAL";
    MemoryPriority[MemoryPriority["P1_CONTEXT"] = 1] = "P1_CONTEXT";
    MemoryPriority[MemoryPriority["P2_SUMMARY"] = 2] = "P2_SUMMARY";
    MemoryPriority[MemoryPriority["P3_TEMPORARY"] = 3] = "P3_TEMPORARY";
})(MemoryPriority || (MemoryPriority = {}));
// Retention periods in milliseconds
export const RETENTION_PERIODS = {
    [MemoryPriority.P0_CRITICAL]: null, // Permanent
    [MemoryPriority.P1_CONTEXT]: 30 * 24 * 60 * 60 * 1000, // 30 days
    [MemoryPriority.P2_SUMMARY]: 7 * 24 * 60 * 60 * 1000, // 7 days
    [MemoryPriority.P3_TEMPORARY]: null, // Session only
};
//# sourceMappingURL=memory-types.js.map