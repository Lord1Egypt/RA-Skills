/**
 * Config schema for memory-agentmemo plugin.
 *
 * Configures connection to an external AgentMemo HTTP service.
 * Project: https://github.com/yxjsxy/agentMemo
 */

export type AgentMemoConfig = {
  /** Base URL of the AgentMemo HTTP service (required). */
  serverUrl: string;
  /** Optional bearer token / API key. */
  apiKey?: string;
  /** Optional user/namespace ID for scoping memories. */
  userId?: string;
  /** Enable auto-capture of important messages after conversation (default: false). */
  autoCapture?: boolean;
  /** Enable auto-recall: inject relevant memories before agent starts (default: true). */
  autoRecall?: boolean;
};

const DEFAULT_SERVER_URL = "http://localhost:8790";

function resolveEnvVars(value: string): string {
  return value.replace(/\$\{([^}]+)\}/g, (_, envVar) => {
    const envValue = process.env[envVar];
    if (!envValue) {
      throw new Error(`Environment variable ${envVar} is not set`);
    }
    return envValue;
  });
}

export const agentMemoConfigSchema = {
  parse(value: unknown): AgentMemoConfig {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new Error("memory-agentmemo: config object required");
    }
    const cfg = value as Record<string, unknown>;

    const serverUrl =
      typeof cfg.serverUrl === "string" ? resolveEnvVars(cfg.serverUrl) : DEFAULT_SERVER_URL;

    const apiKey =
      typeof cfg.apiKey === "string" && cfg.apiKey.trim()
        ? resolveEnvVars(cfg.apiKey)
        : undefined;

    const userId =
      typeof cfg.userId === "string" && cfg.userId.trim() ? cfg.userId.trim() : undefined;

    return {
      serverUrl: serverUrl.replace(/\/$/, ""),
      apiKey,
      userId,
      autoCapture: cfg.autoCapture === true,
      autoRecall: cfg.autoRecall !== false,
    };
  },

  uiHints: {
    serverUrl: {
      label: "AgentMemo Server URL",
      placeholder: "http://localhost:8790",
      help: "Base URL of your AgentMemo HTTP service (or use ${AGENTMEMO_URL})",
    },
    apiKey: {
      label: "API Key",
      sensitive: true,
      placeholder: "your-api-key",
      help: "Optional bearer token for authenticated AgentMemo instances (or use ${AGENTMEMO_API_KEY})",
    },
    userId: {
      label: "User / Namespace ID",
      placeholder: "openclaw",
      help: "Optional user or namespace ID to scope memories",
    },
    autoCapture: {
      label: "Auto-Capture",
      help: "Automatically capture important information from conversations and store to AgentMemo",
    },
    autoRecall: {
      label: "Auto-Recall",
      help: "Automatically inject relevant memories from AgentMemo into context before agent starts",
    },
  },
};
