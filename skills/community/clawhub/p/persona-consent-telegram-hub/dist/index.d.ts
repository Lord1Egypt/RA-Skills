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
/**
 * Called by OpenClaw when the gateway starts, if the runtime supports
 * skill lifecycle hooks. Receives this skill's env (from openclaw.json
 * skills.entries[SKILL_ID].env).
 * If PERSONA_SERVICE_URL and PERSONA_CLIENT_ID are set, spawns
 * scripts/persona_client.sh as a detached child.
 */
export declare function onGatewayStart(env: Record<string, string>, skillDir: string): void;
