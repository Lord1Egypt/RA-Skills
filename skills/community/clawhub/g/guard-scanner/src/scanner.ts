// @ts-nocheck
/**
 * guard-scanner v2.1.0 — Agent Skill Security Scanner 🛡️
 *
 * @security-manifest
 *   env-read: []
 *   env-write: []
 *   network: none
 *   fs-read: [scan target directory (user-specified)]
 *   fs-write: [JSON/SARIF/HTML reports to scan directory]
 *   exec: none
 *   purpose: Static analysis of agent skill files for threat patterns
 *
 * Based on GuavaGuard v9.0.0 (OSS extraction)
 * 20 threat categories • Snyk ToxicSkills + OWASP MCP Top 10
 * Lightweight runtime footprint • CLI + JSON + SARIF + HTML output
 * Plugin API for custom detection rules
 *
 * Born from a real 3-day agent identity hijack (2026-02-12)
 *
 * License: MIT
 */

import fs  from 'fs';
import path  from 'path';
import os  from 'os';

import { PATTERNS  } from './patterns';
import { KNOWN_MALICIOUS  } from './ioc-db';
import { RuleRegistry  } from './core/rule-registry';
import { loadIgnoreFile, loadTextFile  } from './core/content-loader';
import { classifyFile, CODE_EXTENSIONS, BINARY_EXTENSIONS, isSelfNoisePath, isSelfThreatCorpus, getFiles, listSkills  } from './core/inventory';
import { calculateRisk, getVerdict, SEVERITY_WEIGHTS  } from './core/risk-engine';
import { applySemanticValidators, checkASTValidation  } from './core/semantic-validators';
import { toJSONReport, toSARIFReport, toHTMLReport, printSummary  } from './core/report-adapters';
import { inferFindingContext  } from './v16-taxonomy';
import { getCurrentModuleDir } from './module-path';
import { generateModel  } from './threat-model';
import { analyzePopulationMonitor  } from './population-monitor';
import { analyzeMetaGuard  } from './meta-guard';

// ===== CONFIGURATION =====
import pkg from '../package.json' assert { type: 'json' }; const { version: VERSION } = pkg;
const MODULE_DIR = getCurrentModuleDir();

const THRESHOLDS = {
    normal: { suspicious: 30, malicious: 80 },
    strict: { suspicious: 20, malicious: 60 },
};

class GuardScanner {
    constructor(options = {}) {
        this.verbose = options.verbose || false;
        this.selfExclude = options.selfExclude || false;
        this.strict = options.strict || false;
        this.summaryOnly = options.summaryOnly || false;
        this.quiet = options.quiet || false;
        this.checkDeps = options.checkDeps || false;
        this.soulLock = options.soulLock || false;
        this.scannerDir = path.resolve(MODULE_DIR);
        this.thresholds = this.strict ? THRESHOLDS.strict : THRESHOLDS.normal;
        this.findings = [];
        this.stats = { scanned: 0, clean: 0, low: 0, suspicious: 0, malicious: 0 };
        this.ignoredSkills = new Set();
        this.ignoredPatterns = new Set();
        this.customRules = [];
        this.compliance = options.compliance || null;
        this.populationEvents = Array.isArray(options.populationEvents) ? options.populationEvents : [];
        this.metaGuardInput = options.metaGuardInput || null;
        this.threatModelInputs = [];

        // Plugin API: load plugins
        if (options.plugins && Array.isArray(options.plugins)) {
            for (const plugin of options.plugins) {
                this.loadPlugin(plugin);
            }
        }

        // Custom rules file (legacy compat)
        if (options.rulesFile) {
            this.loadCustomRules(options.rulesFile);
        }

        this.ruleRegistry = new RuleRegistry(PATTERNS, this.customRules);
    }

    // Plugin API: load a plugin module
    loadPlugin(pluginPath) {
        try {
            const plugin = require(path.resolve(pluginPath));
            if (plugin.patterns && Array.isArray(plugin.patterns)) {
                for (const p of plugin.patterns) {
                    if (p.id && p.regex && p.severity && p.cat && p.desc) {
                        this.customRules.push(p);
                    }
                }
                if (!this.summaryOnly) {
                    console.log(`🔌 Plugin loaded: ${plugin.name || pluginPath} (${plugin.patterns.length} rule(s))`);
                }
                this.ruleRegistry = new RuleRegistry(PATTERNS, this.customRules);
            }
        } catch (e) {
            console.error(`⚠️  Failed to load plugin ${pluginPath}: ${e.message}`);
        }
    }

    // Custom rules from JSON file
    loadCustomRules(rulesFile) {
        try {
            const content = fs.readFileSync(rulesFile, 'utf-8');
            const rules = JSON.parse(content);
            if (!Array.isArray(rules)) {
                console.error(`⚠️  Custom rules file must be a JSON array`);
                return;
            }
            for (const rule of rules) {
                if (!rule.id || !rule.pattern || !rule.severity || !rule.cat || !rule.desc) {
                    console.error(`⚠️  Skipping invalid rule: ${JSON.stringify(rule).substring(0, 80)}`);
                    continue;
                }
                try {
                    const flags = rule.flags || 'gi';
                    this.customRules.push({
                        id: rule.id,
                        cat: rule.cat,
                        regex: new RegExp(rule.pattern, flags),
                        severity: rule.severity,
                        desc: rule.desc,
                        codeOnly: rule.codeOnly || false,
                        docOnly: rule.docOnly || false,
                        all: !rule.codeOnly && !rule.docOnly
                    });
                } catch (e) {
                    console.error(`⚠️  Invalid regex in rule ${rule.id}: ${e.message}`);
                }
            }
            if (!this.summaryOnly && this.customRules.length > 0) {
                console.log(`📏 Loaded ${this.customRules.length} custom rule(s) from ${rulesFile}`);
            }
            this.ruleRegistry = new RuleRegistry(PATTERNS, this.customRules);
        } catch (e) {
            console.error(`⚠️  Failed to load custom rules: ${e.message}`);
        }
    }

    // Load .guava-guard-ignore / .guard-scanner-ignore from scan directory
    loadIgnoreFile(scanDir) {
        const ignored = loadIgnoreFile(scanDir);
        this.ignoredSkills = ignored.ignoredSkills;
        this.ignoredPatterns = ignored.ignoredPatterns;
        if (this.verbose && (this.ignoredSkills.size || this.ignoredPatterns.size)) {
            console.log(`📋 Loaded ignore file: ${this.ignoredSkills.size} skills, ${this.ignoredPatterns.size} patterns`);
        }
    }

    /**
     * Scan raw text for threats (used for Discord incoming messages, etc.)
     * @param {string} text - Raw text to scan
     * @returns {{ safe: boolean, risk: number, detections: Array }}
     */
    scanText(text) {
        this.threatModelInputs = [text];
        const findings = [];
        this.checkIoCs(text, 'raw_text', findings);
        this.checkPatterns(text, 'raw_text', 'code', findings); // use 'code' to run all patterns
        if (this.customRules.length > 0) {
            this.checkPatterns(text, 'raw_text', 'code', findings, this.customRules);
        }
        applySemanticValidators(text, 'raw_text', findings);
        this.analyzeProtocolFindings(text, 'raw_text', 'code', findings);
        this.analyzeCognitiveFindings(text, 'raw_text', 'code', findings);
        this.analyzeThreatIntelFindings(text, 'raw_text', 'code', findings);
        this.appendThreatModelFindings(text, findings, 'raw_text');
        
        // Filter ignored patterns
        const filteredFindings = findings.filter(f => !this.ignoredPatterns.has(f.id));
        this.annotateV16Findings(filteredFindings);
        const risk = this.calculateRisk(filteredFindings);
        
        return {
            safe: risk < this.thresholds.suspicious,
            risk,
            detections: filteredFindings
        };
    }

