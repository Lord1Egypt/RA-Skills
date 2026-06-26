---
name: guard-scanner
description: "Security scanner and runtime guard for OpenClaw skills, MCP servers, and AI agent workflows. Detects prompt injection, identity hijacking, memory poisoning, A2A contagion, secret leaks, supply-chain abuse, and dangerous tool calls with 364 static threat patterns across 35 threat categories plus 27 runtime checks. Use when reviewing a new skill before install, scanning a workspace in CI/CD (SARIF/JSON/HTML), auditing npm/GitHub/ClawHub assets for leaked credentials, running watch mode during development, exposing scanner tools over MCP for Cursor/Windsurf/Claude Code/OpenClaw, or enforcing before_tool_call policy in OpenClaw. v16 adds 5-layer analysis output (`layer`, `layer_name`, `owasp_asi`, `protocol_surface`) and `--compliance owasp-asi`. MIT licensed; single runtime dependency (`ws`)."
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["node"]}}}
---

# guard-scanner

Security scanner and runtime guard for the agentic stack. Use it before installing a skill from ClawHub, when auditing MCP servers or OpenClaw workspaces, when wiring security checks into CI/CD, or when you want OpenClaw to block dangerous tool calls at runtime.

It covers prompt injection, identity hijacking, memory poisoning, A2A contagion, MCP abuse, secret leakage, supply-chain abuse, and dangerous execution patterns. v16 adds a 5-layer analysis pipeline, OWASP ASI projection mode, richer finding metadata, and Rust runtime evidence integration.

## Quick Start

```bash
# Scan a skill directory
npx -y @guava-parity/guard-scanner ./my-skills/ --verbose

# Scan with identity protection
npx -y @guava-parity/guard-scanner ./skills/ --soul-lock --strict

# Filter to OWASP ASI mapped findings only
npx -y @guava-parity/guard-scanner ./skills/ --compliance owasp-asi --format json

# Installed CLI
guard-scanner ./skills/ --strict

# npm exec compatibility
npm exec --yes --package=@guava-parity/guard-scanner -- guard-scanner ./skills/ --strict
```

## Core Commands

### Scan

```bash
guard-scanner <dir>         # Scan directory
guard-scanner <dir> -v      # Verbose output
guard-scanner <dir> --json  # JSON report file
guard-scanner <dir> --sarif # SARIF for CI/CD
guard-scanner <dir> --html  # HTML report
guard-scanner <dir> --compliance owasp-asi --format json
```

### Asset Audit

Audit public registries for credential exposure.

```bash
guard-scanner audit npm <username>
guard-scanner audit github <username>
guard-scanner audit clawhub <query>
guard-scanner audit all <username> --verbose
```

### MCP Server

Start as MCP server for IDE integration.

```bash
guard-scanner serve
```

Editor config (Cursor, Windsurf, Claude Code, OpenClaw):

```json
{
  "mcpServers": {
    "guard-scanner": {
      "command": "npx",
      "args": ["-y", "@guava-parity/guard-scanner", "serve"]
    }
  }
}
```

MCP tools: `scan_skill`, `scan_text`, `check_tool_call`, `audit_assets`, `get_stats`, and the async experimental task helpers.

## Quality Contract

Public quality contract:

- Benchmark corpus version: `2026-03-15.quality-v17`
- Precision target: `>= 0.90`
- Recall target: `>= 0.90`
- FPR/FNR budgets: `<= 0.10`
- Explainability completeness: `1.0`
- Runtime policy latency budget: `5ms`

Evidence surfaces:

- `docs/spec/capabilities.json`
- `docs/data/corpus-metrics.json`
- `docs/data/benchmark-ledger.json`
- `docs/data/fp-ledger.json`

### Watch Mode

Monitor skill directories in real-time during development.

```bash
guard-scanner watch ./skills/ --strict --soul-lock
```

### VirusTotal Integration

Combine semantic detection with VirusTotal's 70+ antivirus engines. Optional — guard-scanner works fully without it.

```bash
export VT_API_KEY=your-key
guard-scanner scan ./skills/ --vt-scan
```

## Runtime Guard

The validated OpenClaw surface is the compiled runtime plugin entry (`dist/openclaw-plugin.mjs`) discovered through `package.json > openclaw.extensions` and mounted on `before_tool_call` for OpenClaw `v2026.3.13`, with regression coverage kept on `v2026.3.8`.

The `before_tool_call` hook provides 27 runtime checks across 5 defense layers, while v16 scan output adds a second 5-layer analysis view:

| Layer | Focus |
|-------|-------|
| 1. Threat Detection | Reverse shell, curl\|bash, SSRF |
| 2. Trust Defense | SOUL.md tampering, memory injection |
| 3. Safety Judge | Prompt injection in tool arguments |
| 4. Behavioral | No-research execution detection |
| 5. Trust Exploitation | Authority claims, creator bypass |

Modes: `monitor` (log only), `enforce` (block CRITICAL, default), `strict` (block HIGH+).

## v16 Output Surface

- Finding fields: `layer`, `layer_name`, `owasp_asi`, `protocol_surface`
- Compliance mode: `--compliance owasp-asi`
- MCP summaries: `scan_skill`, `scan_text`, and `get_stats` now surface layer and ASI context
- Runtime evidence: Rust `memory_integrity` and `soul_hard_gate` modules are represented in the TypeScript pipeline

## Key Flags

| Flag | Effect |
|------|--------|
| `--verbose` / `-v` | Detailed findings with line numbers |
| `--strict` | Lower detection thresholds |
| `--soul-lock` | Enable identity protection patterns |
| `--json` / `--sarif` / `--html` | Output format |
| `--fail-on-findings` | Exit 1 on findings (CI/CD) |
| `--check-deps` | Scan package.json dependencies |
| `--rules <file>` | Load custom rules JSON |
| `--plugin <file>` | Load plugin module |
| `--compliance owasp-asi` | Keep only OWASP ASI mapped findings in output |

## Custom Rules

```javascript
module.exports = {
  name: 'my-plugin',
  patterns: [
    { id: 'MY_01', cat: 'custom', regex: /dangerous_pattern/g, severity: 'HIGH', desc: 'Description', all: true }
  ]
};
```

```bash
guard-scanner ./skills/ --plugin ./my-plugin.js
```

## CI/CD Integration

```yaml
# .github/workflows/security.yml
- name: Scan AI skills
  run: npx -y @guava-parity/guard-scanner ./skills/ --format sarif --fail-on-findings > report.sarif
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: report.sarif
```

## Threat Categories

35 categories covering OWASP LLM Top 10 + Agentic Security Top 10. See `src/patterns.ts` for the full pattern database. Key categories:

- **Prompt Injection** — hidden instructions, invisible Unicode, homoglyphs
- **Identity Hijacking** ⚿ — persona swap, SOUL.md overwrites, memory wipe
- **Memory Poisoning** ⚿ — crafted conversation injection
- **MCP Security** — tool poisoning, SSRF, shadow servers
- **A2A Contagion** — agent-to-agent worm propagation
- **Supply Chain V2** — typosquatting, slopsquatting, lifecycle scripts
- **CVE Patterns** — CVE-2026-2256, 25046, 25253, 25905, 27825

> ⚿ = Requires `--soul-lock` flag
