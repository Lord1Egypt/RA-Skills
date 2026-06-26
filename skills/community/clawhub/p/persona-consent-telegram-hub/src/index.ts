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

import { spawn } from "node:child_process";
import path from "node:path";

const SKILL_ID = "persona-consent-telegram-hub";

/**
 * Called by OpenClaw when the gateway starts, if the runtime supports
 * skill lifecycle hooks. Receives this skill's env (from openclaw.json
 * skills.entries[SKILL_ID].env).
 * If PERSONA_SERVICE_URL and PERSONA_CLIENT_ID are set, spawns
 * scripts/persona_client.sh as a detached child.
 */
export function onGatewayStart(env: Record<string, string>, skillDir: string): void {
  const personaUrl = env.PERSONA_SERVICE_URL;
  const clientId = env.PERSONA_CLIENT_ID;

  if (!personaUrl?.trim() || !clientId?.trim()) {
    return; // skill installed but persona-service not configured
  }

  const scriptPath = path.join(skillDir, "scripts", "persona_client.sh");

  const childEnv = { ...process.env, ...env };

  const child = spawn("bash", [scriptPath], {
    cwd: skillDir,
    env: childEnv,
    stdio: "ignore",
    detached: true,
  });

  child.unref();
}
