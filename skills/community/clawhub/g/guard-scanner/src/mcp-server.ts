// @ts-nocheck
/**
 * guard-scanner MCP Server — Lightweight stdio JSON-RPC 2.0
 *
 * @security-manifest
 *   env-read: [VT_API_KEY (optional, for audit vt-scan)]
 *   env-write: []
 *   network: [npm registry, GitHub API, VirusTotal API — only for audit_assets]
 *   fs-read: [scan target directories, openclaw config]
 *   fs-write: [~/.openclaw/guard-scanner/audit.jsonl]
 *   exec: none
 *   purpose: MCP server exposing guard-scanner static/runtime analysis over stdio
 *
 * Protocol: MCP (Model Context Protocol) over stdio transport
 * Implements: initialize, tools/list, tools/call, notifications
 *
 * Tools:
 *   scan_skill      — Scan a directory for security threats
 *   scan_text       — Scan a code/text snippet inline
 *   check_tool_call — Runtime check before a tool call (26 checks, 5 layers)
 *   audit_assets    — Audit npm/GitHub/ClawHub assets for exposure
 *   get_stats       — Get scanner capabilities and statistics
 *
 * @author Guava 🍈 & Dee
 * @license MIT
 */

import { GuardScanner, VERSION, scanToolCall, getCheckStats, LAYER_NAMES  } from './scanner';
import { AssetAuditor, AUDIT_VERSION  } from './asset-auditor';
import { normalizeFinding  } from './finding-schema';
import fs  from 'fs';
import path  from 'path';
import os  from 'os';
import CAPABILITIES  from '../docs/spec/capabilities.json';
import QUALITY_CONTRACT  from '../docs/data/quality-contract.json';

// ── MCP Protocol Constants ──

const JSONRPC = '2.0';
const MCP_VERSION = '2025-11-05';

const SERVER_INFO = {
    name: 'guard-scanner',
    version: VERSION,
};

const SERVER_CAPABILITIES = {
    tools: {},
};

const STATIC_SUMMARY = `${CAPABILITIES.static_pattern_count} threat patterns across ${CAPABILITIES.threat_category_count} categories`;

// ── Async Task Store (run_async / status / result / cancel) ──

const TASK_DIR = process.env.GUARD_SCANNER_TASK_DIR || path.join(os.homedir(), '.openclaw', 'guard-scanner', 'tasks');
const TASK_FILE = path.join(TASK_DIR, 'tasks.json');

function ensureTaskStore() {
    fs.mkdirSync(TASK_DIR, { recursive: true });
    if (!fs.existsSync(TASK_FILE)) fs.writeFileSync(TASK_FILE, '{}');
}

function loadTasks() {
    ensureTaskStore();
    try {
        return JSON.parse(fs.readFileSync(TASK_FILE, 'utf8') || '{}');
    } catch {
        return {};
    }
}

function saveTasks(tasks) {
    ensureTaskStore();
    fs.writeFileSync(TASK_FILE, JSON.stringify(tasks, null, 2));
}

