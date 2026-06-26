/**
 * Config Loader — reads dashboard.config.json and provides typed config.
 *
 * Features:
 * - ${ENV_VAR} expansion in string values (secrets stay in env, not config)
 * - ~ expansion to home directory
 * - Validation of required fields
 * - Sensible defaults for optional fields
 * - Returns null if no config file exists (signals first-run / setup wizard)
 */

import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';

// ── Types ──────────────────────────────────────────────────

export interface AgentConfig {
  id: string;
  name: string;
  emoji: string;
  palette: number;
  alwaysPresent: boolean;
  hueShift?: number;
}

export interface RemoteAgentConfig {
  id: string;
  host: string;
  user: string;
  password?: string;
  keyPath?: string;
  agentsDir: string;
}

export interface FeaturesConfig {
  fireAlarm: boolean;
  breakerPanel: boolean;
  hamRadio: boolean;
  serverRack: boolean;
  nickDesk: boolean;
  dayNightCycle: boolean;
  conversationHeat: boolean;
  channelBadges: boolean;
  sounds: boolean;
  door: boolean;
}

export interface DashboardConfig {
  server: {
    port: number;
  };
  gateway: {
    url: string;
    token: string;
  };
  openclaw: {
    agentsDir: string;
  };
  agents: AgentConfig[];
  spawnable: string[];
  remoteAgents: RemoteAgentConfig[];
  features: FeaturesConfig;
}

// ── Defaults ───────────────────────────────────────────────

const DEFAULT_FEATURES: FeaturesConfig = {
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

const DEFAULT_PORT = 5070;
const DEFAULT_GATEWAY_URL = 'http://localhost:18789';

// ── Env Var Expansion ──────────────────────────────────────

/**
 * Expand ${ENV_VAR} references in a string value.
 * Returns the original string with all ${...} replaced by their env values.
 * Missing env vars expand to empty string and are logged as warnings.
 */
function expandEnvVars(value: string): string {
  return value.replace(/\$\{([^}]+)\}/g, (_match, varName: string) => {
    const envVal = process.env[varName];
    if (envVal === undefined) {
      console.warn(`[Config] Warning: environment variable ${varName} is not set`);
      return '';
    }
    return envVal;
  });
}

/**
 * Expand ~ to the user's home directory in path strings.
 */
function expandTilde(value: string): string {
  if (value.startsWith('~/') || value === '~') {
    return path.join(os.homedir(), value.slice(1));
  }
  return value;
}

/**
 * Recursively process all string values in an object:
 * expand ${ENV_VAR} and ~ references.
 */
function expandStrings<T>(obj: T): T {
  if (typeof obj === 'string') {
    return expandTilde(expandEnvVars(obj)) as unknown as T;
  }
  if (Array.isArray(obj)) {
    return obj.map(item => expandStrings(item)) as unknown as T;
  }
  if (obj !== null && typeof obj === 'object') {
    const result: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      result[key] = expandStrings(value);
    }
    return result as T;
  }
  return obj;
}

// ── Validation ─────────────────────────────────────────────

interface ValidationError {
  field: string;
  message: string;
}

function validate(raw: Record<string, unknown>): ValidationError[] {
  const errors: ValidationError[] = [];

  // Agents array required and non-empty
  if (!Array.isArray(raw.agents) || raw.agents.length === 0) {
    errors.push({ field: 'agents', message: 'At least one agent must be defined' });
  } else {
    for (let i = 0; i < raw.agents.length; i++) {
      const a = raw.agents[i] as Record<string, unknown>;
      if (!a.id || typeof a.id !== 'string') {
        errors.push({ field: `agents[${i}].id`, message: 'Agent id is required (string)' });
      }
      if (!a.name || typeof a.name !== 'string') {
        errors.push({ field: `agents[${i}].name`, message: 'Agent name is required (string)' });
      }
      if (typeof a.palette !== 'number' || a.palette < 0 || a.palette > 5) {
        errors.push({ field: `agents[${i}].palette`, message: 'Palette must be a number 0-5' });
      }
    }
  }

  // Gateway URL should be present
  const gw = raw.gateway as Record<string, unknown> | undefined;
  if (!gw?.url || typeof gw.url !== 'string') {
    errors.push({ field: 'gateway.url', message: 'Gateway URL is required' });
  }

  return errors;
}

// ── Loader ─────────────────────────────────────────────────

/** Default config file name */
export const CONFIG_FILENAME = 'dashboard.config.json';

