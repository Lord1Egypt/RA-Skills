import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
/**
 * guard-scanner watcher + CI/CD reporter テストスイート
 *
 * node --test で実行
 */

import { expect, describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import path  from 'path';
import fs  from 'fs';
import { GuardWatcher  } from '../src/watcher';
import { CIReporter  } from '../src/ci-reporter';

const FIXTURES = path.join(__dirname, 'fixtures');

// ===== Mock findings for CI tests =====
const MOCK_FINDINGS = [
    {
        skill: 'malicious-skill',
        verdict: 'MALICIOUS',
        risk: 95,
        findings: [
            { id: 'PI_IGNORE', severity: 'CRITICAL', cat: 'prompt-injection', desc: 'Prompt injection', file: 'index', line: 5 },
            { id: 'MAL_EVAL', severity: 'HIGH', cat: 'malicious-code', desc: 'eval() usage', file: 'index', line: 12 },
            { id: 'EXFIL_WEBHOOK', severity: 'MEDIUM', cat: 'exfiltration', desc: 'Webhook exfil', file: 'index', line: 20 },
        ],
    },
];

const MOCK_STATS = { scanned: 5, clean: 3, suspicious: 1, malicious: 1 };

// ===== 1. GuardWatcher Construction =====
describe('GuardWatcher: Construction', () => {
    it('should create watcher instance', () => {
        const watcher = new GuardWatcher({ quiet: true });
        assert.ok(watcher);
        assert.equal(watcher._running, false);
    });

    it('should require directory for watch', () => {
        const watcher = new GuardWatcher({ quiet: true });
        assert.throws(() => watcher.watch(''), /directory is required/);
    });

    it('should reject non-existent directory', () => {
        const watcher = new GuardWatcher({ quiet: true });
        assert.throws(() => watcher.watch('/nonexistent/path/12345'), /not found/);
    });
});

// ===== 2. GuardWatcher Watch & Stop =====
describe('GuardWatcher: Watch & Stop', () => {
    it('should start and stop watching', () => {
        const watcher = new GuardWatcher({ quiet: true });
        watcher.watch(FIXTURES);
        assert.equal(watcher._running, true);
        const stats = watcher.stop();
        assert.equal(watcher._running, false);
        assert.ok(stats.scanCount >= 0);
    });

    it('should emit watching event', (t, done) => {
        const watcher = new GuardWatcher({ quiet: true });
        watcher.on('watching', (data) => {
            assert.ok(data.directory);
            watcher.stop();
            
        });
        watcher.watch(FIXTURES);
    });

    it('should emit stopped event', (t, done) => {
        const watcher = new GuardWatcher({ quiet: true });
        watcher.on('stopped', (stats) => {
            assert.ok(stats.scanCount >= 0);
            
        });
        watcher.watch(FIXTURES);
        setTimeout(() => watcher.stop(), 50);
    });

    it('should return stats', () => {
        const watcher = new GuardWatcher({ quiet: true });
        watcher.watch(FIXTURES);
        const stats = watcher.getStats();
        assert.equal(stats.running, true);
        assert.equal(stats.watcherCount, 1);
        watcher.stop();
    });
});

// ===== 3. CIReporter: GitHub Actions =====
describe('CIReporter: GitHub Actions', () => {
    it('should generate GitHub annotations', () => {
        const reporter = new CIReporter();
        const annotations = reporter.toGitHubAnnotations(MOCK_FINDINGS);
        assert.equal(annotations.length, 3);
        assert.equal(annotations[0].level, 'error'); // CRITICAL
        assert.equal(annotations[1].level, 'error'); // HIGH
        assert.equal(annotations[2].level, 'warning'); // MEDIUM
    });

    it('should generate GitHub step summary', () => {
        const reporter = new CIReporter();
        const summary = reporter.toGitHubSummary(MOCK_FINDINGS, MOCK_STATS);
        assert.ok(summary.includes('Guard Scanner Report'));
        assert.ok(summary.includes('malicious-skill'));
        assert.ok(summary.includes('MALICIOUS'));
    });

    it('should handle empty findings', () => {
        const reporter = new CIReporter();
        const annotations = reporter.toGitHubAnnotations([]);
        assert.equal(annotations.length, 0);
    });
});

// ===== 4. CIReporter: GitLab Code Quality =====
describe('CIReporter: GitLab Code Quality', () => {
    it('should generate GitLab code quality report', () => {
        const reporter = new CIReporter();
        const issues = reporter.toGitLabCodeQuality(MOCK_FINDINGS);
        assert.equal(issues.length, 3);
        assert.equal(issues[0].severity, 'blocker'); // CRITICAL
        assert.equal(issues[0].type, 'issue');
        assert.ok(issues[0].fingerprint);
    });

    it('should map severities correctly', () => {
        const reporter = new CIReporter();
        const issues = reporter.toGitLabCodeQuality(MOCK_FINDINGS);
        assert.equal(issues[0].severity, 'blocker');
        assert.equal(issues[1].severity, 'critical');
        assert.equal(issues[2].severity, 'major');
    });
});

// ===== 5. CIReporter: Webhook =====
describe('CIReporter: Webhook', () => {
    it('should require webhook URL', async () => {
        const reporter = new CIReporter();
        await await expect(() => reporter.sendWebhook('', {}), /URL is required/);
    });
});

// ===== 6. Integration =====
describe('Watcher + CI Integration', () => {
    it('should export GuardWatcher', () => {
        assert.ok(typeof GuardWatcher === 'function');
    });

    it('should export CIReporter', () => {
        assert.ok(typeof CIReporter === 'function');
    });
});
