/**
 * Agent and server configuration — reads from dashboard.config.json via configLoader.
 *
 * Exports the same AgentConfig interface and constants as before,
 * but everything is now derived from the user's config file.
 * Falls back to sensible defaults when no config exists (first-run).
 */

import { loadConfig, type DashboardConfig, type AgentConfig as ConfigAgent } from './configLoader.js';

// ── Load config (or null for first-run) ────────────────────

let _config: DashboardConfig | null = null;
try {
  _config = loadConfig();
} catch (err) {
  console.error((err as Error).message);
  process.exit(1);
}

/** The loaded config. Null means first-run (setup wizard should take over). */
export const dashboardConfig = _config;

// ── Agent Config (backward-compatible interface) ───────────

export interface AgentConfig {
  /** OpenClaw agent directory name (e.g. 'main', 'larry') */
  agentDir: string;
  /** Display name shown above character */
  displayName: string;
  /** Character palette index (0-5, maps to the 6 sprite skins) */
  palette: number;
  /** Emoji for the agent */
  emoji: string;
  /** Whether this agent is always present (vs spawned on demand) */
  alwaysPresent: boolean;
  /** Hue shift in degrees (0 = no shift) */
  hueShift: number;
}

function configAgentToAgentConfig(a: ConfigAgent): AgentConfig {
  return {
    agentDir: a.id,
    displayName: a.name,
    palette: a.palette,
    emoji: a.emoji,
    alwaysPresent: a.alwaysPresent,
    hueShift: a.hueShift ?? 0,
  };
}

// ── Exports ────────────────────────────────────────────────

/** Agent list — from config, or empty for first-run */
export const AGENTS: AgentConfig[] = _config
  ? _config.agents.map(configAgentToAgentConfig)
  : [];

/** Base path for OpenClaw agent sessions */
export const OPENCLAW_AGENTS_DIR: string = _config?.openclaw.agentsDir ?? '';

/** Port for the dashboard server — env var override for first-run/wizard */
export const SERVER_PORT: number = process.env.PIXEL_AGENTS_PORT
  ? parseInt(process.env.PIXEL_AGENTS_PORT, 10)
  : (_config?.server.port ?? 5070);

/** Spawnable agent IDs */
export const SPAWNABLE_AGENTS: string[] = _config?.spawnable ?? [];

/** Gateway URL */
export const GATEWAY_URL: string = _config?.gateway.url ?? 'http://localhost:18789';

/** Gateway auth token */
export const GATEWAY_TOKEN: string = _config?.gateway.token ?? '';

/** Feature flags */
export const FEATURES = _config?.features ?? {
  fireAlarm: true,
  breakerPanel: true,
  hamRadio: true,
  serverRack: true,
  nickDesk: false,
  dayNightCycle: true,
  conversationHeat: true,
  channelBadges: true,
  sounds: true,
  door: true,
};

/** Remote agent configs */
export const REMOTE_AGENTS = _config?.remoteAgents ?? [];

// ── Timing constants (not user-configurable, just sensible defaults) ──

/** How long (ms) without JSONL activity before an agent is considered idle */
export const IDLE_TIMEOUT_MS = 30_000;

/** How long (ms) a tool call can run before being considered stalled */
export const STALLED_TOOL_TIMEOUT_MS = 5 * 60_000;

/** How long (ms) an always-present agent can go without any JSONL activity before being considered stalled */
export const STALLED_AGENT_TIMEOUT_MS = 10 * 60_000;

/** How long (ms) before a non-always-present agent is despawned after going idle */
export const AGENT_DESPAWN_TIMEOUT_MS = 3 * 60_000;

/** How often (ms) to scan for new/changed session files */
export const SESSION_SCAN_INTERVAL_MS = 3_000;
