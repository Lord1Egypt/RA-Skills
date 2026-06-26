import fs from 'fs';
import path from 'path';
import yaml from 'yaml';

const TAG = '[openclaw-memory-max][weighter]';

let _pinnedRules: string[] = [];
let _lastRead = 0;

function getMemoryPath(): string {
    const baseDir = process.env.OPENCLAW_HOME || path.join(process.env.HOME || '/root', '.openclaw');
    return path.join(baseDir, 'memory/MEMORY.md');
}

/**
 * Parse YAML rule blocks from MEMORY.md and return rules with weight >= 1.0.
 * Reads at most once per 15 seconds (cached).
 */
export function getPinnedRules(): string[] {
    const now = Date.now();
    if (now - _lastRead < 15000 && _pinnedRules.length >= 0) return _pinnedRules;
    _lastRead = now;

    try {
        const memoryPath = getMemoryPath();
        if (!fs.existsSync(memoryPath)) return _pinnedRules = [];

        const text = fs.readFileSync(memoryPath, 'utf8');
        const match = text.match(/<!--yaml\n([\s\S]*?)\n-->/);
        if (!match) return _pinnedRules = [];

        const parsed = yaml.parse(match[1]);
        if (!parsed?.rules || !Array.isArray(parsed.rules)) return _pinnedRules = [];

        _pinnedRules = parsed.rules
            .filter((r: any) => parseFloat(r.weight) >= 1.0)
            .map((r: any) => r.constraint || r.rule || r.preference)
            .filter(Boolean);

        return _pinnedRules;
    } catch {
        return _pinnedRules = [];
    }
}

/**
 * Build an XML block of pinned rules for context injection.
 * Returns empty string if no rules are pinned.
 */
export function buildPinnedRulesXml(): string {
    const rules = getPinnedRules();
    if (rules.length === 0) return '';

    return '\n<pinned-constraints>\n' +
        rules.map(r => `  <constraint weight="1.0">${r}</constraint>`).join('\n') +
        '\n</pinned-constraints>';
}

/**
 * Register the weighter module. No longer writes to openclaw.json —
 * pinned rules are injected via the before_agent_start hook instead.
 */
export function registerWeighter(_api: any) {
    // Pre-warm the cache on startup
    const rules = getPinnedRules();
    if (rules.length > 0) {
        console.log(`${TAG} Loaded ${rules.length} pinned rule(s) from MEMORY.md.`);
    } else {
        console.log(`${TAG} No pinned rules found (add <!--yaml ... --> block to MEMORY.md).`);
    }
}
