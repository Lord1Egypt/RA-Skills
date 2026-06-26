import { PersonaApiError } from '../lib/persona-client.js';

export class ToolError extends Error {
  constructor(
    public readonly tool: string,
    message: string,
    public readonly details?: Record<string, unknown>,
  ) {
    super(`[${tool}] ${message}`);
    this.name = 'ToolError';
  }

  static fromError(tool: string, err: unknown): ToolError {
    if (err instanceof ToolError) return err;

    if (err instanceof PersonaApiError) {
      const hint = ToolError.getFixHint(err.statusCode);
      const message = hint ? `${err.message}. Fix: ${hint}` : err.message;
      return new ToolError(tool, message, { statusCode: err.statusCode });
    }

    const message = err instanceof Error ? err.message : String(err);
    return new ToolError(tool, message);
  }

  private static getFixHint(statusCode: number): string | null {
    switch (statusCode) {
      case 401:
        return 'Check persona API key in plugin config. Keys start with hk_live_.';
      case 403:
        return 'API key lacks the required scope. Use a key with both read and write scopes.';
      case 404:
        return 'Caller not found. Use persona_upsert_caller to create them first, or persona_log_call which auto-creates.';
      default:
        return null;
    }
  }
}
