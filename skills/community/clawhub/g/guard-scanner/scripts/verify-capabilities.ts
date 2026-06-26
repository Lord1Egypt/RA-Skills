import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';

const specPath = path.join(__dirname, '../docs/spec/capabilities.json');
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const TEST_DIR = path.join(__dirname, '../tests');
const TEST_FILE_REGEX = /\.test\.(?:ts|js)$/;

const filesToCheck = [
    {
        path: '../README.md',
        checks: [
            { regex: /<strong>(\d+)<\/strong> detection patterns/, expected: spec.static_pattern_count, name: "Static Pattern Count" },
            { regex: /<strong>(\d+)<\/strong> threat categories/, expected: spec.threat_category_count, name: "Threat Category Count" },
            { regex: /<strong>(\d+)<\/strong> runtime checks/, expected: spec.runtime_check_count, name: "Runtime Check Count" },
            { regex: /<strong>(\d+)<\/strong> dependency/, expected: spec.dependencies_runtime, name: "Runtime Dependencies" }
        ],
        banned: [
            { regex: /first open-source/i, reason: "False 'first' claim" },
            { regex: /zero dependencies/i, reason: "False 'zero dependencies' claim (we use ws)" }
        ]
    },
    {
        path: '../README_ja.md',
        checks: [
            { regex: /<strong>(\d+)<\/strong> 検出パターン/, expected: spec.static_pattern_count, name: "Static Pattern Count" },
            { regex: /<strong>(\d+)<\/strong> 脅威カテゴリ/, expected: spec.threat_category_count, name: "Threat Category Count" },
            { regex: /<strong>(\d+)<\/strong> ランタイムチェック/, expected: spec.runtime_check_count, name: "Runtime Check Count" },
            { regex: /依存: <strong>(\d+)<\/strong>/, expected: spec.dependencies_runtime, name: "Runtime Dependencies" }
        ],
        banned: [
            { regex: /first open-source/i, reason: "False 'first' claim" },
            { regex: /zero dependencies/i, reason: "False 'zero dependencies' claim (we use ws)" }
        ]
    },
    {
        path: '../SKILL.md',
        checks: [
            { regex: /(\d+) static threat patterns/, expected: spec.static_pattern_count, name: "Static Pattern Count" },
            { regex: /(\d+) categories/, expected: spec.threat_category_count, name: "Threat Category Count" },
            { regex: /(\d+) runtime checks/, expected: spec.runtime_check_count, name: "Runtime Check Count" }
        ],
        banned: [
            { regex: /zero dependencies/i, reason: "False 'zero dependencies' claim" }
        ]
    },
    {
        path: '../openclaw.plugin.json',
        isJson: true,
        checks: [
            { path: 'version', expected: spec.package_version, name: "Plugin Version" }
        ]
    },
    {
        path: '../package.json',
        isJson: true,
        checks: [
            { path: 'version', expected: spec.package_version, name: "Package Version" }
        ]
    }
];

let errors = 0;

for (const fileDef of filesToCheck) {
    const fullPath = path.join(__dirname, fileDef.path);
    if (!fs.existsSync(fullPath)) {
        console.error(`❌ File not found: ${fileDef.path}`);
        errors++;
        continue;
    }

    const content = fs.readFileSync(fullPath, 'utf8');

    if (fileDef.isJson) {
        const data = JSON.parse(content);
        for (const check of fileDef.checks) {
            // Very simple path resolution for depth=1
            const actual = data[check.path];
            if (String(actual) !== String(check.expected)) {
                console.error(`❌ [${fileDef.path}] ${check.name} mismatch: expected ${check.expected}, got ${actual}`);
                errors++;
            } else {
                console.log(`✅ [${fileDef.path}] ${check.name} matches (${actual})`);
            }
        }
    } else {
        for (const check of fileDef.checks) {
            const match = content.match(check.regex);
            if (match) {
                const actual = parseInt(match[1], 10);
                if (actual !== check.expected) {
                    console.error(`❌ [${fileDef.path}] ${check.name} mismatch: expected ${check.expected}, got ${actual}`);
                    errors++;
                } else {
                    console.log(`✅ [${fileDef.path}] ${check.name} matches (${actual})`);
                }
            } else {
                console.error(`❌ [${fileDef.path}] ${check.name} regex not found: ${check.regex}`);
                errors++;
            }
        }
    }

    if (fileDef.banned) {
        for (const ban of fileDef.banned) {
            if (ban.regex.test(content)) {
                console.error(`❌ [${fileDef.path}] Banned phrase detected: ${ban.reason}`);
                errors++;
            }
        }
    }
}

// Verify test file count against spec
if (spec.test_file_count !== undefined) {
    const testFiles = fs.readdirSync(TEST_DIR).filter(f => TEST_FILE_REGEX.test(f));
    if (testFiles.length !== spec.test_file_count) {
        console.error(`❌ [tests/] Test file count mismatch: expected ${spec.test_file_count}, got ${testFiles.length}`);
        errors++;
    } else {
        console.log(`✅ [tests/] Test file count matches (${testFiles.length})`);
    }
}

if (errors > 0) {
    console.error(`\n🚨 Verification failed with ${errors} error(s). Please update documents to match docs/spec/capabilities.json.`);
    process.exit(1);
} else {
    console.log(`\n✅ All capability claims verified against Source of Truth.`);
    process.exit(0);
}
