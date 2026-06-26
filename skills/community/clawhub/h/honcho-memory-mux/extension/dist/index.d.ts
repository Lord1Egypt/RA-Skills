/**
 * Memory Multiplexer Plugin for OpenClaw
 *
 * Claims the "memory" slot. Provides:
 * - All honcho_* tools (search, recall, analyze, etc.) for retrieval
 * - memory_get for reading local workspace files
 * - agent_end hook that writes conversations to Honcho
 * - Local markdown files are written by the agent itself (via AGENTS.md behavior)
 *
 * This gives us dual-write (honcho cloud + local files) with honcho-only retrieval.
 * If honcho dies, local files are the backup. If we ditch honcho, swap this plugin
 * for memory-core and everything works.
 */
declare const _default: {
    id: string;
    name: string;
    description: string;
    kind: string;
    register(api: any): void;
};
export default _default;
