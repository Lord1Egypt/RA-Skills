import { createAdapter, loadConfig } from '@felipematos/ain-cli';
import type { AinConfig } from '@felipematos/ain-cli';
import type { OpenClawPluginApi, OpenClawChatRequest, OpenClawChatResponse } from './types.js';

export function registerAinProviders(api: OpenClawPluginApi, config: AinConfig): void {
  for (const [name, providerConfig] of Object.entries(config.providers)) {
    const adapter = createAdapter(providerConfig);
    const models = (providerConfig.models ?? []).map((m) => m.id);

    api.registerProvider({
      id: `ain:${name}`,
      name: `AIN/${name}`,
      models,
      async chat(request: OpenClawChatRequest): Promise<OpenClawChatResponse> {
        const response = await adapter.chat({
          model: request.model,
          messages: request.messages.map((m) => ({
            role: m.role as 'system' | 'user' | 'assistant',
            content: m.content,
          })),
          temperature: request.temperature,
          max_tokens: request.max_tokens,
          ...(request.response_format ? { response_format: request.response_format as { type: 'json_object' } } : {}),
        });

        const content = response.choices[0]?.message?.content ?? '';
        return {
          content,
          model: response.model,
          usage: response.usage,
        };
      },
      async *chatStream(request: OpenClawChatRequest): AsyncGenerator<string> {
        yield* adapter.chatStream({
          model: request.model,
          messages: request.messages.map((m) => ({
            role: m.role as 'system' | 'user' | 'assistant',
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
