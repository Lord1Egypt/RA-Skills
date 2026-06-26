import { describe, it, expect, vi, beforeEach } from 'vitest';
import type { OpenClawPluginApi, OpenClawToolDefinition, OpenClawProviderDefinition, OpenClawHookDefinition } from '../src/types.js';

// Mock ain-cli
vi.mock('@felipematos/ain-cli', () => ({
  loadConfig: vi.fn(() => ({
    version: 1,
    providers: {
      local: {
        kind: 'openai-compatible',
        baseUrl: 'http://localhost:1234/v1',
        models: [{ id: 'llama-3' }, { id: 'mistral-7b' }],
        timeoutMs: 60000,
      },
      openai: {
        kind: 'openai-compatible',
        baseUrl: 'https://api.openai.com/v1',
        apiKey: 'sk-test',
        models: [{ id: 'gpt-4o' }],
        timeoutMs: 60000,
      },
    },
    defaults: { provider: 'local' },
  })),
  createAdapter: vi.fn(() => ({
    chat: vi.fn(async () => ({
      id: 'test',
      object: 'chat.completion',
      created: 1,
      model: 'llama-3',
      choices: [{ index: 0, message: { role: 'assistant', content: 'Hello' }, finish_reason: 'stop' }],
      usage: { prompt_tokens: 10, completion_tokens: 5, total_tokens: 15 },
    })),
    chatStream: vi.fn(async function* () {
      yield 'Hello';
      yield ' world';
    }),
  })),
  run: vi.fn(async () => ({
    ok: true,
    provider: 'local',
    model: 'llama-3',
    output: 'test output',
    usage: { prompt_tokens: 10, completion_tokens: 5, total_tokens: 15 },
  })),
  route: vi.fn(() => ({
    provider: 'local',
    model: 'llama-3',
    tier: 'general',
    rationale: 'Heuristic routing',
  })),
  classifyTask: vi.fn(() => 'generation'),
  estimateComplexity: vi.fn(() => 'low'),
}));

function createMockApi(): OpenClawPluginApi & {
  tools: OpenClawToolDefinition[];
  providers: OpenClawProviderDefinition[];
  hooks: OpenClawHookDefinition[];
} {
  const tools: OpenClawToolDefinition[] = [];
  const providers: OpenClawProviderDefinition[] = [];
  const hooks: OpenClawHookDefinition[] = [];

  return {
    tools,
    providers,
    hooks,
    pluginConfig: {},
    logger: {
      info: vi.fn(),
      warn: vi.fn(),
      error: vi.fn(),
      debug: vi.fn(),
    },
    registerTool(tool: OpenClawToolDefinition) {
      tools.push(tool);
    },
    registerProvider(provider: OpenClawProviderDefinition) {
      providers.push(provider);
    },
    registerHook(hook: OpenClawHookDefinition) {
      hooks.push(hook);
    },
  };
}

describe('OpenClaw plugin registration', () => {
  let mockApi: ReturnType<typeof createMockApi>;

  beforeEach(() => {
    mockApi = createMockApi();
  });

  it('registers a provider for each AIN provider', async () => {
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    expect(mockApi.providers).toHaveLength(2);
    expect(mockApi.providers.map((p) => p.id)).toEqual(['ain:local', 'ain:openai']);
  });

  it('registers providers with correct model lists', async () => {
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    const local = mockApi.providers.find((p) => p.id === 'ain:local');
    expect(local?.models).toEqual(['llama-3', 'mistral-7b']);

    const openai = mockApi.providers.find((p) => p.id === 'ain:openai');
    expect(openai?.models).toEqual(['gpt-4o']);
  });

  it('registers ain_run and ain_classify tools', async () => {
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    const toolNames = mockApi.tools.map((t) => t.name);
    expect(toolNames).toContain('ain_run');
    expect(toolNames).toContain('ain_classify');
  });

  it('registers before_model_resolve hook', async () => {
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    expect(mockApi.hooks).toHaveLength(1);
    expect(mockApi.hooks[0]?.event).toBe('before_model_resolve');
  });

  it('skips tools when exposeTools=false', async () => {
    mockApi.pluginConfig = { exposeTools: false };
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    expect(mockApi.tools).toHaveLength(0);
  });

  it('skips routing hook when enableRouting=false', async () => {
    mockApi.pluginConfig = { enableRouting: false };
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    expect(mockApi.hooks).toHaveLength(0);
  });

  it('ain_run tool executes a prompt', async () => {
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    const ainRun = mockApi.tools.find((t) => t.name === 'ain_run');
    const result = await ainRun!.execute({ prompt: 'Hello world' });
    expect(result).toHaveProperty('output', 'test output');
    expect(result).toHaveProperty('provider', 'local');
  });

  it('ain_classify tool classifies a prompt', async () => {
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    const ainClassify = mockApi.tools.find((t) => t.name === 'ain_classify');
    const result = await ainClassify!.execute({ prompt: 'Write a poem' });
    expect(result).toEqual({ taskType: 'generation', complexity: 'low' });
  });

  it('routing hook returns provider and model', async () => {
    const plugin = (await import('../src/index.js')).default;
    await plugin.register(mockApi);

    const hook = mockApi.hooks[0]!;
    const result = await hook.handler({ prompt: 'Hello' });
    expect(result).toEqual({
      provider: 'ain:local',
      model: 'llama-3',
      metadata: {
        tier: 'general',
        rationale: 'Heuristic routing',
        source: 'ain-routing',
      },
    });
  });

  it('has correct plugin metadata', async () => {
    const plugin = (await import('../src/index.js')).default;
    expect(plugin.id).toBe('openclaw-plugin-ain');
    expect(plugin.name).toBe('AIN - AI Node');
    expect(plugin.version).toBe('0.2.2');
  });
});
