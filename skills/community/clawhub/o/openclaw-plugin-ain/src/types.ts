/**
 * Minimal OpenClaw plugin API types.
 * Defined here to avoid a hard dependency on openclaw — it's a peer dep.
 */

export interface OpenClawToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  execute: (params: Record<string, unknown>) => Promise<unknown>;
}

export interface OpenClawProviderDefinition {
  id: string;
  name: string;
  models: string[];
  chat: (request: OpenClawChatRequest) => Promise<OpenClawChatResponse>;
  chatStream?: (request: OpenClawChatRequest) => AsyncGenerator<string>;
}

export interface OpenClawChatRequest {
  model: string;
  messages: Array<{ role: string; content: string }>;
  temperature?: number;
  max_tokens?: number;
  response_format?: unknown;
}

export interface OpenClawChatResponse {
  content: string;
  model: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface OpenClawHookDefinition {
  event: string;
  handler: (context: Record<string, unknown>) => Promise<Record<string, unknown> | void>;
}

export interface OpenClawLogger {
  info: (message: string) => void;
  warn: (message: string) => void;
  error: (message: string) => void;
  debug: (message: string) => void;
}

export interface OpenClawPluginApi {
  registerTool: (tool: OpenClawToolDefinition) => void;
  registerProvider: (provider: OpenClawProviderDefinition) => void;
  registerHook: (hook: OpenClawHookDefinition) => void;
  pluginConfig: Record<string, unknown>;
  logger: OpenClawLogger;
}

export interface OpenClawPluginDefinition {
  id: string;
  name: string;
  description: string;
  version: string;
  register: (api: OpenClawPluginApi) => Promise<void>;
}

export interface AinPluginConfig {
  configPath?: string;
  enableRouting?: boolean;
  routingPolicy?: string;
  exposeTools?: boolean;
}
