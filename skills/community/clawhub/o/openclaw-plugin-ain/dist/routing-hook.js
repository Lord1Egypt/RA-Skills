import { route } from '@felipematos/ain-cli';
export function registerRoutingHook(api, policyName) {
    api.registerHook({
        event: 'before_model_resolve',
        async handler(context) {
            const prompt = context.prompt;
            if (!prompt)
                return;
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
            }
            catch (err) {
                api.logger.warn(`AIN routing failed: ${err instanceof Error ? err.message : String(err)}`);
                return;
            }
        },
    });
}
//# sourceMappingURL=routing-hook.js.map