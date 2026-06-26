// Health check utilities for Memory Garden MCP skill

export interface HealthStatus {
  healthy: boolean;
  daemon: {
    running: boolean;
    url: string;
    version?: string;
    patternCount?: number;
  };
  skill: {
    version: string;
    searchEnabled: boolean;
    extractionEnabled: boolean;
    syncEnabled: boolean;
  };
}

const HEALTH_TIMEOUT_MS = 3000;

export async function checkHealth(daemonUrl: string, config: {
  searchEnabled: boolean;
  extractionEnabled: boolean;
  syncEnabled: boolean;
}): Promise<HealthStatus> {
  const skillVersion = require('./package.json').version;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);

    const response = await fetch(`${daemonUrl}/health`, {
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      return {
        healthy: false,
        daemon: {
          running: false,
          url: daemonUrl,
        },
        skill: {
          version: skillVersion,
          ...config,
        },
      };
    }

    const body = await response.json() as {
      status: string;
      version: string;
      pattern_count: number;
    };

    return {
      healthy: body.status === 'ok',
      daemon: {
        running: true,
        url: daemonUrl,
        version: body.version,
        patternCount: body.pattern_count,
      },
      skill: {
        version: skillVersion,
        ...config,
      },
    };
  } catch {
    return {
      healthy: false,
      daemon: {
        running: false,
        url: daemonUrl,
      },
      skill: {
        version: skillVersion,
        ...config,
      },
    };
  }
}

// Format health status for display
export function formatHealthStatus(status: HealthStatus): string {
  const lines: string[] = [];

  lines.push(`Memory Garden MCP Health Status`);
  lines.push(`================================`);
  lines.push(``);
  lines.push(`Overall: ${status.healthy ? 'Healthy' : 'Unhealthy'}`);
  lines.push(``);
  lines.push(`Daemon:`);
  lines.push(`  Running: ${status.daemon.running ? 'Yes' : 'No'}`);
  lines.push(`  URL: ${status.daemon.url}`);
  if (status.daemon.version) {
    lines.push(`  Version: ${status.daemon.version}`);
  }
  if (status.daemon.patternCount !== undefined) {
    lines.push(`  Patterns: ${status.daemon.patternCount}`);
  }
  lines.push(``);
  lines.push(`Skill:`);
  lines.push(`  Version: ${status.skill.version}`);
  lines.push(`  Search: ${status.skill.searchEnabled ? 'Enabled' : 'Disabled'}`);
  lines.push(`  Extraction: ${status.skill.extractionEnabled ? 'Enabled' : 'Disabled'}`);
  lines.push(`  Sync: ${status.skill.syncEnabled ? 'Enabled' : 'Disabled'}`);

  return lines.join('\n');
}
