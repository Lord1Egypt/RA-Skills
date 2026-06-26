// Configuration management for Memory Garden MCP skill
// MR-1: Helper to parse int with NaN guard and bounds

export interface SkillConfig {
  daemonUrl: string;
  extraction: {
    enabled: boolean;
    confirmRequired: boolean;
  };
  sync: {
    enabled: boolean;
  };
  search: {
    enabled: boolean;
    limit: number;
  };
}

// MR-1: Helper to parse int with NaN guard and bounds
function parseIntSafe(value: string | undefined, defaultVal: number, min: number, max: number): number {
  if (!value) return defaultVal;
  const parsed = parseInt(value, 10);
  if (isNaN(parsed)) {
    console.warn(`[memory-garden] Invalid integer "${value}", using default: ${defaultVal}`);
    return defaultVal;
  }
  if (parsed < min || parsed > max) {
    console.warn(`[memory-garden] Value ${parsed} out of bounds [${min}, ${max}], clamping`);
    return Math.max(min, Math.min(parsed, max));
  }
  return parsed;
}

// Parse boolean from env with explicit handling
function parseBoolEnv(value: string | undefined, defaultVal: boolean): boolean {
  if (value === undefined) return defaultVal;
  return value.toLowerCase() === 'true' || value === '1';
}

export function loadConfig(): SkillConfig {
  return {
    daemonUrl: process.env.MG_DAEMON_URL || 'http://127.0.0.1:18790',
    extraction: {
      enabled: parseBoolEnv(process.env.MG_EXTRACTION_ENABLED, false),
      confirmRequired: parseBoolEnv(process.env.MG_EXTRACTION_CONFIRM, true),
    },
    sync: {
      enabled: parseBoolEnv(process.env.MG_SYNC_ENABLED, false),
    },
    search: {
      // Search enabled by default (core feature)
      // CR-7: Use consistent parseBoolEnv with default true
      enabled: parseBoolEnv(process.env.MG_SEARCH_ENABLED, true),
      // MR-1: NaN guard with bounds (1-100)
      limit: parseIntSafe(process.env.MG_SEARCH_LIMIT, 8, 1, 100),
    },
  };
}

// Validate config and warn about potential issues
export function validateConfig(config: SkillConfig): string[] {
  const warnings: string[] = [];

  if (config.extraction.enabled && !config.extraction.confirmRequired) {
    warnings.push('Extraction enabled without confirmation - patterns may be extracted automatically');
  }

  if (config.sync.enabled && !config.extraction.enabled) {
    warnings.push('Sync enabled but extraction disabled - you can receive but not contribute patterns');
  }

  return warnings;
}
