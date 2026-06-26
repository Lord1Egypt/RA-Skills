"use strict";
// Health check utilities for Memory Garden MCP skill
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkHealth = checkHealth;
exports.formatHealthStatus = formatHealthStatus;
const HEALTH_TIMEOUT_MS = 3000;
async function checkHealth(daemonUrl, config) {
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
        const body = await response.json();
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
    }
    catch {
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
function formatHealthStatus(status) {
    const lines = [];
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
//# sourceMappingURL=health.js.map