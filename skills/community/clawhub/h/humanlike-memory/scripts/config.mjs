const DEFAULT_BASE_URL = 'https://plugin.human-like.me';
const ALLOWED_ENV_KEYS = Object.freeze({
  API_KEY: 'HUMAN_LIKE_MEM_API_KEY',
  BASE_URL: 'HUMAN_LIKE_MEM_BASE_URL',
  USER_ID: 'HUMAN_LIKE_MEM_USER_ID',
  AGENT_ID: 'HUMAN_LIKE_MEM_AGENT_ID',
  LIMIT_NUMBER: 'HUMAN_LIKE_MEM_LIMIT_NUMBER',
  MIN_SCORE: 'HUMAN_LIKE_MEM_MIN_SCORE',
  TIMEOUT_MS: 'HUMAN_LIKE_MEM_TIMEOUT_MS',
  SCENARIO: 'HUMAN_LIKE_MEM_SCENARIO',
  RECALL_ENABLED: 'HUMAN_LIKE_MEM_RECALL_ENABLED',
  ADD_ENABLED: 'HUMAN_LIKE_MEM_ADD_ENABLED',
  AUTO_SAVE_ENABLED: 'HUMAN_LIKE_MEM_AUTO_SAVE_ENABLED',
  SAVE_TRIGGER_TURNS: 'HUMAN_LIKE_MEM_SAVE_TRIGGER_TURNS',
  SAVE_MAX_MESSAGES: 'HUMAN_LIKE_MEM_SAVE_MAX_MESSAGES',
  USE_V2_PROTOCOL: 'HUMAN_LIKE_MEM_USE_V2_PROTOCOL',
  CAPTURE_TOOL_CALLS: 'HUMAN_LIKE_MEM_CAPTURE_TOOL_CALLS',
});
const ALLOWED_ENV_KEY_SET = new Set(Object.values(ALLOWED_ENV_KEYS));
const LOCALHOST_HOSTS = new Set(['localhost', '127.0.0.1', '::1']);

function parseBoolean(value, defaultValue) {
  if (value === undefined || value === null) return defaultValue;
  if (typeof value === 'boolean') return value;
  if (typeof value === 'string') {
    const normalized = value.trim().toLowerCase();
    if (['true', '1', 'yes', 'on'].includes(normalized)) return true;
    if (['false', '0', 'no', 'off'].includes(normalized)) return false;
  }
  return defaultValue;
}

function readSkillEnv(name) {
  if (!ALLOWED_ENV_KEY_SET.has(name)) {
    throw new Error(`Unsupported environment variable access: ${name}`);
  }
  return process.env[name];
}

function normalizeBaseUrl(rawValue) {
  const candidate = (rawValue || DEFAULT_BASE_URL).trim();
  let parsed;
  try {
    parsed = new URL(candidate);
  } catch {
    throw new Error(`Invalid HUMAN_LIKE_MEM_BASE_URL: ${candidate}`);
  }

  if (!['https:', 'http:'].includes(parsed.protocol)) {
    throw new Error('HUMAN_LIKE_MEM_BASE_URL must use http or https');
  }

  if (parsed.protocol === 'http:' && !LOCALHOST_HOSTS.has(parsed.hostname)) {
    throw new Error('HUMAN_LIKE_MEM_BASE_URL must use https unless targeting localhost');
  }

  const path = parsed.pathname === '/' ? '' : parsed.pathname.replace(/\/+$/, '');
  return `${parsed.origin}${path}`;
}

export async function buildConfig() {
  const rawLimit = parseInt(readSkillEnv(ALLOWED_ENV_KEYS.LIMIT_NUMBER) || '', 10);
  const rawMinScore = parseFloat(readSkillEnv(ALLOWED_ENV_KEYS.MIN_SCORE) || '');
  const rawTimeoutMs = parseInt(readSkillEnv(ALLOWED_ENV_KEYS.TIMEOUT_MS) || '', 10);
  const rawSaveTriggerTurns = parseInt(readSkillEnv(ALLOWED_ENV_KEYS.SAVE_TRIGGER_TURNS) || '', 10);
  const rawSaveMaxMessages = parseInt(readSkillEnv(ALLOWED_ENV_KEYS.SAVE_MAX_MESSAGES) || '', 10);

  return {
    baseUrl: normalizeBaseUrl(readSkillEnv(ALLOWED_ENV_KEYS.BASE_URL)),
    apiKey: readSkillEnv(ALLOWED_ENV_KEYS.API_KEY),
    userId: readSkillEnv(ALLOWED_ENV_KEYS.USER_ID) || 'openclaw-user',
    agentId: readSkillEnv(ALLOWED_ENV_KEYS.AGENT_ID) || 'main',
    memoryLimitNumber: Number.isFinite(rawLimit) && rawLimit > 0 ? rawLimit : 6,
    minScore: Number.isFinite(rawMinScore) ? rawMinScore : 0.0,
    timeoutMs: Number.isFinite(rawTimeoutMs) && rawTimeoutMs > 0 ? rawTimeoutMs : 30000,
    scenario: readSkillEnv(ALLOWED_ENV_KEYS.SCENARIO) || 'openclaw-plugin',
    recallEnabled: parseBoolean(readSkillEnv(ALLOWED_ENV_KEYS.RECALL_ENABLED), true),
    addEnabled: parseBoolean(readSkillEnv(ALLOWED_ENV_KEYS.ADD_ENABLED), true),
    autoSaveEnabled: parseBoolean(readSkillEnv(ALLOWED_ENV_KEYS.AUTO_SAVE_ENABLED), true),
    saveTriggerTurns: Number.isFinite(rawSaveTriggerTurns) && rawSaveTriggerTurns > 0 ? rawSaveTriggerTurns : 5,
    saveMaxMessages: Number.isFinite(rawSaveMaxMessages) && rawSaveMaxMessages > 0 ? rawSaveMaxMessages : 20,
    useV2Protocol: parseBoolean(readSkillEnv(ALLOWED_ENV_KEYS.USE_V2_PROTOCOL), true),
    captureToolCalls: parseBoolean(readSkillEnv(ALLOWED_ENV_KEYS.CAPTURE_TOOL_CALLS), true),
  };
}

export function buildMissingApiKeyError() {
  return {
    success: false,
    error: 'API Key not configured. HUMAN_LIKE_MEM_API_KEY is required.',
    nextSteps: [
      'Run: openclaw config set skills.entries.human-like-memory.enabled true --strict-json',
      'Run: openclaw config set skills.entries.human-like-memory.apiKey "mp_xxx"',
      'Optional: openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_BASE_URL "https://plugin.human-like.me"',
      'Then verify with: node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs config',
    ],
    helpUrl: 'https://plugin.human-like.me',
  };
}
