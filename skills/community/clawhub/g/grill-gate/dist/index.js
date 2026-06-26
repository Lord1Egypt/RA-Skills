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
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { existsSync, readdirSync, readFileSync, unlinkSync, mkdirSync } from "fs";
import { join } from "path";
import { homedir } from "os";
// ─── Default Presets ─────────────────────────────────────────────
const PRESETS = {
    zh: {
        triggers: [
            "研究", "开发", "设计", "架构", "方案", "规划",
            "重构", "迁移", "系统设计", "技术选型",
        ],
        exemptions: ["快点", "直接做", "赶紧", "ASAP", "skip grill"],
    },
    en: {
        triggers: [
            "research", "develop", "design", "architect", "plan",
            "refactor", "migrate", "system design", "tech selection",
        ],
        exemptions: ["ASAP", "skip grill", "just do it", "quick"],
    },
};
function loadConfig() {
    const defaults = {
        triggers: [...PRESETS.zh.triggers, ...PRESETS.en.triggers],
        exemptions: [...PRESETS.zh.exemptions, ...PRESETS.en.exemptions],
        blockedCommands: ["hermes", "hermes-agent", ".hermes/"],
        tokenDir: join(process.env.OPENCLAW_WORKSPACE || join(homedir(), ".openclaw", "workspace"), ".grill-tokens"),
        tokenTtlSeconds: 3600,
    };
    // Try loading config from env or file
    try {
        const envConfig = process.env.GRILL_GATE_CONFIG;
        if (envConfig) {
            const parsed = JSON.parse(envConfig);
            return { ...defaults, ...parsed };
        }
        const configPath = join(homedir(), ".openclaw", "grill-gate.json");
        if (existsSync(configPath)) {
            const parsed = JSON.parse(readFileSync(configPath, "utf-8"));
            return { ...defaults, ...parsed };
        }
    }
    catch (err) {
        console.warn(`[grill-gate] Config load failed, using defaults:`, err instanceof Error ? err.message : err);
    }
    return defaults;
}
// ─── Token Management ────────────────────────────────────────────
function hasValidToken(config) {
    try {
        if (!existsSync(config.tokenDir))
            return false;
        const files = readdirSync(config.tokenDir).filter((f) => f.endsWith(".token"));
        const now = Date.now() / 1000;
        for (const file of files) {
            const filePath = join(config.tokenDir, file);
            try {
                const content = readFileSync(filePath, "utf-8");
                const data = JSON.parse(content);
                if (now - (data.issued_at || 0) < config.tokenTtlSeconds) {
                    return true; // Valid token found
                }
                // Expired — clean up
                unlinkSync(filePath);
            }
            catch {
                try {
                    unlinkSync(filePath);
                }
                catch { }
            }
        }
        return false;
    }
    catch {
        return false;
    }
}
// ─── Pattern Matching ────────────────────────────────────────────
function containsTrigger(text, config) {
    if (!text)
        return false;
    const lower = text.toLowerCase();
    // Check exemptions first
    for (const exempt of config.exemptions) {
        if (lower.includes(exempt.toLowerCase()))
            return false;
    }
    // Check triggers
    for (const trigger of config.triggers) {
        if (lower.includes(trigger.toLowerCase()))
            return true;
    }
    return false;
}
function isBlockedCommand(command, config) {
    if (!command)
        return false;
    const lower = command.toLowerCase();
    return config.blockedCommands.some((kw) => lower.includes(kw.toLowerCase()));
}
// ─── Plugin Entry ────────────────────────────────────────────────
export default definePluginEntry({
    id: "grill-gate",
    name: "Grill Gate",
    description: "Runtime-level grill enforcement. Blocks exec/spawn calls for " +
        "research/development tasks unless a valid grill token exists. " +
        "Ensures agents think before they act on complex tasks.",
    register(api) {
        const config = loadConfig();
        // Ensure token directory exists
        try {
            mkdirSync(config.tokenDir, { recursive: true });
        }
        catch { }
        api.on("before_tool_call", async (event) => {
            const toolName = event.toolName;
            const params = event.params || {};
            // ─── Gate 1: exec calling blocked commands ─────────
            if (toolName === "exec") {
                const command = params.command || "";
                if (isBlockedCommand(command, config)) {
                    if (!hasValidToken(config)) {
                        console.log(`[grill-gate] 🛑 BLOCKED exec: command matches blocked pattern, no grill token`);
                        return {
                            block: true,
                            blockReason: "🛑 Grill Gate: Blocked command detected without grill token. " +
                                "You must complete a grill-with-docs session first, then issue a " +
                                "grill token via: python3 scripts/auto_dispatch.py --issue-grill-token '<task>'",
                        };
                    }
                    console.log(`[grill-gate] ✅ exec allowed (valid grill token found)`);
                }
                return;
            }
            // ─── Gate 2: sessions_spawn with trigger keywords ──
            if (toolName === "sessions_spawn") {
                const task = params.task || "";
                if (containsTrigger(task, config)) {
                    if (!hasValidToken(config)) {
                        console.log(`[grill-gate] 🛑 BLOCKED sessions_spawn: task contains grill trigger, no token`);
                        return {
                            block: true,
                            blockReason: "🛑 Grill Gate: Task contains research/development keywords but no grill token. " +
                                "Complete a grill-with-docs session first.",
                        };
                    }
                }
                return;
            }
            // ─── All other tools: pass through ─────────────────
            return;
        }, { priority: 1 } // Highest priority — runs before other hooks
        );
    },
});
