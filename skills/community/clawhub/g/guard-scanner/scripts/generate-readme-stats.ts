import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
/**
 * generate-readme-stats.js
 *
 * Runs `npm test` and injects actual test counts into README.md
 * Also updates the badge. Zero tolerance for hardcoded test numbers.
 *
 * Usage:
 *   node scripts/generate-readme-stats.js          # update README
 *   node scripts/generate-readme-stats.js --check   # CI mode: fail if drift detected
 */

import { execSync }  from 'child_process';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.join(__dirname, '..');
const README_PATHS = [
    path.join(ROOT, 'README.md'),
    path.join(ROOT, 'README_ja.md'),
];
const CONTRIBUTING_PATH = path.join(ROOT, 'CONTRIBUTING.md');
const TEST_FILE_COUNT_REGEX = /\.test\.(?:ts|js)$/;

function extractVitestJson(output: string): {
    numTotalTests: number;
    numPassedTests: number;
    numFailedTests: number;
    testResults: Array<{ name: string }>;
} {
    const lines = output.trim().split('\n').reverse();
    const jsonLine = lines.find((line) => line.trim().startsWith('{') && line.includes('"numTotalTests"'));
    if (!jsonLine) {
        throw new Error(`Could not find Vitest JSON payload in output:\n${output}`);
    }
    return JSON.parse(jsonLine);
}

// Run tests and capture output
let testOutput = '';
try {
    testOutput = execSync('npx vitest run --reporter=json', { cwd: ROOT, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
} catch (err) {
    testOutput = (err.stdout || '') + '\n' + (err.stderr || '');
}

let vitestReport;
try {
    vitestReport = extractVitestJson(testOutput);
} catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
}

const tests = vitestReport.numTotalTests;
const pass = vitestReport.numPassedTests;
const fail = vitestReport.numFailedTests;
const suites = fs.readdirSync(path.join(ROOT, 'tests')).filter((file) => TEST_FILE_COUNT_REGEX.test(file)).length;

console.log(`📊 Parsed: tests=${tests} suites=${suites} pass=${pass} fail=${fail}`);

if (fail > 0) {
    console.error(`❌ ${fail} tests failed. Fix tests before updating README.`);
    process.exit(1);
}

const badgePatterns = [
    /tests-\d+%20passed/g,
    /テスト-\d+_passed/g,
];
const statsBlockRe = /ℹ tests\s+\d+\nℹ suites\s+\d+\nℹ pass\s+\d+\nℹ fail\s+\d+/;
const newStatsBlock = `ℹ tests    ${tests}\nℹ suites   ${suites}\nℹ pass     ${pass}\nℹ fail     ${fail}`;
const testFileSentencePatterns = [
    /\d+ test files\. Run `npm test` to reproduce\./,
    /テストファイル\d+件。`npm test` で再現可能。/,
];
const newTestFileSentences = [
    `${suites} test files. Run \`npm test\` to reproduce.`,
    `テストファイル${suites}件。\`npm test\` で再現可能。`,
];
const contributingChecklistRe = /- \[ \] Tests pass \(`npm test` — currently \d+ tests \/ \d+ suites\)/;
const newContributingChecklist = `- [ ] Tests pass (\`npm test\` — currently ${tests} tests / ${suites} suites)`;

const updatedReadmes = README_PATHS.map((readmePath, index) => {
    let readme = fs.readFileSync(readmePath, 'utf8');
    readme = readme.replace(badgePatterns[index], index === 0 ? `tests-${pass}%20passed` : `テスト-${pass}_passed`);
    readme = readme.replace(statsBlockRe, newStatsBlock);
    readme = readme.replace(testFileSentencePatterns[index], newTestFileSentences[index]);
    return { readmePath, readme };
});

const contributing = fs.readFileSync(CONTRIBUTING_PATH, 'utf8').replace(contributingChecklistRe, newContributingChecklist);

const isCheck = process.argv.includes('--check');

if (isCheck) {
    for (const { readmePath, readme } of updatedReadmes) {
        const current = fs.readFileSync(readmePath, 'utf8');
        if (current !== readme) {
            console.error(`❌ ${path.basename(readmePath)} test stats are out of sync! Run: node scripts/generate-readme-stats`);
            process.exit(1);
        }
    }
    if (fs.readFileSync(CONTRIBUTING_PATH, 'utf8') !== contributing) {
        console.error('❌ CONTRIBUTING.md test stats are out of sync! Run: node scripts/generate-readme-stats');
        process.exit(1);
    }
    console.log('✅ README/README_ja/CONTRIBUTING test stats are in sync.');
} else {
    for (const { readmePath, readme } of updatedReadmes) {
        fs.writeFileSync(readmePath, readme);
    }
    fs.writeFileSync(CONTRIBUTING_PATH, contributing);
    console.log(`✅ Docs updated: ${pass} tests / ${suites} suites / ${fail} fail`);
}
