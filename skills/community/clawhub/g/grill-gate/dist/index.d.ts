/**
 * grill-gate — OpenClaw Plugin
 *
 * Runtime-level tool-call gating for research/development tasks.
 * Blocks exec and sessions_spawn calls that match configurable trigger
 * patterns unless a valid grill token exists.
 *
 * Three-layer defense (this plugin is the innermost, unforgeable layer):
 *   Layer 1: auto_dispatch.py  — agent can skip it
 *   Layer 2: hermes_exec.py    — agent can bypass with raw exec
 *   Layer 3: grill-gate plugin — runtime hook, agent cannot bypass
 *
 * Configuration (via GRILL_GATE_CONFIG env or ~/.openclaw/grill-gate.json):
 *   triggers:        string[]  — keywords that require grill (default: research/design/architecture terms)
 *   exemptions:      string[]  — keywords that skip grill check (default: "ASAP", "skip grill")
 *   blockedCommands: string[]  — exec command patterns to intercept (default: ["hermes"])
 *   tokenDir:        string    — grill token directory (default: <workspace>/.grill-tokens)
 *   tokenTtlSeconds: number    — token expiry time (default: 3600)
 *   language:        "zh"|"en" — trigger/exemption language preset (default: auto-detect)
 */
declare const _default: {
    id: string;
    name: string;
    description: string;
    configSchema: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginConfigSchema;
    register: NonNullable<import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition["register"]>;
} & Pick<import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition, "kind" | "reload" | "nodeHostCommands" | "securityAuditCollectors">;
export default _default;
