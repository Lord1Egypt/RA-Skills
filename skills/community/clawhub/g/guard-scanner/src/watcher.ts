// @ts-nocheck
/**
 * guard-scanner v8 — Real-time File Watcher
 *
 * @security-manifest
 *   env-read: []
 *   env-write: []
 *   network: none
 *   fs-read: [watched directory]
 *   fs-write: []
 *   exec: none
 *   purpose: Real-time file system monitoring for security threats
 */

import fs  from 'fs';
import path  from 'path';
import { GuardScanner  } from './scanner';
import EventEmitter  from 'events';

class GuardWatcher extends EventEmitter {
    constructor(options = {}) {
        super();
        this.verbose = options.verbose || false;
        this.strict = options.strict || false;
        this.soulLock = options.soulLock || false;
        this.debounceMs = options.debounceMs || 300;
        this.quiet = options.quiet || false;
        this._watchers = [];
        this._debounceTimers = new Map();
        this._running = false;
        this._scanCount = 0;
        this._alertCount = 0;
    }

    watch(directory) {
        if (!directory) throw new Error('Watch directory is required');
        if (!fs.existsSync(directory)) throw new Error(`Directory not found: ${directory}`);
        if (!fs.statSync(directory).isDirectory()) throw new Error(`Not a directory: ${directory}`);

        this._running = true;

        if (!this.quiet) {
            console.log(`\n🛡️  guard-scanner watch mode`);
            console.log(`👁️  Watching: ${path.resolve(directory)}`);
            console.log(`⚡ Strict: ${this.strict ? 'ON' : 'OFF'}`);
            console.log(`🔒 Soul Lock: ${this.soulLock ? 'ON' : 'OFF'}`);
            console.log('───────────────────────────────');
            console.log('Press Ctrl+C to stop\n');
        }

        try {
            const watcher = fs.watch(directory, { recursive: true }, (eventType, filename) => {
                if (!filename || !this._running) return;
                const fullPath = path.join(directory, filename);

                // Debounce
                if (this._debounceTimers.has(fullPath)) {
                    clearTimeout(this._debounceTimers.get(fullPath));
                }
                this._debounceTimers.set(fullPath, setTimeout(() => {
                    this._debounceTimers.delete(fullPath);
                    this._onFileChange(directory, filename, eventType);
                }, this.debounceMs));
            });

            this._watchers.push(watcher);
            this.emit('watching', { directory: path.resolve(directory) });
        } catch (e) {
            this.emit('error', e);
        }

        return this;
    }

    _onFileChange(baseDir, filename, eventType) {
        if (!this._running) return;

        // Skip hidden files, node_modules, .git
        if (filename.startsWith('.') || filename.includes('node_modules') || filename.includes('.git')) {
            return;
        }

        // Skip non-code files
        const ext = path.extname(filename).toLowerCase();
        const codeExts = ['', '.ts', '.py', '.sh', '.md', '.json', '.yaml', '.yml', '.toml'];
        if (!codeExts.includes(ext)) return;

        const fullPath = path.join(baseDir, filename);
        if (!fs.existsSync(fullPath)) {
            this.emit('deleted', { file: filename });
            return;
        }

        this._scanCount++;
        const scanner = new GuardScanner({
            summaryOnly: true,
            strict: this.strict,
            soulLock: this.soulLock,
            quiet: true,
        });

        // Find the skill directory (parent directory of the changed file)
        const skillDir = path.dirname(fullPath);
        const skillName = path.basename(skillDir);

        try {
            scanner.scanSkill(skillDir, skillName);
            const findings = scanner.findings[0];

            if (findings && findings.findings.length > 0) {
                this._alertCount += findings.findings.length;
                const result = {
                    file: filename,
                    skill: skillName,
                    eventType,
                    verdict: findings.verdict,
                    risk: findings.risk,
                    findingCount: findings.findings.length,
                    findings: findings.findings,
                    timestamp: new Date().toISOString(),
                };

                this.emit('alert', result);

                if (!this.quiet) {
                    const icon = findings.verdict === 'MALICIOUS' ? '🚨' :
                        findings.verdict === 'SUSPICIOUS' ? '⚠️' : '🔶';
                    console.log(`${icon} [${new Date().toLocaleTimeString()}] ${findings.verdict} — ${filename}`);
                    console.log(`   Risk: ${findings.risk} | Findings: ${findings.findings.length}`);
                    if (this.verbose) {
                        for (const f of findings.findings.slice(0, 5)) {
                            console.log(`   → [${f.severity}] ${f.id}: ${f.desc}`);
                        }
                    }
                }
            } else {
                this.emit('clean', { file: filename, skill: skillName });
                if (this.verbose && !this.quiet) {
                    console.log(`✅ [${new Date().toLocaleTimeString()}] CLEAN — ${filename}`);
                }
            }
        } catch (e) {
            this.emit('error', { file: filename, error: e.message });
        }
    }

    stop() {
        this._running = false;
        for (const w of this._watchers) {
            try { w.close(); } catch (e) { /* ignore */ }
        }
        this._watchers = [];
        for (const t of this._debounceTimers.values()) {
            clearTimeout(t);
        }
        this._debounceTimers.clear();
        this.emit('stopped', { scanCount: this._scanCount, alertCount: this._alertCount });
        return { scanCount: this._scanCount, alertCount: this._alertCount };
    }

    getStats() {
        return {
            running: this._running,
            scanCount: this._scanCount,
            alertCount: this._alertCount,
            watcherCount: this._watchers.length,
        };
    }
}

export {  GuardWatcher  };
