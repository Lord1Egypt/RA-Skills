import { PersonaClient } from '../lib/persona-client.js';
import { GetCallerTool, LogCallTool, UpdateDocsTool } from './PersonaTools.js';

// ── Tool interface (matches OpenClaw's expected shape) ──────

export interface PersonaTool {
  readonly name: string;
  readonly label: string;
  readonly description: string;
  readonly parameters: unknown;
  execute(
    toolCallId: string,
    params: Record<string, unknown>,
  ): Promise<{
    content: Array<{ type: 'text'; text: string }>;
    details: unknown;
  }>;
}

// ── Tool services ───────────────────────────────────────────

export interface ToolServices {
  readonly client: PersonaClient;
  readonly logger: { info(msg: string): void };
}

// ── Factory ─────────────────────────────────────────────────

export function createTools(services: ToolServices): PersonaTool[] {
  return [
    new GetCallerTool(services),
    new LogCallTool(services),
    new UpdateDocsTool(services),
  ];
}

export function registerTools(
  api: { registerTool: (tool: PersonaTool) => void },
  services: ToolServices,
): void {
  const tools = createTools(services);

  for (const tool of tools) {
    api.registerTool(tool);
  }

  services.logger.info(`[persona] Registered ${tools.length} persona tools`);
}
