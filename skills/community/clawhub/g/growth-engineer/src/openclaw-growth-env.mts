import { promises as fs } from 'node:fs';
import path from 'node:path';
import process from 'node:process';

type SecretRef = {
  source?: string;
  provider?: string;
  id?: string;
};

function resolveOpenClawGrowthSecretsFile() {
  const explicit = process.env.OPENCLAW_GROWTH_SECRETS_FILE?.trim();
  if (explicit) return path.resolve(explicit);
  if (process.env.HOME) return path.join(process.env.HOME, '.config', 'openclaw-growth', 'secrets.env');
  return path.resolve('.openclaw-growth-secrets.env');
}

function decodeEnvValue(rawValue) {
  const value = String(rawValue || '').trim();
  if (value.startsWith('"') && value.endsWith('"')) {
    return value
      .slice(1, -1)
      .replace(/\\(["\\$`])/g, '$1')
      .replace(/\\n/g, '\n')
      .replace(/\\r/g, '\r')
      .replace(/\\t/g, '\t');
  }
  if (value.startsWith("'") && value.endsWith("'")) {
    return value.slice(1, -1);
  }
  return value;
}

function normalizeSecretRef(value): SecretRef | null {
  if (!value || typeof value !== 'object') return null;
  const ref = value as SecretRef;
  const source = String(ref.source || '').trim();
  const id = String(ref.id || '').trim();
  if (!source || !id) return null;
  return {
    source,
    provider: String(ref.provider || 'default').trim() || 'default',
    id,
  };
}

function getConfiguredSecretRefs(config): Array<{ envName: string; ref: SecretRef }> {
  const secrets = config?.secrets && typeof config.secrets === 'object' ? config.secrets : {};
  const pairs = [
    ['githubTokenEnv', 'githubTokenRef', 'GITHUB_TOKEN'],
    ['analyticsTokenEnv', 'analyticsTokenRef', 'ANALYTICSCLI_ACCESS_TOKEN'],
    ['revenuecatTokenEnv', 'revenuecatTokenRef', 'REVENUECAT_API_KEY'],
    ['paddleTokenEnv', 'paddleTokenRef', 'PADDLE_API_KEY'],
    ['gscTokenEnv', 'gscTokenRef', 'GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN'],
    ['dataforseoLoginEnv', 'dataforseoLoginRef', 'DATAFORSEO_LOGIN'],
    ['dataforseoPasswordEnv', 'dataforseoPasswordRef', 'DATAFORSEO_PASSWORD'],
    ['sentryTokenEnv', 'sentryTokenRef', 'SENTRY_AUTH_TOKEN'],
    ['coolifyTokenEnv', 'coolifyTokenRef', 'COOLIFY_API_TOKEN'],
  ];

  return pairs
    .map(([envKey, refKey, fallbackEnv]) => {
      const envName = String(secrets?.[envKey] || fallbackEnv).trim();
      const ref = normalizeSecretRef(secrets?.[refKey]);
      return envName && ref ? { envName, ref } : null;
    })
    .filter(Boolean) as Array<{ envName: string; ref: SecretRef }>;
}

async function resolveSecretRef(ref: SecretRef): Promise<string> {
  const source = String(ref.source || '').trim();
  const id = String(ref.id || '').trim();
  if (!id) return '';
  if (source === 'env') {
    return process.env[id] || '';
  }
  if (source === 'file') {
    return (await fs.readFile(path.resolve(id), 'utf8')).trim();
  }
  return '';
}

export async function applyOpenClawSecretRefs(config) {
  const applied: string[] = [];
  const skipped: string[] = [];
  for (const { envName, ref } of getConfiguredSecretRefs(config)) {
    if (process.env[envName]) {
      skipped.push(envName);
      continue;
    }
    try {
      const value = await resolveSecretRef(ref);
      if (value) {
        process.env[envName] = value;
        applied.push(envName);
      } else {
        skipped.push(envName);
      }
    } catch {
      skipped.push(envName);
    }
  }
  return { applied, skipped };
}

export async function loadOpenClawGrowthSecrets() {
  const filePath = resolveOpenClawGrowthSecretsFile();
  let raw = '';
  try {
    raw = await fs.readFile(filePath, 'utf8');
  } catch {
    return {
      loaded: false,
      filePath,
      keys: [],
    };
  }

  const keys = [];
  for (const line of raw.split(/\r?\n/)) {
    const match = line.match(/^\s*(?:export\s+)?([A-Z0-9_]+)=(.*)\s*$/);
    if (!match) continue;

    const key = match[1];
    const value = decodeEnvValue(match[2]);
    if (!process.env[key] && value) {
      process.env[key] = value;
    }
    keys.push(key);
  }

  return {
    loaded: true,
    filePath,
    keys,
  };
}