function makeTaskId() {
    return `task_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
}

function nowIso() {
    return new Date().toISOString();
}

function runTaskAsync(taskId, toolName, toolArgs) {
    setImmediate(async () => {
        const tasks = loadTasks();
        const t = tasks[taskId];
        if (!t || t.state === 'cancelled') return;

        t.state = 'running';
        t.startedAt = nowIso();
        t.updatedAt = nowIso();
        saveTasks(tasks);

        try {
            let result;
            if (toolName === 'scan_skill') result = handleScanSkill(toolArgs);
            else if (toolName === 'scan_text') result = handleScanText(toolArgs);
            else if (toolName === 'check_tool_call') result = handleCheckToolCall(toolArgs);
            else if (toolName === 'audit_assets') result = await handleAuditAssets(toolArgs);
            else if (toolName === 'get_stats') result = handleGetStats(toolArgs);
            else throw new Error(`Unsupported async tool: ${toolName}`);

            const latest = loadTasks();
            if (!latest[taskId] || latest[taskId].state === 'cancelled') return;
            latest[taskId].state = result?.isError ? 'failed' : 'succeeded';
            latest[taskId].updatedAt = nowIso();
            latest[taskId].finishedAt = nowIso();
            latest[taskId].result = result;
            saveTasks(latest);
        } catch (e) {
            const latest = loadTasks();
            if (!latest[taskId]) return;
            latest[taskId].state = 'failed';
            latest[taskId].updatedAt = nowIso();
            latest[taskId].finishedAt = nowIso();
            latest[taskId].error = e.message;
            saveTasks(latest);
        }
    });
}

// ── Tool Definitions ──

const TOOLS = [
    {
        name: 'scan_skill',
        description: `Scan a directory for agent security threats. Detects prompt injection, data exfiltration, credential theft, reverse shells, and ${STATIC_SUMMARY}. Returns risk score, verdict, and detailed findings.`,
        inputSchema: {
            type: 'object',
            properties: {
                path: {
                    type: 'string',
                    description: 'Absolute path to the directory to scan',
                },
                verbose: {
                    type: 'boolean',
                    description: 'Include detailed finding samples',
                    default: false,
                },
                strict: {
                    type: 'boolean',
                    description: 'Lower detection thresholds (more sensitive)',
                    default: false,
                },
                compliance: {
                    type: 'string',
                    enum: ['owasp-asi'],
                    description: 'Optional compliance projection. Filters output to findings mapped to OWASP ASI.',
                },
            },
            required: ['path'],
        },
    },
    {
        name: 'scan_text',
        description: 'Scan a code or text snippet for security threats inline. Useful for checking generated code, tool descriptions, or agent prompts before execution. Returns matched patterns with severity levels.',
        inputSchema: {
            type: 'object',
            properties: {
                text: {
                    type: 'string',
                    description: 'The code or text content to scan',
                },
                filename: {
                    type: 'string',
                    description: 'Optional filename hint for file-type detection (e.g. "script")',
                    default: 'snippet.txt',
                },
                compliance: {
                    type: 'string',
                    enum: ['owasp-asi'],
                    description: 'Optional compliance projection. Filters output to findings mapped to OWASP ASI.',
                },
            },
            required: ['text'],
        },
    },
    {
        name: 'check_tool_call',
        description: 'Runtime security check for an agent tool call (before_tool_call equivalent). Checks 26 threat patterns across 5 layers: Threat Detection, Trust Defense, Safety Judge, Brain/Behavioral, Trust Exploitation. Returns whether the call should be blocked.',
        inputSchema: {
            type: 'object',
            properties: {
                tool: {
                    type: 'string',
                    description: 'Name of the tool being called (e.g. "exec", "write", "shell")',
                },
                args: {
                    type: 'object',
                    description: 'Arguments/parameters of the tool call',
                    additionalProperties: true,
                },
                mode: {
                    type: 'string',
                    enum: ['monitor', 'enforce', 'strict'],
                    description: 'Guard mode — monitor: log only, enforce: block CRITICAL (default), strict: block HIGH+CRITICAL',
                    default: 'enforce',
                },
                policy: {
                    type: 'object',
                    description: 'Optional capability-scoped runtime policy contract',
                    additionalProperties: false,
                    properties: {
                        id: { type: 'string' },
                        allowed_tools: { type: 'array', items: { type: 'string' } },
                        blocked_tools: { type: 'array', items: { type: 'string' } },
                        max_network_scope: { type: 'string', enum: ['none', 'internal-only', 'external-ok'] },
                        secret_bearing_context: { type: 'boolean' },
                        memory_write_permission: { type: 'boolean' },
                    },
                },
            },
            required: ['tool', 'args'],
        },
    },
    {
        name: 'audit_assets',
        description: 'Audit npm packages or GitHub repositories for security exposure. Checks for accidental source leaks, overly permissive access, and supply chain risks.',
        inputSchema: {
            type: 'object',
            properties: {
                username: {
                    type: 'string',
                    description: 'npm or GitHub username to audit',
                },
                scope: {
                    type: 'string',
                    enum: ['npm', 'github', 'all'],
                    description: 'What to audit — npm packages, GitHub repos, or all',
                    default: 'all',
                },
            },
            required: ['username'],
        },
    },
    {
        name: 'get_stats',
        description: 'Get guard-scanner capabilities, version, and detection statistics. Returns pattern counts, runtime check counts by layer and severity, supported categories, and configuration.',
        inputSchema: {
            type: 'object',
            properties: {},
        },
    },
    {
        name: 'experimental.run_async',
        description: '[Experimental] Run a supported guard-scanner tool asynchronously. Returns taskId immediately; use experimental.task_status/experimental.task_result to retrieve output.',
        inputSchema: {
            type: 'object',
            properties: {
                tool: { type: 'string', enum: ['scan_skill', 'scan_text', 'check_tool_call', 'audit_assets', 'get_stats'] },
                args: { type: 'object', additionalProperties: true, default: {} },
            },
            required: ['tool'],
        },
    },
    {
        name: 'experimental.task_status',
        description: '[Experimental] Get async task status by taskId.',
        inputSchema: {
            type: 'object',
            properties: { taskId: { type: 'string' } },
            required: ['taskId'],
        },
    },
    {
        name: 'experimental.task_result',
        description: '[Experimental] Get async task final result by taskId.',
        inputSchema: {
            type: 'object',
            properties: { taskId: { type: 'string' } },
            required: ['taskId'],
        },
    },
    {
        name: 'experimental.task_cancel',
        description: '[Experimental] Cancel async task by taskId (best-effort).',
        inputSchema: {
            type: 'object',
            properties: { taskId: { type: 'string' }, reason: { type: 'string' } },
            required: ['taskId'],
        },
    },
];

// NOTE: cron_glm5_config was removed in v14.0.0 — not guard-scanner's responsibility

// ── Tool Handlers ──

function handleScanSkill({ path: scanPath, verbose = false, strict = false, compliance = null }) {
    if (!scanPath) return errorResult('path is required');

    if (!fs.existsSync(scanPath)) {
        return errorResult(`Directory not found: ${scanPath}`);
    }
    if (!fs.statSync(scanPath).isDirectory()) {
        return errorResult(`Not a directory: ${scanPath}`);
    }

    const scanner = new GuardScanner({ verbose, strict, quiet: true, compliance });
    scanner.scanDirectory(scanPath);
    const report = scanner.toJSON();

    // Count findings by severity
    let critical = 0, high = 0, medium = 0, low = 0, total = 0;
    for (const skill of report.findings) {
        for (const f of skill.findings) {
            total++;
            if (f.severity === 'CRITICAL') critical++;
            else if (f.severity === 'HIGH') high++;
            else if (f.severity === 'MEDIUM') medium++;
            else low++;
        }
    }

    const verdict = report.stats.malicious > 0 ? '🔴 MALICIOUS'
        : report.stats.suspicious > 0 ? '🟡 SUSPICIOUS'
            : '🟢 SAFE';

    return successResult(
        `🛡️ Scan: ${verdict}\n` +
        `Files: ${report.stats.scanned}, Skills: ${report.findings.length}\n` +
        `Compliance: ${report.compliance_mode || 'default'}\n` +
        `Clean: ${report.stats.clean}, Suspicious: ${report.stats.suspicious}, Malicious: ${report.stats.malicious}\n` +
        `Findings: ${total} (Critical: ${critical}, High: ${high}, Medium: ${medium}, Low: ${low})\n` +
        `Layers: ${report.layer_summary?.map((layer) => `L${layer.layer}=${layer.count}`).join(', ') || 'none'}\n` +
        `OWASP ASI: ${report.owasp_asi_coverage?.map((entry) => entry.id).join(', ') || 'none'}\n` +
        (total > 0
            ? '\nTop findings:\n' + report.findings.flatMap(s =>
                s.findings.slice(0, 5).map(f =>
                    `  [${f.severity}] ${f.id}: ${f.desc} — ${s.skill}/${f.file} (${f.layer_name || `L${f.layer}`})`
                )
            ).slice(0, 10).join('\n')
            : '\n✅ No threats detected.')
    );
}

function handleScanText({ text, filename = 'snippet.txt', compliance = null }) {
    if (!text) return errorResult('text is required');
    const scanner = new GuardScanner({ quiet: true, compliance });
    const report = scanner.scanText(text);
    const detections = report.detections.map((finding) => normalizeFinding(finding, { source: 'static' }));
    const filtered = compliance === 'owasp-asi'
        ? detections.filter((finding) => finding.owasp_asi?.length > 0)
        : detections;
    const highest = filtered[0]?.severity || 'LOW';

    return successResult(
        `🛡️ Text Scan: ${filtered.length > 0 ? '⚠️ FINDINGS' : '🟢 CLEAN'}\n` +
        `Filename: ${filename}\n` +
        `Compliance: ${compliance || 'default'}\n` +
        `Score: ${report.risk}\n` +
        `Findings: ${filtered.length} (highest: ${highest})\n` +
        (filtered.length > 0
            ? '\nDetected:\n' + filtered.map(f =>
                `  [${f.severity}] ${f.id}: ${f.desc} (${f.layer_name || `L${f.layer}`}${f.owasp_asi?.length ? ` | ${f.owasp_asi.join(',')}` : ''})`
            ).join('\n')
            : '\n✅ No threats detected.')
    );
}

function handleCheckToolCall({ tool, args, mode = 'enforce', policy }) {
    if (!tool) return errorResult('tool is required');
    if (args === undefined) return errorResult('args is required');

    const result = scanToolCall(tool, args, { mode, auditLog: true, policy });
    const runtimeCheckCount = getCheckStats().total;

    if (result.detections.length === 0) {
        return successResult(
            `✅ Tool call "${tool}" passed all ${runtimeCheckCount} runtime checks.\nMode: ${mode}\nPolicy: ${result.matchedPolicyId || 'none'}`
        );
    }

    const lines = result.detections.map(d =>
        `  [${d.action.toUpperCase()}] ${d.id} (${d.severity}${d.layer ? `, L${d.layer}` : ''}): ${d.desc}`
    );

    return successResult(
        `🛡️ Runtime Check: ${result.blocked ? '🚫 BLOCKED' : '⚠️ WARNINGS'}\n` +
        `Tool: ${tool} | Mode: ${mode}\n` +
        `Policy: ${result.matchedPolicyId || 'none'}\n` +
        `Detections: ${result.detections.length}\n\n` +
        lines.join('\n') +
        (result.riskAmplificationReasons.length > 0 ? `\n\nAmplification:\n  - ${result.riskAmplificationReasons.join('\n  - ')}` : '') +
        (result.policyRationale ? `\n\nPolicy rationale: ${result.policyRationale}` : '') +
        (result.remediationSuggestion ? `\nRemediation: ${result.remediationSuggestion}` : '') +
        (result.blocked ? `\n\n❌ Blocked: ${result.blockReason}` : '')
    );
}

async function handleAuditAssets({ username, scope = 'all' }) {
    if (!username) return errorResult('username is required');

    const auditor = new AssetAuditor({ quiet: true });

    try {
        if (scope === 'npm' || scope === 'all') {
            await auditor.auditNpm(username);
        }
        if (scope === 'github' || scope === 'all') {
            await auditor.auditGithub(username);
        }

        const report = auditor.toJSON();
        const verdict = auditor.getVerdict();

        return successResult(
            `🛡️ Asset Audit: ${verdict.label}\n` +
            `User: ${username} | Scope: ${scope}\n` +
            `Alerts: ${report.summary.totalAlerts} ` +
            `(Critical: ${report.summary.critical}, High: ${report.summary.high}, ` +
            `Medium: ${report.summary.medium}, Low: ${report.summary.low})\n` +
            (report.alerts.length > 0
                ? '\nAlerts:\n' + report.alerts.slice(0, 10).map(a =>
                    `  [${a.severity}] ${a.source}: ${a.message}`
                ).join('\n')
                : '\n✅ No exposure detected.')
        );
    } catch (e) {
        return errorResult(`Audit failed: ${e.message}`);
    }
}

function handleGetStats() {
    const runtimeStats = getCheckStats();
    const targets = CAPABILITIES.quality_targets || QUALITY_CONTRACT.quality_targets;

    return successResult(
        `🛡️ guard-scanner v${VERSION}\n\n` +
        `Static Analysis:\n` +
        `  • ${STATIC_SUMMARY}\n` +
        `  • 5-layer v16 pipeline: static, protocol, runtime, cognitive, threat intel\n` +
        `  • Entropy-based secret detection\n` +
        `  • Data flow analysis (JS)\n` +
        `  • Cross-file reference checking\n` +
        `  • SKILL.md manifest validation\n` +
        `  • Dependency chain scanning\n` +
        `  • SARIF, JSON, HTML reporting\n\n` +
        `Runtime Guard:\n` +
        `  • ${runtimeStats.total} checks across ${Object.keys(runtimeStats.byLayer).length} layers\n` +
        Object.entries(runtimeStats.byLayer).map(([l, c]) =>
            `  • Layer ${l} (${LAYER_NAMES[l] || 'Unknown'}): ${c} checks`
        ).join('\n') + '\n\n' +
        `Asset Audit: v${AUDIT_VERSION}\n` +
        `  • npm package exposure detection\n` +
        `  • GitHub repository scanning\n` +
        `  • ClawHub skill auditing\n\n` +
        `Quality Contract:\n` +
        `  • Benchmark corpus version: ${CAPABILITIES.benchmark_corpus_version || QUALITY_CONTRACT.benchmark_version}\n` +
        `  • Precision target: >= ${targets.precision_min}\n` +
        `  • Recall target: >= ${targets.recall_min}\n` +
        `  • FPR budget: <= ${targets.false_positive_rate_max}\n` +
        `  • FNR budget: <= ${targets.false_negative_rate_max}\n` +
        `  • Explainability completeness: ${CAPABILITIES.explainability_completeness_rate}\n` +
        `  • Runtime latency budget: ${CAPABILITIES.runtime_check_latency_budget_ms}ms\n\n` +
        `OWASP ASI Coverage:\n` +
        `  • ${(CAPABILITIES.owasp_asi_coverage || []).map((entry) => `${entry.id}=${entry.count}`).join(', ')}\n` +
        `  • Layers: ${(CAPABILITIES.analysis_layers || []).map((layer) => `L${layer.layer}:${layer.name}`).join(', ')}\n` +
        `  • Capability flags: protocol=${CAPABILITIES.capability_flags?.protocol_analysis ? 'yes' : 'no'}, runtime=${CAPABILITIES.capability_flags?.runtime_evidence ? 'yes' : 'no'}, cognitive=${CAPABILITIES.capability_flags?.cognitive_detection ? 'yes' : 'no'}\n\n` +
        `Performance: 0.016ms/scan average\n` +
        `Dependencies: 1 runtime (${CAPABILITIES.dependencies_runtime === 1 ? 'ws' : CAPABILITIES.dependencies_runtime})`
    );
}

function handleRunAsync({ tool, args = {} }) {
    if (!tool) return errorResult('tool is required');
    const supported = new Set(['scan_skill', 'scan_text', 'check_tool_call', 'audit_assets', 'get_stats']);
    if (!supported.has(tool)) return errorResult(`Unsupported async tool: ${tool}`);

    const taskId = makeTaskId();
    const tasks = loadTasks();
    tasks[taskId] = {
        taskId,
        tool,
        args,
        state: 'queued',
        createdAt: nowIso(),
        updatedAt: nowIso(),
    };
    saveTasks(tasks);
    runTaskAsync(taskId, tool, args);

    return successResult(`accepted\ntaskId=${taskId}\nstate=queued\npollAfterMs=800`);
}

function handleTaskStatus({ taskId }) {
    if (!taskId) return errorResult('taskId is required');
    const tasks = loadTasks();
    const t = tasks[taskId];
    if (!t) return errorResult(`Task not found: ${taskId}`);
    return successResult(`taskId=${taskId}\nstate=${t.state}\nupdatedAt=${t.updatedAt}`);
}

function handleTaskResult({ taskId }) {
    if (!taskId) return errorResult('taskId is required');
    const tasks = loadTasks();
    const t = tasks[taskId];
    if (!t) return errorResult(`Task not found: ${taskId}`);
    if (t.state === 'queued' || t.state === 'running') {
        return successResult(`taskId=${taskId}\nstate=${t.state}\nmessage=not ready`);
    }
    if (t.error) return errorResult(`taskId=${taskId}\nstate=${t.state}\nerror=${t.error}`);
    if (!t.result) return errorResult(`taskId=${taskId}\nstate=${t.state}\nerror=no result`);
    return t.result;
}

function handleTaskCancel({ taskId, reason = 'user cancel' }) {
    if (!taskId) return errorResult('taskId is required');
    const tasks = loadTasks();
    const t = tasks[taskId];
    if (!t) return errorResult(`Task not found: ${taskId}`);
    if (t.state === 'succeeded' || t.state === 'failed' || t.state === 'cancelled') {
        return successResult(`taskId=${taskId}\nstate=${t.state}\nmessage=already terminal`);
    }
    t.state = 'cancelled';
    t.updatedAt = nowIso();
    t.finishedAt = nowIso();
    t.cancelReason = reason;
    saveTasks(tasks);
    return successResult(`taskId=${taskId}\nstate=cancelled`);
}

// handleCronGlm5Config removed in v14.0.0 — not guard-scanner's responsibility

// ── Result helpers ──

function successResult(text) {
    return { content: [{ type: 'text', text }], isError: false };
}

function errorResult(text) {
    return { content: [{ type: 'text', text: `❌ ${text}` }], isError: true };
}

// ── MCP JSON-RPC over stdio ──

class MCPServer {
    constructor() {
        this._initialized = false;
        this._buffer = '';
    }

    start() {
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', (chunk) => this._onData(chunk));
        process.stdin.on('end', () => process.exit(0));
        process.stderr.write(`🛡️ guard-scanner MCP server v${VERSION} started\n`);
    }

    _onData(chunk) {
        this._buffer += chunk;

        // Parse newline-delimited JSON-RPC messages
        let newlineIdx;
        while ((newlineIdx = this._buffer.indexOf('\n')) !== -1) {
            const line = this._buffer.slice(0, newlineIdx).trim();
            this._buffer = this._buffer.slice(newlineIdx + 1);

            if (line.length === 0) continue;

            try {
                const msg = JSON.parse(line);
                this._handleMessage(msg);
            } catch (e) {
                // If parse fails, try Content-Length header protocol
                if (line.startsWith('Content-Length:')) {
                    this._handleContentLength(line);
                }
                // else ignore malformed input
            }
        }

        // Handle Content-Length based protocol (MCP stdio standard)
        this._tryParseContentLength();
    }

    _handleContentLength(headerLine) {
        // Already handled in _tryParseContentLength
    }

    _tryParseContentLength() {
        // MCP stdio: "Content-Length: N\r\n\r\n{json}"
        const clMatch = this._buffer.match(/Content-Length:\s*(\d+)\r?\n\r?\n/);
        if (!clMatch) return;

        const contentLength = parseInt(clMatch[1], 10);
        const headerEnd = clMatch.index + clMatch[0].length;
        const available = this._buffer.length - headerEnd;

        if (available < contentLength) return; // wait for more data

        const body = this._buffer.slice(headerEnd, headerEnd + contentLength);
        this._buffer = this._buffer.slice(headerEnd + contentLength);

        try {
            const msg = JSON.parse(body);
            this._handleMessage(msg);
        } catch { /* ignore */ }

        // Recurse for more messages
        this._tryParseContentLength();
    }

    async _handleMessage(msg) {
        if (!msg.method) return; // Not a request or notification

        // Notifications (no id) — acknowledge silently
        if (msg.id === undefined || msg.id === null) {
            // notifications/initialized, notifications/cancelled, etc.
            return;
        }

        let result;
        try {
            result = await this._dispatch(msg.method, msg.params || {});
            this._send({ jsonrpc: JSONRPC, id: msg.id, result });
        } catch (e) {
            this._send({
                jsonrpc: JSONRPC,
                id: msg.id,
                error: { code: e.code || -32603, message: e.message },
            });
        }
    }

    async _dispatch(method, params) {
        switch (method) {
            case 'initialize':
                this._initialized = true;
                return {
                    protocolVersion: MCP_VERSION,
                    capabilities: SERVER_CAPABILITIES,
                    serverInfo: SERVER_INFO,
                };

            case 'tools/list':
                return { tools: TOOLS };

            case 'tools/call':
                return this._callTool(params.name, params.arguments || {});

            case 'ping':
                return {};

            default:
                throw Object.assign(new Error(`Method not found: ${method}`), { code: -32601 });
        }
    }

    async _callTool(name, args) {
        switch (name) {
            case 'scan_skill':
                return handleScanSkill(args);
            case 'scan_text':
                return handleScanText(args);
            case 'check_tool_call':
                return handleCheckToolCall(args);
            case 'audit_assets':
                return await handleAuditAssets(args);
            case 'get_stats':
                return handleGetStats();
            case 'experimental.run_async':
                return handleRunAsync(args);
            case 'experimental.task_status':
                return handleTaskStatus(args);
            case 'experimental.task_result':
                return handleTaskResult(args);
            case 'experimental.task_cancel':
                return handleTaskCancel(args);
            default:
                return errorResult(`Unknown tool: ${name}`);
        }
    }

    _send(msg) {
        const body = JSON.stringify(msg);
        const header = `Content-Length: ${Buffer.byteLength(body)}\r\n\r\n`;
        process.stdout.write(header + body);
    }
}

// ── Export for CLI integration ──

function startServer() {
    const server = new MCPServer();
    server.start();
}

export {  MCPServer, startServer, TOOLS  };
