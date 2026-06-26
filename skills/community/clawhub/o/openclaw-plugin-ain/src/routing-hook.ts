import { route } from '@felipematos/ain-cli';
import type { OpenClawPluginApi } from './types.js';

export function registerRoutingHook(api: OpenClawPluginApi, policyName?: string): void {
  api.registerHook({
    event: 'before_model_resolve',
    async handler(context) {
      const prompt = context.prompt as string | undefined;
      if (!prompt) return;

      try {
        const decision = await route({
          prompt,
          policyName,
        });

        return {
          provider: `ain:${decision.provider}`,
          model: decision.model,
          metadata: {
            tier: decision.tier,
            rationale: decision.rationale,
            source: 'ain-routing',
          },
        };
      } catch (err) {
        api.logger.warn(`AIN routing failed: ${err instanceof Error ? err.message : String(err)}`);
        return;
      }
    },
  });
}