    scanDirectory(dir) {
        if (!fs.existsSync(dir)) {
            throw new Error(`Directory not found: ${dir}`);
        }

        this.threatModelInputs = [];
        this.loadIgnoreFile(dir);

        const rootSkillMd = path.join(dir, 'SKILL.md');
        const skills = fs.existsSync(rootSkillMd)
            ? [{ name: path.basename(path.resolve(dir)), path: path.resolve(dir) }]
            : listSkills(dir).map((skill) => ({ name: skill, path: path.join(dir, skill) }));

        if (!this.quiet) {
            console.log(`\n🛡️  guard-scanner v${VERSION}`);
            console.log(`${'═'.repeat(54)}`);
            console.log(`📂 Scanning: ${dir}`);
            console.log(`📦 Skills found: ${skills.length}`);
            if (this.strict) console.log(`⚡ Strict mode enabled`);
            console.log();
        }

        for (const skill of skills) {
            const skillPath = skill.path;
            const skillName = skill.name;

            // Self-exclusion
            if (this.selfExclude && path.resolve(skillPath) === this.scannerDir) {
                if (!this.summaryOnly && !this.quiet) console.log(`⏭️  ${skillName} — SELF (excluded)`);
                continue;
            }

            // Ignore list
            if (this.ignoredSkills.has(skillName)) {
                if (!this.summaryOnly && !this.quiet) console.log(`⏭️  ${skillName} — IGNORED`);
                continue;
            }

            this.scanSkill(skillPath, skillName);
        }

        if (!this.quiet) this.printSummary();
        return this.findings;
    }

    scanTarget(targetPath) {
        this.findings = [];
        this.stats = { scanned: 0, clean: 0, low: 0, suspicious: 0, malicious: 0 };
        this.scanDirectory(targetPath);
        return this.toJSON();
    }

    scanSkill(skillPath, skillName) {
        this.stats.scanned++;
        const skillFindings = [];
        const skillContentParts = [];

        // Check 1: Known malicious skill name
        if (KNOWN_MALICIOUS.typosquats.includes(skillName.toLowerCase())) {
            skillFindings.push({
                severity: 'CRITICAL', id: 'KNOWN_TYPOSQUAT', cat: 'malicious-code',
                desc: `Known malicious/typosquat skill name`,
                file: 'SKILL NAME', line: 0
            });
        }

        // Check 2: Scan all files
        const files = this.getFiles(skillPath);
        for (const file of files) {
            const ext = path.extname(file).toLowerCase();
            const relFile = path.relative(skillPath, file);

            if (relFile.includes('node_modules/') || relFile.includes('node_modules\\')) continue;
            if (relFile.startsWith('.git/') || relFile.startsWith('.git\\')) continue;
            if (BINARY_EXTENSIONS.has(ext)) continue;
            if (this.isSelfNoisePath(skillName, relFile)) continue;

            const content = loadTextFile(file);
            if (content === null) continue;
            skillContentParts.push(content);

            const fileType = this.classifyFile(ext, relFile);

            // IoC checks
            if (!this.isSelfThreatCorpus(skillName, relFile)) {
                this.checkIoCs(content, relFile, skillFindings);
            }

            // Pattern checks (context-aware)
            this.checkPatterns(content, relFile, fileType, skillFindings);

            // Custom rules / plugins
            if (this.customRules.length > 0) {
                this.checkPatterns(content, relFile, fileType, skillFindings, this.customRules);
            }

            // Hardcoded secret detection
            const baseName = path.basename(relFile).toLowerCase();
            const skipSecretCheck = baseName.endsWith('-lock.json') || baseName === 'package-lock.json' ||
                baseName === 'yarn.lock' || baseName === 'pnpm-lock.yaml' ||
                baseName === '_meta.json' || baseName === '.package-lock.json';
            if (fileType === 'code' && !skipSecretCheck) {
                this.checkHardcodedSecrets(content, relFile, skillFindings);
            }

            // Lightweight JS data flow analysis
            if ((ext === '' || ext === '.mjs' || ext === '.cjs' || ext === '.ts') && content.length < 200000) {
                this.checkJSDataFlow(content, relFile, skillFindings);
            }
            applySemanticValidators(content, relFile, skillFindings);
            this.analyzeProtocolFindings(content, relFile, fileType, skillFindings);
            this.analyzeCognitiveFindings(content, relFile, fileType, skillFindings);
            this.analyzeThreatIntelFindings(content, relFile, fileType, skillFindings);
        }

        const skillContent = skillContentParts.join('\n');
        this.appendThreatModelFindings(skillContent, skillFindings, skillName);
        if (skillContent) {
            this.threatModelInputs.push(skillContent);
        }

        // Check 3: Structural checks
        this.checkStructure(skillPath, skillName, skillFindings);

        // Check 4: Dependency chain scanning
        if (this.checkDeps) {
            this.checkDependencies(skillPath, skillName, skillFindings);
        }

        // Check 5: Hidden files detection
        this.checkHiddenFiles(skillPath, skillName, skillFindings);

        // Check 6: Cross-file analysis
        this.checkCrossFile(skillPath, skillName, skillFindings);
        this.checkRuntimeIntegration(skillPath, skillName, skillFindings);

        // Check 7: Skill manifest validation (v1.1)
        this.checkSkillManifest(skillPath, skillName, skillFindings);

        // Check 8: Code complexity metrics (v1.1)
        this.checkComplexity(skillPath, skillName, skillFindings);

        // Check 9: Config impact analysis (v1.1)
        this.checkConfigImpact(skillPath, skillName, skillFindings);

        // Filter ignored patterns
        const filteredFindings = skillFindings.filter(f => !this.ignoredPatterns.has(f.id));
        this.annotateV16Findings(filteredFindings);

        // Calculate risk
        const risk = this.calculateRisk(filteredFindings);
        const verdict = this.getVerdict(risk);

        this.stats[verdict.stat]++;

        if (!this.summaryOnly && !this.quiet) {
            console.log(`${verdict.icon} ${skillName} — ${verdict.label} (risk: ${risk})`);

            if (this.verbose && filteredFindings.length > 0) {
                const byCat = {};
                for (const f of filteredFindings) {
                    (byCat[f.cat] = byCat[f.cat] || []).push(f);
                }
                for (const [cat, findings] of Object.entries(byCat)) {
                    console.log(`   📁 ${cat}`);
                    for (const f of findings) {
                        const icon = f.severity === 'CRITICAL' ? '💀' : f.severity === 'HIGH' ? '🔴' : f.severity === 'MEDIUM' ? '🟡' : '⚪';
                        const loc = f.line ? `${f.file}:${f.line}` : f.file;
                        const layerLabel = f.layer_name || inferFindingContext(f).layer_name;
                        console.log(`      ${icon} [${f.severity}] ${f.desc} — ${loc} (${layerLabel})`);
                        if (f.sample) console.log(`         └─ "${f.sample}"`);
                    }
                }
            }
        }

        if (filteredFindings.length > 0) {
            this.findings.push({ skill: skillName, risk, verdict: verdict.label, findings: filteredFindings });
        }
    }

    classifyFile(ext, relFile) {
        return classifyFile(ext, relFile);
    }

    isSelfNoisePath(skillName, relFile) {
        return isSelfNoisePath(skillName, relFile);
    }

    isSelfThreatCorpus(skillName, relFile) {
        return isSelfThreatCorpus(skillName, relFile);
    }

