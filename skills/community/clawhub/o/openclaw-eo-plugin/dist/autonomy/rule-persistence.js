/**
 * Rule Persistence - Saves/loads mandatory rules to disk
 *
 * Part of the closed-loop evolution:
 * Track → Analyze → Generate Rules → Persist → Enforce → Verify → Repeat
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
const RULES_DIR = '.openclaw/eo-rules';
const RULES_FILE = 'mandatory-rules.json';
const EVOLUTION_LOG = 'evolution-log.json';
/**
 * Get the rules directory path
 */
function getRulesDir() {
    return join(homedir(), RULES_DIR);
}
/**
 * Ensure rules directory exists
 */
function ensureRulesDir() {
    const dir = getRulesDir();
    if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
    }
    return dir;
}
/**
 * Save mandatory rules to disk
 */
export function saveMandatoryRules(rules) {
    const dir = ensureRulesDir();
    const path = join(dir, RULES_FILE);
    const data = {
        version: '1.0',
        timestamp: Date.now(),
        rules: rules,
        ruleCount: rules.length,
    };
    writeFileSync(path, JSON.stringify(data, null, 2), 'utf-8');
    return path;
}
/**
 * Load mandatory rules from disk
 */
export function loadMandatoryRules() {
    const path = join(getRulesDir(), RULES_FILE);
    if (!existsSync(path)) {
        return null;
    }
    try {
        const content = readFileSync(path, 'utf-8');
        const data = JSON.parse(content);
        return data.rules || [];
    }
    catch (e) {
        console.error('[RulePersistence] Failed to load rules:', e.message);
        return null;
    }
}
/**
 * Append to evolution log
 */
export function appendEvolutionLog(entry) {
    const dir = ensureRulesDir();
    const path = join(dir, EVOLUTION_LOG);
    let log = [];
    if (existsSync(path)) {
        try {
            log = JSON.parse(readFileSync(path, 'utf-8'));
        }
        catch (e) {
            log = [];
        }
    }
    log.push({
        ...entry,
        timestamp: Date.now(),
        date: new Date().toISOString(),
    });
    // Keep last 100 entries
    if (log.length > 100) {
        log = log.slice(-100);
    }
    writeFileSync(path, JSON.stringify(log, null, 2), 'utf-8');
    return log.length;
}
/**
 * Get evolution log
 */
export function getEvolutionLog(limit = 20) {
    const path = join(getRulesDir(), EVOLUTION_LOG);
    if (!existsSync(path)) {
        return [];
    }
    try {
        const content = readFileSync(path, 'utf-8');
        const log = JSON.parse(content);
        return log.slice(-limit);
    }
    catch (e) {
        return [];
    }
}
/**
 * Clear all rules (for testing)
 */
export function clearAllRules() {
    const dir = getRulesDir();
    const rulesPath = join(dir, RULES_FILE);
    if (existsSync(rulesPath)) {
        const rules = loadMandatoryRules();
        // Backup before clearing
        appendEvolutionLog({ action: 'rules_cleared', rules });
        writeFileSync(rulesPath, JSON.stringify({ version: '1.0', timestamp: Date.now(), rules: [], ruleCount: 0 }, null, 2), 'utf-8');
    }
}
/**
 * Get rules directory path (for external use)
 */
export function getRulesPath() {
    return join(getRulesDir(), RULES_FILE);
}
//# sourceMappingURL=rule-persistence.js.map