/**
 * Resolve config file path. Checks:
 * 1. Explicit path from env PIXEL_AGENTS_CONFIG
 * 2. ./dashboard.config.json (cwd)
 * 3. ~/.config/pixel-agents/dashboard.config.json
 */
function resolveConfigPath(): string | null {
  const envPath = process.env.PIXEL_AGENTS_CONFIG;
  if (envPath) {
    const resolved = path.resolve(expandTilde(envPath));
    if (fs.existsSync(resolved)) return resolved;
    console.warn(`[Config] PIXEL_AGENTS_CONFIG points to ${resolved} but file not found`);
    return null;
  }

  // Check CWD
  const cwdPath = path.resolve(CONFIG_FILENAME);
  if (fs.existsSync(cwdPath)) return cwdPath;

  // Check ~/.config/pixel-agents/
  const xdgPath = path.join(os.homedir(), '.config', 'pixel-agents', CONFIG_FILENAME);
  if (fs.existsSync(xdgPath)) return xdgPath;

  return null;
}

/**
 * Load and parse the dashboard config.
 * Returns the typed config object, or null if no config file exists (first-run).
 * Throws on invalid config (file exists but is malformed).
 */
export function loadConfig(): DashboardConfig | null {
  const configPath = resolveConfigPath();
  if (!configPath) {
    console.log('[Config] No config file found — first-run mode');
    return null;
  }

  console.log(`[Config] Loading from ${configPath}`);

  let raw: Record<string, unknown>;
  try {
    const text = fs.readFileSync(configPath, 'utf-8');
    // Strip JS-style comments (// and /* */) for convenience
    // Be careful not to strip // inside strings (e.g., URLs)
    const stripped = text
      .replace(/("(?:[^"\\]|\\.)*")|\/\/.*$/gm, (match, str) => str || '')
      .replace(/\/\*[\s\S]*?\*\//g, '');
    raw = JSON.parse(stripped);
  } catch (err) {
    throw new Error(`[Config] Failed to parse ${configPath}: ${(err as Error).message}`);
  }

  // Expand env vars and ~ in all string values
  const expanded = expandStrings(raw);

  // Validate
  const errors = validate(expanded);
  if (errors.length > 0) {
    const msgs = errors.map(e => `  ${e.field}: ${e.message}`).join('\n');
    throw new Error(`[Config] Validation errors in ${configPath}:\n${msgs}`);
  }

  // Build typed config with defaults
  const server = (expanded.server || {}) as Record<string, unknown>;
  const gateway = (expanded.gateway || {}) as Record<string, unknown>;
  const openclaw = (expanded.openclaw || {}) as Record<string, unknown>;
  const features = (expanded.features || {}) as Record<string, unknown>;
  const agents = (expanded.agents || []) as Record<string, unknown>[];
  const remoteAgents = (expanded.remoteAgents || []) as Record<string, unknown>[];
  const spawnable = (expanded.spawnable || []) as string[];

  const config: DashboardConfig = {
    server: {
      port: typeof server.port === 'number' ? server.port : DEFAULT_PORT,
    },
    gateway: {
      url: (gateway.url as string) || DEFAULT_GATEWAY_URL,
      token: (gateway.token as string) || process.env.OPENCLAW_GATEWAY_TOKEN || '',
    },
    openclaw: {
      agentsDir: (openclaw.agentsDir as string) || path.join(os.homedir(), '.openclaw', 'agents'),
    },
    agents: agents.map(a => ({
      id: a.id as string,
      name: a.name as string,
      emoji: (a.emoji as string) || '🤖',
      palette: (a.palette as number) ?? 0,
      alwaysPresent: (a.alwaysPresent as boolean) ?? false,
      hueShift: (a.hueShift as number) ?? 0,
    })),
    spawnable,
    remoteAgents: remoteAgents.map(r => ({
      id: r.id as string,
      host: r.host as string,
      user: r.user as string,
      password: r.password as string | undefined,
      keyPath: r.keyPath as string | undefined,
      agentsDir: r.agentsDir as string,
    })),
    features: {
      ...DEFAULT_FEATURES,
      ...Object.fromEntries(
        Object.entries(features).filter(([, v]) => typeof v === 'boolean'),
      ),
    } as FeaturesConfig,
  };

  console.log(`[Config] Loaded: ${config.agents.length} agents, ${config.remoteAgents.length} remote, ${config.spawnable.length} spawnable`);
  return config;
}

/**
 * Get the directory where config should be written (for setup wizard).
 */
export function getConfigDir(): string {
  return process.cwd();
}
