import { createAdapter } from '@felipematos/ain-cli';
export function registerAinProviders(api, config) {
    for (const [name, providerConfig] of Object.entries(config.providers)) {
        const adapter = createAdapter(providerConfig);
        const models = (providerConfig.models ?? []).map((m) => m.id);
        api.registerProvider({
            id: `ain:${name}`,
            name: `AIN/${name}`,
            models,
            async chat(request) {
                const response = await adapter.chat({
                    model: request.model,
                    messages: request.messages.map((m) => ({
                        role: m.role,
                        content: m.content,
                    })),
                    temperature: request.temperature,
                    max_tokens: request.max_tokens,
                    ...(request.response_format ? { response_format: request.response_format } : {}),
                });
                const content = response.choices[0]?.message?.content ?? '';
                return {
                    content,
                    model: response.model,
                    usage: response.usage,
                };
            },
            async *chatStream(request) {
                yield* adapter.chatStream({
                    model: request.model,
                    messages: request.messages.map((m) => ({
                        role: m.role,
                        content: m.content,
                    })),
                    temperature: request.temperature,
                    max_tokens: request.max_tokens,
                });
            },
        });
        api.logger.info(`Registered provider ain:${name} with ${models.length} model(s)`);
    }
}
//# sourceMappingURL=providers.js.map