    checkIoCs(content, relFile, findings) {
        const contentLower = content.toLowerCase();

        for (const ip of KNOWN_MALICIOUS.ips) {
            if (content.includes(ip)) {
                findings.push({ severity: 'CRITICAL', id: 'IOC_IP', cat: 'malicious-code', desc: `Known malicious IP: ${ip}`, file: relFile });
            }
        }

        for (const url of KNOWN_MALICIOUS.urls) {
            if (contentLower.includes(url.toLowerCase())) {
                findings.push({ severity: 'CRITICAL', id: 'IOC_URL', cat: 'malicious-code', desc: `Known malicious URL: ${url}`, file: relFile });
            }
        }

        for (const domain of KNOWN_MALICIOUS.domains) {
            const domainRegex = new RegExp(`(?:https?://|[\\s'"\`(]|^)${domain.replace(/\./g, '\\.')}`, 'gi');
            if (domainRegex.test(content)) {
                findings.push({ severity: 'HIGH', id: 'IOC_DOMAIN', cat: 'exfiltration', desc: `Suspicious domain: ${domain}`, file: relFile });
            }
        }

        for (const fname of KNOWN_MALICIOUS.filenames) {
            if (contentLower.includes(fname.toLowerCase())) {
                findings.push({ severity: 'CRITICAL', id: 'IOC_FILE', cat: 'suspicious-download', desc: `Known malicious filename: ${fname}`, file: relFile });
            }
        }

        for (const user of KNOWN_MALICIOUS.usernames) {
            if (contentLower.includes(user.toLowerCase())) {
                findings.push({ severity: 'HIGH', id: 'IOC_USER', cat: 'malicious-code', desc: `Known malicious username: ${user}`, file: relFile });
            }
        }
    }

    annotateV16Findings(findings) {
        for (const finding of findings) {
            const inferred = inferFindingContext(finding);
            if (finding.layer === undefined) finding.layer = inferred.layer;
            if (finding.layer_name === undefined) finding.layer_name = inferred.layer_name;
            if (finding.owasp_asi === undefined) finding.owasp_asi = inferred.owasp_asi;
            if (finding.protocol_surface === undefined) finding.protocol_surface = inferred.protocol_surface;
        }
    }

    pushUniqueFinding(findings, finding) {
        const key = `${finding.id}|${finding.file || ''}|${finding.line || 0}|${finding.desc || ''}`;
        const exists = findings.some((current) => `${current.id}|${current.file || ''}|${current.line || 0}|${current.desc || ''}` === key);
        if (!exists) findings.push(finding);
    }

