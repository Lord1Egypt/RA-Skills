import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck

/**
 * sync-capabilities.js
 * 
 * Enforces the Single Source of Truth for capabilities across documentation.
 * Fails if inconsistencies are found, or syncs them if --fix is passed.
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT_DIR = path.join(__dirname, '..');
const SPEC_PATH = path.join(ROOT_DIR, 'docs', 'spec', 'capabilities.json');

const spec = JSON.parse(fs.readFileSync(SPEC_PATH, 'utf8'));

const targets = [
    { file: 'README.md', updates: [
        { regex: /\d+ static patterns/g, val: `${spec.static_pattern_count} static patterns` },
        { regex: /\d+ threat categories/g, val: `${spec.threat_category_count} threat categories` },
        { regex: /\d+ runtime checks/g, val: `${spec.runtime_check_count} runtime checks` },
        { regex: /zero dependencies/gi, val: `minimal dependencies (${spec.dependencies_runtime.join(', ')})` }
    ]},
    { file: 'SKILL.md', updates: [
        { regex: /\d+ static patterns/g, val: `${spec.static_pattern_count} static patterns` },
        { regex: /\d+ threat categories/g, val: `${spec.threat_category_count} threat categories` },
        { regex: /\d+ runtime checks/g, val: `${spec.runtime_check_count} runtime checks` },
        { regex: /\d+ tests/g, val: `${spec.test_count} tests` },
        { regex: /zero dependencies/gi, val: `minimal dependencies (${spec.dependencies_runtime.join(', ')})` }
    ]},
    { file: 'openclaw.plugin.json', updates: [
        { regex: /"version":\s*"[^"]+"/g, val: `"version": "${spec.plugin_version}"` },
        { regex: /\d+ static patterns/g, val: `${spec.static_pattern_count} static patterns` },
        { regex: /\d+ categories/g, val: `${spec.threat_category_count} categories` },
        { regex: /\d+ runtime checks/g, val: `${spec.runtime_check_count} runtime checks` }
    ]}
];

const fix = process.argv.includes('--fix');
let failed = false;

for (const target of targets) {
    const filePath = path.join(ROOT_DIR, target.file);
    if (!fs.existsSync(filePath)) {
        console.warn(`File not found: ${target.file}`);
        continue;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;

    for (const update of target.updates) {
        const matches = content.match(update.regex);
        if (matches) {
            for (const match of matches) {
                if (match !== update.val) {
                    if (fix) {
                        content = content.replace(update.regex, update.val);
                        modified = true;
                    } else {
                        console.error(`Mismatch in ${target.file}: expected '${update.val}', found '${match}'`);
                        failed = true;
                    }
                }
            }
        }
    }

    if (modified && fix) {
        fs.writeFileSync(filePath, content);
        console.log(`Synced ${target.file}`);
    }
}

// Special check for package.json dependencies
const pkgPath = path.join(ROOT_DIR, 'package.json');
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
const runtimeDeps = Object.keys(pkg.dependencies || {});
const specDeps = spec.dependencies_runtime;

if (runtimeDeps.length !== specDeps.length || !runtimeDeps.every(d => specDeps.includes(d))) {
    console.error(`Mismatch in package.json dependencies: expected ${specDeps.join(', ')}, found ${runtimeDeps.join(', ')}`);
    failed = true;
}

if (failed && !fix) {
    console.error('\n💥 Capability sync failed! Run `node scripts/sync-capabilities.js --fix` to update documents.');
    process.exit(1);
} else if (failed && fix) {
    // If fixing dependencies, we'd need to run npm install, but for now we just fail on dep mismatch
    if (runtimeDeps.length !== specDeps.length) {
         console.error('Cannot auto-fix package.json dependencies. Please update package.json manually.');
         process.exit(1);
    }
} else {
    console.log('✅ Capabilities synced and verified.');
}
