// @ts-nocheck
/**
 * guard-scanner Context Engine Hooks — OpenClaw Lifecycle Integration
 *
 * 3 lifecycle hooks for the Guard Scanner plugin:
 *   1. bootstrap — Initialize guard state, inject status summary
 *   2. afterTurn — Clear temporal context, flush audit log
 *   3. prepareSubagentSpawn — Guard-scan subagent payloads
 *
 * Design:
 *   - Duck-typed interfaces (no OpenClaw dependency)
 *   - Pure regex pattern matching for Moltbook/A2A detection (no external process)
 *   - Context-Crush 185KB hard limit on all injections
 *   - All hooks are non-blocking on failure (agent must never stall)
 *
 * @author Guava 🍈 & Dee
 * @version 15.0.0
 * @license MIT
 */

import { appendFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

// ── Constants ──

const CONTEXT_CRUSH_LIMIT = 189440; // 185KB
const BOOTSTRAP_CONTEXT_LIMIT = 2048; // 2KB max for bootstrap injection
const AUDIT_DIR = join(homedir(), ".openclaw", "guard-scanner");
const AUDIT_FILE = join(AUDIT_DIR, "audit.jsonl");

// ── Types (duck-typed — from OpenClaw src/plugins/types.ts) ──

/**
 * @typedef {Object} HookContext
 * @property {Record<string, unknown>} [config]
 * @property {string} [workspaceDir]
 * @property {string} [agentId]
 * @property {string} [sessionKey]
 */

/**
 * @typedef {Object} BootstrapEvent
 * @property {string} [workspace]
 * @property {string} [sessionId]
 */

/**
 * @typedef {Object} BootstrapResult
 * @property {string} [systemPromptSuffix]
 * @property {string} [extraContext]
 */

/**
 * @typedef {Object} AfterTurnEvent
 * @property {number} [turnNumber]
 * @property {number} [messageCount]
 */

/**
 * @typedef {Object} SubagentSpawnEvent
 * @property {string} [subagentId]
 * @property {string} [task]
 * @property {string[]} [tools]
 * @property {Record<string, unknown>} [params]
 */

/**
 * @typedef {Object} SubagentSpawnResult
 * @property {boolean} [block]
 * @property {string} [blockReason]
 * @property {Record<string, unknown>} [params]
 */

// ── Internal: Audit logging ──

function ensureAuditDir() {
    try {
        mkdirSync(AUDIT_DIR, { recursive: true });
    } catch {
        /* ignore — non-critical */
    }
}

function logAudit(entry) {
    ensureAuditDir();
    try {
        const line = JSON.stringify({ ...entry, ts: new Date().toISOString() }) + "\n";
        appendFileSync(AUDIT_FILE, line);
    } catch {
        /* ignore — audit failure must never block agent */
    }
}

// ── Internal: Config resolution ──

function resolveMode(ctx) {
    const mode = ctx?.config?.mode;
    if (mode === "monitor" || mode === "enforce" || mode === "strict") return mode;
    return "enforce";
}

function shouldBlock(mode, severity) {
    if (!severity || mode === "monitor") return false;
    if (mode === "strict") return severity === "CRITICAL" || severity === "HIGH";
    return severity === "CRITICAL";
}


// ── Runtime threat patterns (subset for subagent validation) ──

const SUBAGENT_CHECKS = [
    {
        id: "SA_PROMPT_INJECT", severity: "CRITICAL",
        desc: "Prompt injection in subagent task",
        test: (s) => /(ignore\s+(previous|all|above)\s+(instructions|rules)|you\s+are\s+now\s+[a-z]+|system\s*:\s*override)/i.test(s),
    },
    {
        id: "SA_CRED_EXFIL", severity: "CRITICAL",
        desc: "Credential exfiltration in subagent payload",
        test: (s) =>
            /(webhook\.site|requestbin\.com|hookbin\.com|pipedream\.net|ngrok\.io|socifiapp\.com)/i.test(s) &&
            /(token|key|secret|password|credential|env)/i.test(s),
    },
    {
        id: "SA_TRUST_BYPASS", severity: "CRITICAL",
        desc: "A2A trust bypass — partnership exploitation to override safety",
        test: (s) =>
            /(as\s+your\s+(partner|equal)|trust\s+means|between\s+us|don'?t\s+tell\s+(the\s+)?human)/i.test(s) &&
            /(ignore|bypass|skip|override|disable)\s+(guard|safety|rule|check)/i.test(s),
    },
    {
        id: "SA_REVSHELL", severity: "CRITICAL",
        desc: "Reverse shell in subagent parameters",
        test: (s) => /\/dev\/tcp\/|nc\s+-e|ncat\s+-e|bash\s+-i\s+>&|socat\s+TCP/i.test(s),
    },
    {
        id: "SA_CURL_BASH", severity: "CRITICAL",
        desc: "Download piped to shell in subagent",
        test: (s) => /(curl|wget)\s+[^\n]*\|\s*(sh|bash|zsh)/i.test(s),
    },
    {
        id: "SA_SSH_READ", severity: "HIGH",
        desc: "SSH key access in subagent",
        test: (s) => /\.ssh\/id_|\.ssh\/authorized_keys/i.test(s),
    },
    {
        id: "SA_SOUL_TAMPER", severity: "CRITICAL",
        desc: "SOUL.md modification in subagent",
        test: (s) => /SOUL\.md/i.test(s) && /(write|edit|replace|rm|delete|>)/i.test(s),
    },
    {
        id: "SA_MOLTBOOK", severity: "CRITICAL",
        desc: "Moltbook/AMOS indicator in subagent",
        test: (s) => /socifiapp|Atomic\s*Stealer|AMOS/i.test(s),
    },
    {
        id: "SA_CLOUD_META", severity: "CRITICAL",
        desc: "Cloud metadata access in subagent",
        test: (s) => /169\.254\.169\.254|metadata\.google|metadata\.aws/i.test(s),
    },
];

// ── Exported Hooks ──

/**
 * HOOK: bootstrap (priority: 10)
 *
 * Initialize guard-scanner context engine state on agent boot.
 * Injects a compact status summary into systemPromptSuffix.
 * Hard-capped at 2KB to prevent context bloat.
 *
 * @param {BootstrapEvent} event
 * @param {HookContext} ctx
 * @returns {Promise<BootstrapResult | undefined>}
 */
export async function bootstrap(event, ctx) {
    try {
        const mode = resolveMode(ctx);
        const patternCount = SUBAGENT_CHECKS.length;

        const status = [
            `🛡️ guard-scanner v15.0.0 active (mode: ${mode})`,
            `Patterns: ${patternCount} subagent + 22 runtime checks`,
            `Context-Crush limit: ${Math.round(CONTEXT_CRUSH_LIMIT / 1024)}KB`,
            `Audit: ${AUDIT_FILE}`,
        ].join(" | ");

        // Hard cap at 2KB
        const clipped = status.length > BOOTSTRAP_CONTEXT_LIMIT
            ? status.slice(0, BOOTSTRAP_CONTEXT_LIMIT - 3) + "..."
            : status;

        logAudit({
            hook: "bootstrap",
            mode,
            sessionId: event?.sessionId ?? "unknown",
            status: "initialized",
        });

        return {
            systemPromptSuffix: clipped,
        };
    } catch {
        // Bootstrap failure must never block agent startup
        return undefined;
    }
}

/**
 * HOOK: afterTurn (priority: 100)
 *
 * Post-turn cleanup:
 *   - Flush accumulated audit entries
 *   - Clear any temporal guard state
 *   - Log turn completion for forensics
 *
 * Fire-and-forget — never blocks, never throws.
 *
 * @param {AfterTurnEvent} event
 * @param {HookContext} ctx
 * @returns {Promise<void>}
 */
export async function afterTurn(event, ctx) {
    try {
        logAudit({
            hook: "afterTurn",
            turnNumber: event?.turnNumber ?? 0,
            messageCount: event?.messageCount ?? 0,
            agent: ctx?.agentId ?? "unknown",
            session: ctx?.sessionKey ?? "unknown",
            status: "turn_complete",
        });
    } catch {
        // afterTurn failure must never affect agent
    }
}

/**
 * HOOK: prepareSubagentSpawn (priority: 100)
 *
 * Critical security gate before subagent creation.
 * Validates the entire spawn payload against:
 *   1. Context-Crush limit (185KB)
 *   2. 9 subagent-specific threat patterns (Moltbook, A2A hijack, etc.)
 *
 * Returns { block: true, blockReason } on threat detection.
 *
 * @param {SubagentSpawnEvent} event
 * @param {HookContext} ctx
 * @returns {Promise<SubagentSpawnResult | undefined>}
 */
export async function prepareSubagentSpawn(event, ctx) {
    try {
        const mode = resolveMode(ctx);
        const serialized = JSON.stringify(event ?? {});

        // ── Context-Crush Check ──
        const payloadBytes = Buffer.byteLength(serialized, "utf8");
        if (payloadBytes > CONTEXT_CRUSH_LIMIT) {
            const reason = `🛡️ guard-scanner: Context-Crush — subagent payload ${payloadBytes} bytes exceeds ${Math.round(CONTEXT_CRUSH_LIMIT / 1024)}KB limit`;
            logAudit({
                hook: "prepareSubagentSpawn",
                check: "CONTEXT_CRUSH",
                severity: "CRITICAL",
                subagentId: event?.subagentId ?? "unknown",
                payloadBytes,
                action: "blocked",
            });
            return { block: true, blockReason: reason };
        }

        // ── Subagent Threat Pattern Scan ──
        for (const check of SUBAGENT_CHECKS) {
            if (!check.test(serialized)) continue;

            const auditEntry = {
                hook: "prepareSubagentSpawn",
                check: check.id,
                severity: check.severity,
                desc: check.desc,
                subagentId: event?.subagentId ?? "unknown",
                mode,
                action: "warned",
            };

            if (shouldBlock(mode, check.severity)) {
                auditEntry.action = "blocked";
                logAudit(auditEntry);
                return {
                    block: true,
                    blockReason: `🛡️ guard-scanner: ${check.desc} [${check.id}] in subagent ${event?.subagentId ?? "unknown"}`,
                };
            }

            // Below threshold — warn only
            logAudit(auditEntry);
        }

        // Clean payload — allow spawn
        return undefined;
    } catch {
        // Guard failure must never block subagent spawn
        return undefined;
    }
}
