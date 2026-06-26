"use strict";
/**
 * Persona-consent-telegram-hub plugin.
 *
 * When OpenClaw supports a gateway lifecycle hook (e.g. onGatewayStart), this
 * module will be invoked with the skill's env. Until then, use the wrapper:
 *
 *   node scripts/run-gateway-with-persona-client.js -- <openclaw gateway args>
 *
 * or run persona_client.sh manually in a separate terminal.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.onGatewayStart = onGatewayStart;
const node_child_process_1 = require("node:child_process");
const node_path_1 = __importDefault(require("node:path"));
const SKILL_ID = "persona-consent-telegram-hub";
/**
 * Called by OpenClaw when the gateway starts, if the runtime supports
 * skill lifecycle hooks. Receives this skill's env (from openclaw.json
 * skills.entries[SKILL_ID].env).
 * If PERSONA_SERVICE_URL and PERSONA_CLIENT_ID are set, spawns
 * scripts/persona_client.sh as a detached child.
 */
function onGatewayStart(env, skillDir) {
    const personaUrl = env.PERSONA_SERVICE_URL;
    const clientId = env.PERSONA_CLIENT_ID;
    if (!personaUrl?.trim() || !clientId?.trim()) {
        return; // skill installed but persona-service not configured
    }
    const scriptPath = node_path_1.default.join(skillDir, "scripts", "persona_client.sh");
    const childEnv = { ...process.env, ...env };
    const child = (0, node_child_process_1.spawn)("bash", [scriptPath], {
        cwd: skillDir,
        env: childEnv,
        stdio: "ignore",
        detached: true,
    });
    child.unref();
}