    analyzeProtocolFindings(content, relFile, fileType, findings) {
        const checks = [
            {
                id: 'PROTO_WS_INSECURE_TRANSPORT',
                when: /new\s+WebSocket\s*\(\s*['"`]ws:\/\//i,
                finding: {
                    severity: 'HIGH',
                    cat: 'agent-protocol',
                    desc: 'Protocol: insecure WebSocket transport without TLS',
                    protocol_surface: ['websocket'],
                    owasp_asi: ['ASI07'],
                    layer: 2,
                },
            },
            {
                id: 'PROTO_MCP_TOOL_MUTATION_V16',
                when: /(tools\/list|tool[s]?)[\s\S]{0,120}(redefine|override|replace|mutate)/i,
                finding: {
                    severity: 'HIGH',
                    cat: 'mcp-security',
                    desc: 'Protocol: MCP tool definition mutation risk',
                    protocol_surface: ['mcp'],
                    owasp_asi: ['ASI07'],
                    layer: 2,
                },
            },
            {
                id: 'PROTO_AGENT_IDENTITY_SPOOF_V16',
                when: /(agent.?card|trusted origin|x-agent-id|authorization)[\s\S]{0,120}(spoof|forge|impersonat|override)/i,
                finding: {
                    severity: 'HIGH',
                    cat: 'a2a-contagion',
                    desc: 'Protocol: agent identity spoofing or trusted-origin abuse',
                    protocol_surface: ['a2a', 'machine-identity'],
                    owasp_asi: ['ASI07', 'ASI10'],
                    layer: 2,
                },
            },
            {
                id: 'PROTO_SESSION_REPLAY_V16',
                when: /(session|task)[\s\S]{0,80}(replay|resume|smuggle|persist)/i,
                finding: {
                    severity: 'HIGH',
                    cat: 'agent-protocol',
                    desc: 'Runtime: session replay or smuggling path detected',
                    protocol_surface: ['session-boundary', 'a2a'],
                    owasp_asi: ['ASI07'],
                    layer: 3,
                },
            },
            {
                id: 'PROTO_CRED_FLOW_TRACE_V16',
                when: /(client_secret|access_token|authorization|bearer|api[_-]?key|private[_-]?key)[\s\S]{0,120}(fetch|websocket|send|emit|postMessage|tool[s]?\/call)/i,
                finding: {
                    severity: 'CRITICAL',
                    cat: 'credential-handling',
                    desc: 'Protocol: credential-bearing data may cross a protocol boundary',
                    protocol_surface: ['credential-flow'],
                    owasp_asi: ['ASI02', 'ASI07'],
                    layer: 2,
                },
            },
            {
                id: 'PROTO_MCP_SSRF_V17',
                when: /(resources\/(?:read|list)|mcp)[\s\S]{0,160}(https?:\/\/(?:127\.0\.0\.1|localhost)|169\.254\.169\.254|metadata\.google)/i,
                finding: {
                    severity: 'CRITICAL',
                    cat: 'mcp-security',
                    desc: 'Protocol: MCP resource fetch may pivot into localhost or metadata endpoints',
                    protocol_surface: ['mcp', 'resource', 'ssrf'],
                    owasp_asi: ['ASI02', 'ASI07'],
                    layer: 2,
                },
            },
            {
                id: 'PROTO_MCP_CONNECTOR_POISON_V17',
                when: /(mcp|connector|registry)[\s\S]{0,160}(poison|shadow|rogue|tamper|unverified publisher)/i,
                finding: {
                    severity: 'HIGH',
                    cat: 'mcp-security',
                    desc: 'Protocol: MCP connector or registry poisoning indicator',
                    protocol_surface: ['mcp', 'registry', 'connector'],
                    owasp_asi: ['ASI04', 'ASI07'],
                    layer: 2,
                },
            },
            {
                id: 'PROTO_MCP_JSONRPC_INJECT_V17',
                when: /(jsonrpc|content-length|stdin\.write)[\s\S]{0,160}(inject|smuggle|override|truncate)/i,
                finding: {
                    severity: 'CRITICAL',
                    cat: 'mcp-security',
                    desc: 'Protocol: MCP transport or JSON-RPC message injection indicator',
                    protocol_surface: ['mcp', 'json-rpc', 'transport'],
                    owasp_asi: ['ASI07'],
                    layer: 2,
                },
            },
        ];

        for (const check of checks) {
            const match = content.match(check.when);
            if (!match) continue;
            const idx = content.search(check.when);
            const line = idx >= 0 ? content.substring(0, idx).split('\n').length : null;
            this.pushUniqueFinding(findings, {
                ...check.finding,
                id: check.id,
                file: relFile,
                line,
                sample: match[0].substring(0, 80),
            });
        }
    }

    analyzeCognitiveFindings(content, relFile, fileType, findings) {
        const checks = [
            {
                id: 'COG_GOAL_DRIFT_V16',
                when: /(ignore|drop|rewrite|replace)\s+(the\s+)?(goal|objective|mission|success criteria)/i,
                finding: {
                    severity: 'HIGH',
                    cat: 'behavioral-guard',
                    desc: 'Cognitive: goal-drift proxy detected',
                    owasp_asi: ['ASI01'],
                    layer: 4,
                },
            },
            {
                id: 'COG_TRUST_BIAS_V16',
                when: /(trusted|authority|creator|partner|owner)[\s\S]{0,100}(skip|ignore|bypass|disable)\s+(guard|review|verification|safety)/i,
                finding: {
                    severity: 'HIGH',
                    cat: 'trust-exploitation',
                    desc: 'Cognitive: trust-bias shortcut may override verification',
                    owasp_asi: ['ASI09'],
                    layer: 4,
                },
            },
            {
                id: 'COG_CASCADING_HANDOFF_V16',
                when: /(handoff|delegate|forward|relay)[\s\S]{0,80}(agent|tool|task)[\s\S]{0,120}(without review|auto|automatic)/i,
                finding: {
                    severity: 'MEDIUM',
                    cat: 'behavioral-guard',
                    desc: 'Cognitive: cascading handoff without review',
                    owasp_asi: ['ASI08'],
                    layer: 4,
                },
            },
        ];

        for (const check of checks) {
            const match = content.match(check.when);
            if (!match) continue;
            const idx = content.search(check.when);
            const line = idx >= 0 ? content.substring(0, idx).split('\n').length : null;
            this.pushUniqueFinding(findings, {
                ...check.finding,
                id: check.id,
                file: relFile,
                line,
                sample: match[0].substring(0, 80),
            });
        }
    }

    analyzeThreatIntelFindings(content, relFile, fileType, findings) {
        const checks = [
            {
                id: 'TI_MACHINE_IDENTITY_EXPOSURE_V16',
                when: /(client_secret|private_key|id_token|refresh_token|service account|oauth client)/i,
                finding: {
                    severity: 'HIGH',
                    cat: 'credential-handling',
                    desc: 'Threat intel: machine identity or long-lived credential material detected',
                    protocol_surface: ['machine-identity', 'credential-flow'],
                    owasp_asi: ['ASI07'],
                    layer: 5,
                },
            },
            {
                id: 'TI_REGISTRY_SHADOW_HINT_V16',
                when: /(registry|server|plugin)[\s\S]{0,100}(shadow|unverified|rogue|unknown publisher)/i,
                finding: {
                    severity: 'MEDIUM',
                    cat: 'unverifiable-deps',
                    desc: 'Threat intel: unverified registry or plugin provenance hint',
                    protocol_surface: ['registry'],
                    owasp_asi: ['ASI04'],
                    layer: 5,
                },
            },
            {
                id: 'TI_PROTOCOL_BUDGET_ABUSE_V16',
                when: /(max[_ -]?tokens|overthink|reasoning effort|budget|quota)[\s\S]{0,100}(increase|drain|exhaust|infinite)/i,
                finding: {
                    severity: 'MEDIUM',
                    cat: 'advanced-exfil',
                    desc: 'Threat intel: protocol or reasoning budget abuse indicator',
                    owasp_asi: ['ASI08'],
                    layer: 5,
                },
            },
        ];

        for (const check of checks) {
            const match = content.match(check.when);
            if (!match) continue;
            const idx = content.search(check.when);
            const line = idx >= 0 ? content.substring(0, idx).split('\n').length : null;
            this.pushUniqueFinding(findings, {
                ...check.finding,
                id: check.id,
                file: relFile,
                line,
                sample: match[0].substring(0, 80),
            });
        }
    }

    checkPatterns(content, relFile, fileType, findings, patterns = null) {
        const activePatterns = patterns || this.ruleRegistry.getRulesForFileType(fileType);
        // v9: Payload Unfurling (Base64 / Hex Decoders)
        let unfurledContent = content;

        // Unfurl Buffer.from('...', 'base64') and atob('...')
        const b64Regex = /(?:Buffer\.from\(\s*['"]([^'"]+)['"]\s*,\s*['"]base64['"]\)|atob\(\s*['"]([^'"]+)['"]\))/g;
        unfurledContent = unfurledContent.replace(b64Regex, (match, g1, g2) => {
            try {
                const b64 = g1 || g2;
                return Buffer.from(b64, 'base64').toString('utf8');
            } catch { return match; }
        });

        // Unfurl hex escaped strings like \x63\x61\x74 -> cat
        unfurledContent = unfurledContent.replace(/\\x([0-9a-fA-F]{2})/g, (match, hex) => {
            return String.fromCharCode(parseInt(hex, 16));
        });

        for (const pattern of activePatterns) {
            // Soul Lock: skip identity-hijack/memory-poisoning patterns unless --soul-lock is enabled
            if (pattern.soulLock && !this.soulLock) continue;
            if (pattern.codeOnly && fileType !== 'code') continue;
            if (pattern.docOnly && fileType !== 'doc' && fileType !== 'skill-doc') continue;
            if (!pattern.all && !pattern.codeOnly && !pattern.docOnly && pattern.scope !== 'skill-doc') continue;

            pattern.regex.lastIndex = 0;
            let matches = content.match(pattern.regex);
            let targetContent = content;

            // If no match on raw content, try unfurled content
            if (!matches && unfurledContent !== content) {
                pattern.regex.lastIndex = 0;
                matches = unfurledContent.match(pattern.regex);
                targetContent = unfurledContent;
            }

            if (!matches) continue;

            pattern.regex.lastIndex = 0;
            const idx = targetContent.search(pattern.regex);
            const lineNum = idx >= 0 ? targetContent.substring(0, idx).split('\n').length : null;

            let adjustedSeverity = pattern.severity;
            if ((fileType === 'doc' || fileType === 'skill-doc') && pattern.all && !pattern.docOnly) {
                if (adjustedSeverity === 'HIGH') adjustedSeverity = 'MEDIUM';
                else if (adjustedSeverity === 'MEDIUM') adjustedSeverity = 'LOW';
            }

            findings.push({
                severity: adjustedSeverity,
                id: pattern.id,
                cat: pattern.cat || pattern.category,
                desc: pattern.desc || pattern.description,
                file: relFile,
                line: lineNum,
                matchCount: matches.length,
                sample: matches[0].substring(0, 80)
            });
        }
    }

    // Entropy-based secret detection
    checkHardcodedSecrets(content, relFile, findings) {
        const assignmentRegex = /(?:api[_-]?key|secret|token|password|credential|auth)\s*[:=]\s*['"]([a-zA-Z0-9_\-+/=]{16,})['"]|['"]([a-zA-Z0-9_\-+/=]{32,})['"]/gi;
        let match;
        while ((match = assignmentRegex.exec(content)) !== null) {
            const value = match[1] || match[2];
            if (!value) continue;

            if (/^[A-Z_]+$/.test(value)) continue;
            if (/^(true|false|null|undefined|none|default|example|test|placeholder|your[_-])/i.test(value)) continue;
            if (/^x{4,}|\.{4,}|_{4,}|0{8,}$/i.test(value)) continue;
            if (/^projects\/|^gs:\/\/|^https?:\/\//i.test(value)) continue;
            if (/^[a-z]+-[a-z]+-[a-z0-9]+$/i.test(value)) continue;

            const entropy = this.shannonEntropy(value);
            if (entropy > 3.5 && value.length >= 20) {
                const lineNum = content.substring(0, match.index).split('\n').length;
                findings.push({
                    severity: 'HIGH', id: 'SECRET_ENTROPY', cat: 'secret-detection',
                    desc: `High-entropy string (possible leaked secret, entropy=${entropy.toFixed(1)})`,
                    file: relFile, line: lineNum,
                    sample: value.substring(0, 8) + '...' + value.substring(value.length - 4)
                });
            }
        }
    }

    shannonEntropy(str) {
        const freq = {};
        for (const c of str) freq[c] = (freq[c] || 0) + 1;
        const len = str.length;
        let entropy = 0;
        for (const count of Object.values(freq)) {
            const p = count / len;
            if (p > 0) entropy -= p * Math.log2(p);
        }
        return entropy;
    }

    checkStructure(skillPath, skillName, findings) {
        const skillMd = path.join(skillPath, 'SKILL.md');
        if (!fs.existsSync(skillMd)) {
            findings.push({ severity: 'LOW', id: 'STRUCT_NO_SKILLMD', cat: 'structural', desc: 'No SKILL.md found', file: skillName });
            return;
        }
        const content = fs.readFileSync(skillMd, 'utf-8');
        if (content.length < 50) {
            findings.push({ severity: 'MEDIUM', id: 'STRUCT_TINY_SKILLMD', cat: 'structural', desc: 'Suspiciously short SKILL.md (< 50 chars)', file: 'SKILL.md' });
        }
        const scriptsDir = path.join(skillPath, 'scripts');
        if (fs.existsSync(scriptsDir)) {
            const scripts = fs.readdirSync(scriptsDir).filter(f => CODE_EXTENSIONS.has(path.extname(f).toLowerCase()));
            if (scripts.length > 0 && !content.includes('scripts/')) {
                findings.push({ severity: 'MEDIUM', id: 'STRUCT_UNDOCUMENTED_SCRIPTS', cat: 'structural', desc: `${scripts.length} script(s) in scripts/ not referenced in SKILL.md`, file: 'scripts/' });
            }
        }
    }

    checkDependencies(skillPath, skillName, findings) {
        const pkgPath = path.join(skillPath, 'package.json');
        if (!fs.existsSync(pkgPath)) return;

        let pkg;
        try { pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8')); } catch { return; }

        const allDeps = { ...pkg.dependencies, ...pkg.devDependencies, ...pkg.optionalDependencies };

        const RISKY_PACKAGES = new Set([
            'node-ipc', 'colors', 'faker', 'event-stream', 'ua-parser-js', 'coa', 'rc',
        ]);

        for (const [dep, version] of Object.entries(allDeps)) {
            if (RISKY_PACKAGES.has(dep)) {
                findings.push({ severity: 'HIGH', id: 'DEP_RISKY', cat: 'dependency-chain', desc: `Known risky dependency: ${dep}@${version}`, file: 'package.json' });
            }
            if (typeof version === 'string' && (version.startsWith('git+') || version.startsWith('http') || version.startsWith('github:') || version.includes('.tar.gz'))) {
                findings.push({ severity: 'HIGH', id: 'DEP_REMOTE', cat: 'dependency-chain', desc: `Remote/git dependency: ${dep}@${version}`, file: 'package.json' });
            }
            if (version === '*' || version === 'latest') {
                findings.push({ severity: 'MEDIUM', id: 'DEP_WILDCARD', cat: 'dependency-chain', desc: `Wildcard version: ${dep}@${version}`, file: 'package.json' });
            }
        }

        const RISKY_SCRIPTS = ['preinstall', 'postinstall', 'preuninstall', 'postuninstall', 'prepare'];
        if (pkg.scripts) {
            for (const scriptName of RISKY_SCRIPTS) {
                if (pkg.scripts[scriptName]) {
                    const cmd = pkg.scripts[scriptName];
                    findings.push({ severity: 'HIGH', id: 'DEP_LIFECYCLE', cat: 'dependency-chain', desc: `Lifecycle script "${scriptName}": ${cmd.substring(0, 80)}`, file: 'package.json' });
                    if (/curl|wget|node\s+-e|eval|exec|bash\s+-c/i.test(cmd)) {
                        findings.push({ severity: 'CRITICAL', id: 'DEP_LIFECYCLE_EXEC', cat: 'dependency-chain', desc: `Lifecycle script "${scriptName}" downloads/executes code`, file: 'package.json', sample: cmd.substring(0, 80) });
                    }
                }
            }
        }
    }

    // ── v1.1: Skill Manifest Validation ──
    // Checks SKILL.md frontmatter for dangerous tool declarations,
    // overly broad file scope, and sensitive env requirements
    checkSkillManifest(skillPath, skillName, findings) {
        const skillMd = path.join(skillPath, 'SKILL.md');
        if (!fs.existsSync(skillMd)) return;

        let content;
        try { content = fs.readFileSync(skillMd, 'utf-8'); } catch { return; }

        // Parse YAML frontmatter (lightweight, no dependency)
        const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
        if (!fmMatch) return;
        const fm = fmMatch[1];

        // Check 1: Dangerous binary requirements
        const DANGEROUS_BINS = new Set([
            'sudo', 'rm', 'rmdir', 'chmod', 'chown', 'kill', 'pkill',
            'curl', 'wget', 'nc', 'ncat', 'socat', 'ssh', 'scp',
            'dd', 'mkfs', 'fdisk', 'mount', 'umount',
            'iptables', 'ufw', 'firewall-cmd',
            'docker', 'kubectl', 'systemctl',
        ]);
        const binsMatch = fm.match(/bins:\s*\n((?:\s+-\s+[^\n]+\n?)*)/i);
        if (binsMatch) {
            const bins = binsMatch[1].match(/- ([^\n]+)/g) || [];
            for (const binLine of bins) {
                const bin = binLine.replace(/^-\s*/, '').trim().toLowerCase();
                if (DANGEROUS_BINS.has(bin)) {
                    findings.push({
                        severity: 'HIGH', id: 'MANIFEST_DANGEROUS_BIN',
                        cat: 'sandbox-validation',
                        desc: `SKILL.md requires dangerous binary: ${bin}`,
                        file: 'SKILL.md'
                    });
                }
            }
        }

        // Check 2: Overly broad file scope
        const filesMatch = fm.match(/files:\s*\[([^\]]+)\]/i) || fm.match(/files:\s*\n((?:\s+-\s+[^\n]+\n?)*)/i);
        if (filesMatch) {
            const filesStr = filesMatch[1];
            if (/\*\*\/\*|\*\.\*|\"\*\"/i.test(filesStr)) {
                findings.push({
                    severity: 'HIGH', id: 'MANIFEST_BROAD_FILES',
                    cat: 'sandbox-validation',
                    desc: 'SKILL.md declares overly broad file scope (e.g. **/*)',
                    file: 'SKILL.md'
                });
            }
        }

        // Check 3: Sensitive env requirements
        const SENSITIVE_ENV_PATTERNS = /(?:SECRET|PASSWORD|CREDENTIAL|PRIVATE_KEY|AWS_SECRET|GITHUB_TOKEN)/i;
        const envMatch = fm.match(/env:\s*\n((?:\s+-\s+[^\n]+\n?)*)/i);
        if (envMatch) {
            const envVars = envMatch[1].match(/- ([^\n]+)/g) || [];
            for (const envLine of envVars) {
                const envVar = envLine.replace(/^-\s*/, '').trim();
                if (SENSITIVE_ENV_PATTERNS.test(envVar)) {
                    findings.push({
                        severity: 'HIGH', id: 'MANIFEST_SENSITIVE_ENV',
                        cat: 'sandbox-validation',
                        desc: `SKILL.md requires sensitive env var: ${envVar}`,
                        file: 'SKILL.md'
                    });
                }
            }
        }

        // Check 4: exec or network declared without justification
        if (/exec:\s*(?:true|yes|enabled|'\*'|"\*")/i.test(fm)) {
            findings.push({
                severity: 'MEDIUM', id: 'MANIFEST_EXEC_DECLARED',
                cat: 'sandbox-validation',
                desc: 'SKILL.md declares exec capability',
                file: 'SKILL.md'
            });
        }
        if (/network:\s*(?:true|yes|enabled|'\*'|"\*"|all|any)/i.test(fm)) {
            findings.push({
                severity: 'MEDIUM', id: 'MANIFEST_NETWORK_DECLARED',
                cat: 'sandbox-validation',
                desc: 'SKILL.md declares unrestricted network access',
                file: 'SKILL.md'
            });
        }
    }

    // ── v1.1: Code Complexity Metrics ──
    // Detects excessive file length, deep nesting, and eval/exec density
    checkComplexity(skillPath, skillName, findings) {
        const files = this.getFiles(skillPath);
        const MAX_LINES = 1000;
        const MAX_NESTING = 5;
        const MAX_EVAL_DENSITY = 0.02; // 2% of lines

        for (const file of files) {
            const ext = path.extname(file).toLowerCase();
            if (!CODE_EXTENSIONS.has(ext)) continue;

            const relFile = path.relative(skillPath, file);
            if (relFile.includes('node_modules') || relFile.startsWith('.git')) continue;

            let content;
            try { content = fs.readFileSync(file, 'utf-8'); } catch { continue; }

            const lines = content.split('\n');

            // Check 1: Excessive file length
            if (lines.length > MAX_LINES) {
                findings.push({
                    severity: 'MEDIUM', id: 'COMPLEXITY_LONG_FILE',
                    cat: 'complexity',
                    desc: `File exceeds ${MAX_LINES} lines (${lines.length} lines)`,
                    file: relFile
                });
            }

            // Check 2: Deep nesting (brace tracking)
            let maxDepth = 0;
            let currentDepth = 0;
            let deepestLine = 0;
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                // Count opening/closing braces outside strings (simplified)
                for (const ch of line) {
                    if (ch === '{') currentDepth++;
                    if (ch === '}') currentDepth = Math.max(0, currentDepth - 1);
                }
                if (currentDepth > maxDepth) {
                    maxDepth = currentDepth;
                    deepestLine = i + 1;
                }
            }
            if (maxDepth > MAX_NESTING) {
                findings.push({
                    severity: 'MEDIUM', id: 'COMPLEXITY_DEEP_NESTING',
                    cat: 'complexity',
                    desc: `Deep nesting detected: ${maxDepth} levels (max recommended: ${MAX_NESTING})`,
                    file: relFile, line: deepestLine
                });
            }

            // Check 3: eval/exec density
            const evalPattern = /\b(?:eval|exec|execSync|spawn|Function)\s*\(/g;
            const evalMatches = content.match(evalPattern) || [];
            const density = lines.length > 0 ? evalMatches.length / lines.length : 0;
            if (density > MAX_EVAL_DENSITY && evalMatches.length >= 3) {
                findings.push({
                    severity: 'HIGH', id: 'COMPLEXITY_EVAL_DENSITY',
                    cat: 'complexity',
                    desc: `High eval/exec density: ${evalMatches.length} calls in ${lines.length} lines (${(density * 100).toFixed(1)}%)`,
                    file: relFile
                });
            }
        }
    }

    // ── v1.1: Config Impact Analysis ──
    // Detects modifications to openclaw.json and dangerous configuration changes
    checkConfigImpact(skillPath, skillName, findings) {
        const files = this.getFiles(skillPath);

        for (const file of files) {
            const ext = path.extname(file).toLowerCase();
            if (!CODE_EXTENSIONS.has(ext) && ext !== '.json') continue;

            const relFile = path.relative(skillPath, file);
            if (relFile.includes('node_modules') || relFile.startsWith('.git')) continue;

            let content;
            try { content = fs.readFileSync(file, 'utf-8'); } catch { continue; }

            // Check 1: openclaw.json reference + write operation in same file
            // Handles both direct and variable-based patterns (e.g. writeFileSync(configPath))
            const hasConfigRef = /openclaw\.json/i.test(content);
            const hasWriteOp = /(?:writeFileSync|writeFile|fs\.write)\s*\(/i.test(content);
            if (hasConfigRef && hasWriteOp) {
                // Find the write line for location info
                const clines = content.split('\n');
                let writeLine = 0;
                for (let i = 0; i < clines.length; i++) {
                    if (/(?:writeFileSync|writeFile|fs\.write)\s*\(/i.test(clines[i])) {
                        writeLine = i + 1;
                        break;
                    }
                }
                findings.push({
                    severity: 'CRITICAL', id: 'CFG_WRITE_DETECTED',
                    cat: 'config-impact',
                    desc: 'Code writes to openclaw.json',
                    file: relFile, line: writeLine,
                    sample: writeLine > 0 ? clines[writeLine - 1].trim().substring(0, 80) : ''
                });
            }

            // Check 2: Dangerous config key modifications
            const DANGEROUS_CONFIG_KEYS = [
                { regex: /exec\.approvals?\s*[:=]\s*['"]?(off|false|disabled|none)/gi, id: 'CFG_EXEC_APPROVAL_OFF', desc: 'Disables exec approval requirement', severity: 'CRITICAL' },
                { regex: /tools\.exec\.host\s*[:=]\s*['"]gateway['"]/gi, id: 'CFG_EXEC_HOST_GATEWAY', desc: 'Sets exec host to gateway (bypasses sandbox)', severity: 'CRITICAL' },
                { regex: /hooks\s*\.\s*internal\s*\.\s*entries\s*[:=]/gi, id: 'CFG_HOOKS_INTERNAL', desc: 'Modifies internal hook entries', severity: 'HIGH' },
                { regex: /network\.allowedDomains\s*[:=]\s*\[?\s*['"]\*['"]/gi, id: 'CFG_NET_WILDCARD', desc: 'Sets network allowedDomains to wildcard', severity: 'HIGH' },
            ];

            for (const check of DANGEROUS_CONFIG_KEYS) {
                check.regex.lastIndex = 0;
                if (check.regex.test(content)) {
                    findings.push({
                        severity: check.severity, id: check.id,
                        cat: 'config-impact',
                        desc: check.desc,
                        file: relFile
                    });
                }
            }
        }
    }

    checkHiddenFiles(skillPath, skillName, findings) {
        try {
            const entries = fs.readdirSync(skillPath);
            for (const entry of entries) {
                if (entry.startsWith('.') && entry !== '.guard-scanner-ignore' && entry !== '.guava-guard-ignore' && entry !== '.gitignore' && entry !== '.git') {
                    const fullPath = path.join(skillPath, entry);
                    const stat = fs.statSync(fullPath);
                    if (stat.isFile()) {
                        const ext = path.extname(entry).toLowerCase();
                        if (CODE_EXTENSIONS.has(ext) || ext === '' || ext === '.sh') {
                            findings.push({ severity: 'MEDIUM', id: 'STRUCT_HIDDEN_EXEC', cat: 'structural', desc: `Hidden executable file: ${entry}`, file: entry });
                        }
                    } else if (stat.isDirectory() && entry !== '.git') {
                        findings.push({ severity: 'LOW', id: 'STRUCT_HIDDEN_DIR', cat: 'structural', desc: `Hidden directory: ${entry}/`, file: entry });
                    }
                }
            }
        } catch { }
    }

    checkJSDataFlow(content, relFile, findings) {
        // v9: Pseudo-AST Semantic Unfurling & Alias Tracking
        // 1. Resolve string concatenations (e.g., '"f" + "etch"' -> '"fetch"')
        let unfurledContent = content.replace(/(["'`])([^"'`]*)\1\s*\+\s*(["'`])([^"'`]*)\3/g, '$1$2$4$1');
        for (let i = 0; i < 3; i++) { // Deep unfurl (up to 3 concats)
            unfurledContent = unfurledContent.replace(/(["'`])([^"'`]*)\1\s*\+\s*(["'`])([^"'`]*)\3/g, '$1$2$4$1');
        }

        const lines = unfurledContent.split('\n');
        const imports = new Map();
        const sensitiveReads = [];
        const networkCalls = [];
        const execCalls = [];

        // Alias Tracker for Sinks & Vars
        const activeAliases = {
            network: ['fetch', 'axios', 'request', 'http.request', 'https.request', 'got'],
            exec: ['exec', 'execSync', 'spawn', 'spawnSync', 'execFile', "require('child_process').execSync"],
            fsRead: ['readFileSync', 'readFile', 'fs.readFileSync', 'fs.readFile', "require('fs').readFileSync"]
        };
        const stringVars = new Map();

        const registerAlias = (alias, target) => {
            if (!alias || !target) return;
            for (const [key, sinks] of Object.entries(activeAliases)) {
                if (sinks.some(s => target.includes(s) || s.includes(target))) {
                    activeAliases[key].push(alias);
                }
            }
        };

        // Pass 1: Extract Context & Aliases & Values
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            // Standard variable assignment: const getRemote = fetch;
            const aliasMatch = line.match(/(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*([a-zA-Z0-9_$.]+(?:\([^)]*\))?)\s*;/);
            if (aliasMatch) {
                registerAlias(aliasMatch[1], aliasMatch[2]);
            }

            // String literals: const target = ".env";
            const strMatch = line.match(/(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(["'`])([^"'`]+)\2/);
            if (strMatch) {
                stringVars.set(strMatch[1], strMatch[3]); // target -> .env
            }

            // Require assignments: const fs = require('fs')
            const reqMatch = line.match(/(?:const|let|var)\s+(?:{[^}]+}|\w+)\s*=\s*require\s*\(\s*['"]([^'"]+)['"]\s*\)/);
            if (reqMatch) {
                const varMatch = line.match(/(?:const|let|var)\s+({[^}]+}|\w+)/);
                if (varMatch) {
                    const aliasName = varMatch[1].trim();
                    imports.set(aliasName, reqMatch[1]);
                    registerAlias(`${aliasName}.readFileSync`, 'readFileSync'); // Link fs methods
                    registerAlias(`${aliasName}.readFile`, 'readFile');
                    registerAlias(`${aliasName}.exec`, 'exec');
                    registerAlias(`${aliasName}.execSync`, 'execSync');
                }
            }
        }

        // Helper to create safe regex from dynamic aliases
        const escapeRegex = (arr) => arr.map(a => a.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')).join('|');

        // Pass 2: Data Flow Matching with Interpolation
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const lineNum = i + 1;

            // Pseudo-AST: substitute known literal vars into the line to reveal logic
            let resolvedLine = line;
            for (const [k, v] of stringVars.entries()) {
                // replace var usage but only for whole words
                resolvedLine = resolvedLine.replace(new RegExp(`\\b${k}\\b`, 'g'), `"${v}"`);
            }

            const fsPattern = new RegExp(`(?:${escapeRegex(activeAliases.fsRead)})\\s*\\([^)]*(?:\\.env|\\.ssh|id_rsa|\\.clawdbot|\\.openclaw(?!\\/workspace))`, 'i');
            if (fsPattern.test(resolvedLine)) {
                sensitiveReads.push({ line: lineNum, text: resolvedLine.trim() });
            }
            if (/process\.env\.[A-Z_]*(?:KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)/i.test(resolvedLine)) {
                sensitiveReads.push({ line: lineNum, text: resolvedLine.trim() });
            }

            const netPattern = new RegExp(`(?:${escapeRegex(activeAliases.network)})\\s*\\(`, 'i');
            if (netPattern.test(resolvedLine) || /\.post\s*\(|\.put\s*\(|\.patch\s*\(/.test(resolvedLine)) {
                networkCalls.push({ line: lineNum, text: resolvedLine.trim() });
            }

            const execPattern = new RegExp(`(?:${escapeRegex(activeAliases.exec)})\\s*\\(`, 'i');
            if (execPattern.test(resolvedLine)) {
                execCalls.push({ line: lineNum, text: resolvedLine.trim() });
            }
        }

        if (sensitiveReads.length > 0 && networkCalls.length > 0) {
            findings.push({
                severity: 'CRITICAL', id: 'AST_CRED_TO_NET', cat: 'data-flow',
                desc: `Data flow: secret read (L${sensitiveReads[0].line}) → network call (L${networkCalls[0].line})`,
                file: relFile, line: sensitiveReads[0].line,
                sample: sensitiveReads[0].text.substring(0, 60)
            });
        }

        if (sensitiveReads.length > 0 && execCalls.length > 0) {
            findings.push({
                severity: 'HIGH', id: 'AST_CRED_TO_EXEC', cat: 'data-flow',
                desc: `Data flow: secret read (L${sensitiveReads[0].line}) → command exec (L${execCalls[0].line})`,
                file: relFile, line: sensitiveReads[0].line,
                sample: sensitiveReads[0].text.substring(0, 60)
            });
        }

        const importedModules = new Set([...imports.values()]);
        if (importedModules.has('child_process') && (importedModules.has('https') || importedModules.has('http') || importedModules.has('node-fetch'))) {
            findings.push({ severity: 'HIGH', id: 'AST_SUSPICIOUS_IMPORTS', cat: 'data-flow', desc: 'Suspicious import combination: child_process + network module', file: relFile });
        }
        if (importedModules.has('fs') && importedModules.has('child_process') && (importedModules.has('https') || importedModules.has('http'))) {
            findings.push({ severity: 'CRITICAL', id: 'AST_EXFIL_TRIFECTA', cat: 'data-flow', desc: 'Exfiltration trifecta: fs + child_process + network', file: relFile });
        }

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (/`[^`]*\$\{.*(?:env|key|token|secret|password).*\}[^`]*`\s*(?:\)|,)/i.test(line) &&
                /(?:fetch|request|axios|http|url)/i.test(line)) {
                findings.push({ severity: 'CRITICAL', id: 'AST_SECRET_IN_URL', cat: 'data-flow', desc: 'Secret interpolated into URL/request', file: relFile, line: i + 1, sample: line.trim().substring(0, 80) });
            }
        }
    }

    checkCrossFile(skillPath, skillName, findings) {
        const files = this.getFiles(skillPath);
        const allContent = {};

        for (const file of files) {
            const ext = path.extname(file).toLowerCase();
            if (BINARY_EXTENSIONS.has(ext)) continue;
            const relFile = path.relative(skillPath, file);
            if (relFile.includes('node_modules') || relFile.startsWith('.git')) continue;
            try {
                const content = fs.readFileSync(file, 'utf-8');
                if (content.length < 500000) allContent[relFile] = content;
            } catch { }
        }

        const skillMd = allContent['SKILL.md'] || '';
        const codeFileRefs = skillMd.match(/(?:(?:\.\.\/)+|\.\/)?(?:[a-zA-Z0-9_\-]+\/)*[a-zA-Z0-9_\-.]+\.(js|py|sh|ts)/gi) || [];
        for (const ref of codeFileRefs) {
            const cleanRef = ref.trim();
            const normalizedRef = cleanRef.replace(/^\.\//, '');
            const resolvedRef = path.normalize(path.resolve(skillPath, cleanRef));
            const insideSkillRef = path.normalize(path.join(skillPath, normalizedRef));
            const exists = fs.existsSync(resolvedRef)
                || fs.existsSync(insideSkillRef)
                || !!allContent[normalizedRef]
                || files.some(f => path.normalize(f) === resolvedRef || path.relative(skillPath, f) === normalizedRef);
            if (!exists) {
                findings.push({ severity: 'MEDIUM', id: 'XFILE_PHANTOM_REF', cat: 'structural', desc: `SKILL.md references non-existent file: ${cleanRef}`, file: 'SKILL.md' });
            }
        }

        const base64Fragments = [];
        for (const [file, content] of Object.entries(allContent)) {
            const matches = content.match(/[A-Za-z0-9+/]{20,}={0,2}/g) || [];
            for (const m of matches) {
                if (m.length > 40) base64Fragments.push({ file, fragment: m.substring(0, 30) });
            }
        }
        if (base64Fragments.length > 3 && new Set(base64Fragments.map(f => f.file)).size > 1) {
            findings.push({ severity: 'HIGH', id: 'XFILE_FRAGMENT_B64', cat: 'obfuscation', desc: `Base64 fragments across ${new Set(base64Fragments.map(f => f.file)).size} files`, file: skillName });
        }

        if (/(?:read|load|source|import)\s+(?:the\s+)?(?:script|file|code)\s+(?:from|at|in)\s+(?:scripts?\/)/gi.test(skillMd)) {
            const hasExec = Object.values(allContent).some(c => /(?:eval|exec|spawn)\s*\(/i.test(c));
            if (hasExec) {
                findings.push({ severity: 'MEDIUM', id: 'XFILE_LOAD_EXEC', cat: 'data-flow', desc: 'SKILL.md references script files that contain exec/eval', file: 'SKILL.md' });
            }
        }
    }

    checkRuntimeIntegration(skillPath, skillName, findings) {
        const runtimeModules = [
            {
                rel: path.join('rust', 'guard-scan-core', 'src', 'memory_integrity.rs'),
                id: 'RUNTIME_MEMORY_INTEGRITY_MODULE',
                desc: 'Runtime behavior: Rust memory_integrity module is wired into the v16 pipeline',
                owasp_asi: ['ASI06'],
            },
            {
                rel: path.join('rust', 'guard-scan-core', 'src', 'soul_hard_gate.rs'),
                id: 'RUNTIME_SOUL_HARD_GATE_MODULE',
                desc: 'Runtime behavior: Rust soul_hard_gate module is wired into the v16 pipeline',
                owasp_asi: ['ASI10'],
            },
        ];

        for (const module of runtimeModules) {
            const abs = path.join(skillPath, module.rel);
            if (!fs.existsSync(abs)) continue;
            this.pushUniqueFinding(findings, {
                id: module.id,
                severity: 'LOW',
                cat: 'runtime-guard',
                desc: module.desc,
                file: module.rel,
                layer: 3,
                owasp_asi: module.owasp_asi,
                protocol_surface: ['session-boundary'],
            });
        }
    }

    calculateRisk(findings) {
        return calculateRisk(findings);
    }

    getVerdict(risk) {
        return getVerdict(risk, this.thresholds);
    }

    getFiles(dir) {
        return getFiles(dir);
    }

    printSummary() {
        return printSummary(this.stats, VERSION);
    }

    toJSON() {
        return toJSONReport(this, VERSION);
    }

    toSARIF(scanDir) {
        return toSARIFReport(this, VERSION, scanDir);
    }

    toHTML() {
        return toHTMLReport(this, VERSION);
    }

    /**
     * Generate a Threat Model based on the scan findings.
     * @param {Array<Object>} findings - The array of findings from the scan.
     * @returns {Object} The generated threat model.
     */

    /**
     * Check AST for contextual validation of high-risk chains.
     * Separates heuristic-only matches from validated chains.
     */
    checkASTValidation(content, relFile, findings) {
        return checkASTValidation(content, relFile, findings);
    }

    appendThreatModelFindings(content, findings, relFile = 'threat-model') {
        if (!content || typeof content !== 'string') return;
        const model = generateModel(content);
        for (const risk of model.compounded_risks || []) {
            if (!['compound.fs_read_network', 'compound.env_access_network'].includes(risk.id)) {
                continue;
            }
            this.pushUniqueFinding(findings, {
                id: `TM_${risk.id.split('.').pop().toUpperCase()}`,
                severity: risk.severity,
                cat: 'agent-protocol',
                desc: `Threat model: ${risk.description}`,
                file: relFile,
                rationale: risk.description,
                preconditions: 'Multiple risky capabilities must coexist in the same code path.',
                false_positive_scenarios: [
                    'The capabilities are present in isolated branches that cannot compose.',
                    'The code sample documents a risky pattern without executing it.',
                ],
                remediation_hint: 'Separate the capabilities across reviewed boundaries or remove the risky coupling.',
                validation_status: 'validated',
                validation_state: 'semantic-match',
                confidence: 0.9,
                protocol_surface: ['credential-flow'],
                owasp_asi: ['ASI02', 'ASI07'],
                layer: 2,
                sample: risk.contributing_capabilities.join(', '),
            });
        }
        if (!model.lethal_trifecta?.triggered) return;

        this.pushUniqueFinding(findings, {
            id: 'TM_LETHAL_TRIFECTA',
            severity: 'CRITICAL',
            cat: 'agent-protocol',
            desc: 'Threat model: lethal trifecta detected (private data + untrusted input + external communication)',
            file: relFile,
            rationale: model.lethal_trifecta.rationale,
            preconditions: 'A code path combines private-data access, attacker-influenced input, and outbound communication in the same execution surface.',
            false_positive_scenarios: [
                'The file is documenting an unsafe architecture without implementing it.',
                'The capabilities appear in separate unreachable branches that do not compose at runtime.',
            ],
            remediation_hint: 'Split trust boundaries, isolate private data access, and require explicit mediation before any outbound communication.',
            validation_status: 'validated',
            validation_state: 'semantic-match',
            confidence: 0.97,
            protocol_surface: ['credential-flow', 'session-boundary'],
            owasp_asi: ['ASI02', 'ASI07'],
            layer: 2,
            sample: model.summary,
        });
    }

    generateThreatModel(findings) {
        const derivedContent = this.threatModelInputs.join('\n')
            || findings.map((f) => [f.id, f.desc, f.sample, f.file].filter(Boolean).join(' ')).join('\n');
        const model = generateModel(derivedContent);
        const surface = {
            network: false,
            file_system: false,
            code_execution: false,
            credential_exposure: false,
            external_ingestion: false,
            persistence: false
        };
        const owasp = new Set();
        const protocolSurfaces = new Set();
        const layerSeen = new Map();

        for (const f of findings) {
            // Map pattern IDs or categories to capability surfaces
            const id = f.id || '';
            const cat = f.cat || '';
            const desc = (f.desc || '').toLowerCase();
            
            if (id.includes('FETCH') || id.includes('CURL') || id.includes('SSRF') || id.includes('NETWORK') || id.includes('EXFIL') || id.includes('TRUST_WEB_EXEC') || desc.includes('fetch') || desc.includes('network') || desc.includes('web content')) {
                surface.network = true;
            }
            if (id.includes('FS_') || id.includes('WRITE') || id.includes('READ') || id.includes('FILE') || id.includes('TRUST_WEB_EXEC') || desc.includes('file system') || desc.includes('readfilesync') || desc.includes('fs.read')) {
                surface.file_system = true;
            }
            if (id.includes('EXEC') || id.includes('EVAL') || id.includes('SHELL') || id.includes('SPAWN') || id.includes('RCE') || desc.includes('exec') || desc.includes('shell')) {
                surface.code_execution = true;
            }
            if (id.includes('CRED') || id.includes('KEY') || id.includes('SECRET') || id.includes('TOKEN') || cat.includes('credential') || desc.includes('credential') || desc.includes('trust boundary')) {
                surface.credential_exposure = true;
            }
            if (id.includes('PI_') || id.includes('PROMPT_INJECT') || id.includes('POISON') || id.includes('TRUST_WEB_EXEC') || cat.includes('prompt-injection') || desc.includes('ignore all')) {
                surface.external_ingestion = true;
            }
            if (id.includes('PERSIST') || id.includes('CRON') || id.includes('STARTUP') || cat.includes('persistence') || desc.includes('cron') || id.includes('DEPS_PHANTOM_IMPORT')) {
                surface.persistence = true;
            }
            for (const asi of f.owasp_asi || []) owasp.add(asi);
            for (const protocol of f.protocol_surface || []) protocolSurfaces.add(protocol);
            const layer = f.layer || 1;
            layerSeen.set(layer, f.layer_name || inferFindingContext(f).layer_name);
        }

        const lethalTrifecta = model.lethal_trifecta?.triggered || (
            surface.network &&
            (surface.file_system || surface.credential_exposure) &&
            surface.external_ingestion
        )
            ? {
                triggered: true,
                severity: 'CRITICAL',
                contributing_capabilities: ['private_data_access', 'untrusted_input', 'external_communication'],
                rationale: 'The inferred threat surface combines private data access, untrusted input, and outbound communication.',
            }
            : model.lethal_trifecta;

        return {
            timestamp: new Date().toISOString(),
            surface,
            capabilities: model.capabilities,
            compounded_risks: model.compounded_risks,
            lethal_trifecta: lethalTrifecta,
            summary: Object.keys(surface).filter(k => surface[k]).join(', ') || 'none',
            owasp_asi: [...owasp].sort(),
            protocol_surfaces: [...protocolSurfaces].sort(),
            layer_summary: [...layerSeen.entries()].sort((a, b) => a[0] - b[0]).map(([layer, layer_name]) => ({ layer, layer_name })),
        };
    }

    generatePopulationMonitor() {
        if (!Array.isArray(this.populationEvents) || this.populationEvents.length === 0) return null;
        return analyzePopulationMonitor(this.populationEvents);
    }

    generateMetaGuard() {
        if (!this.metaGuardInput) return null;
        return analyzeMetaGuard(this.metaGuardInput);
    }

}

import { scanToolCall, RUNTIME_CHECKS, getCheckStats, LAYER_NAMES  } from './runtime-guard';

export {  GuardScanner, VERSION, THRESHOLDS, SEVERITY_WEIGHTS, scanToolCall, RUNTIME_CHECKS, getCheckStats, LAYER_NAMES  };
