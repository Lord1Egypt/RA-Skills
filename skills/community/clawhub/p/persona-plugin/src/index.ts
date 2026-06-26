/**
 * Persona Plugin for OpenClaw
 *
 * Exposes caller persona management as agent tools:
 *   - persona_get_caller    — look up caller profile + persona at call start
 *   - persona_upsert_caller — create/update basic caller info
 *   - persona_log_call      — log call + update soul/identity/memory at call end
 *   - persona_get_history   — get call history for a caller
 *
 * Configure in OpenClaw:
 *   plugins.entries.persona.config.apiKey = "hk_live_..."
 *   plugins.entries.persona.config.server = "http://localhost:3002"
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { PersonaClient } from './lib/persona-client.js';
import { createTools, registerTools } from './tools/index.js';

interface PersonaConfig {
  readonly enabled?: boolean;
  readonly apiKey: string;
  readonly server?: string;
}

const personaPlugin = {
  id: 'persona',
  name: 'Persona',
  description: 'Caller identity, memory, and persona management via the HughKnew Persona API',

  register(api: OpenClawPluginApi) {
    const rawConfig = (api.pluginConfig ?? {}) as unknown as PersonaConfig;
    const logger = api.logger;

    if (rawConfig.enabled === false) {
      logger.info('[persona] Plugin disabled');
      return;
    }

    if (!rawConfig.apiKey) {
      logger.info('[persona] No apiKey configured — persona tools will not be available');
      return;
    }

    const server = rawConfig.server ?? 'http://localhost:3002';
    const client = new PersonaClient({ server, apiKey: rawConfig.apiKey });

    // Register all tools eagerly
    registerTools(api as any, { client, logger });

    // Register a health-check service
    api.registerService({
      id: 'persona',
      async start() {
        try {
          await client.health();
          logger.info(`[persona] Connected to Persona API at ${server}`);
        } catch (err) {
          logger.info(
            `[persona] Persona API at ${server} is not reachable — tools will fail until it's started`,
          );
        }
      },
    });

    logger.info(`[persona] Plugin registered (server: ${server})`);
  },
};

export default personaPlugin;
