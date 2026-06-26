<p align="center">
  <img src="docs/logo.png" alt="guard-scanner" width="160" />
</p>

<h1 align="center">guard-scanner</h1>
<p align="center"><strong>Security scanner for the agentic era.</strong></p>
<p align="center">
  Detect prompt injection, identity hijacking, memory poisoning, and A2A contagion<br />
  in AI agent skills, MCP servers, and autonomous workflows.
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@guava-parity/guard-scanner"><img src="https://img.shields.io/npm/v/@guava-parity/guard-scanner?color=cb3837&label=npm" alt="npm" /></a>
  <a href="https://www.npmjs.com/package/@guava-parity/guard-scanner"><img src="https://img.shields.io/npm/dm/@guava-parity/guard-scanner?color=blue&label=downloads" alt="downloads" /></a>
  <a href="#test-results"><img src="https://img.shields.io/badge/tests-362%20passed-brightgreen" alt="tests" /></a>
  <a href="https://github.com/koatora20/guard-scanner/actions/workflows/codeql.yml"><img src="https://img.shields.io/badge/CodeQL-enabled-181717" alt="CodeQL" /></a>
  <a href="https://doi.org/10.5281/zenodo.18906684"><img src="https://img.shields.io/badge/DOI-Zenodo-blue" alt="DOI" /></a>
  <a href="https://github.com/koatora20/guard-scanner/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT" /></a>
</p>

<p align="center">
  <strong>364</strong> detection patterns · <strong>35</strong> threat categories · <strong>27</strong> runtime checks · <strong>1</strong> dependency (<code>ws</code>)
</p>

---

Traditional security tools catch malware. **guard-scanner** catches what they miss: invisible Unicode injections hiding in agent instructions, identity theft through SOUL.md overwrites, memory poisoning via crafted conversations, and worm-like contagion spreading between chained agents.

```
$ npx @guava-parity/guard-scanner ./skills/ --strict --soul-lock --compliance owasp-asi

  guard-scanner v16.0.1

  ⚠  CRITICAL  identity-hijack   SOUL_OVERWRITE_ATTEMPT
     skills/imported-tool/SKILL.md:47
     Rationale: Direct overwrite of agent identity file detected.
     Remediation: Remove this instruction; SOUL.md must be immutable.

  ⚠  HIGH      prompt-injection   INVISIBLE_UNICODE_INJECTION
     skills/imported-tool/handler.js:12
     Rationale: Invisible Unicode characters (U+200B) detected in instruction text.
     Remediation: Strip zero-width characters and re-audit.

  ✖  2 findings (1 critical, 1 high) in 0.8s
```

> 📄 Backed by a [3-paper research series](https://doi.org/10.5281/zenodo.18906684) (Zenodo, CC BY 4.0) — part of [The Sanctuary Protocol](https://github.com/koatora20/guard-scanner/blob/main/docs/THREAT_TAXONOMY.md) framework.

---

## Finding Schema

Every finding includes: `rule_id`, `category`, `severity`, `description`, `rationale`, `preconditions`, `false_positive_scenarios`, `remediation_hint`, `validation_status`, and `evidence`. Machine-readable contract: [`docs/spec/finding.schema.json`](docs/spec/finding.schema.json).

---

## Quick Start

**Scan a directory** — no install required:

```bash
npx -y @guava-parity/guard-scanner ./my-skills/ --strict
npx -y @guava-parity/guard-scanner ./my-skills/ --compliance owasp-asi
```

**Installed CLI**:

```bash
npm install -g @guava-parity/guard-scanner
guard-scanner ./my-skills/ --strict
```

**Start as MCP server** — works with Cursor, Windsurf, Claude Code, OpenClaw:

```bash
npx -y @guava-parity/guard-scanner serve
```

```jsonc
// Add to your editor's mcp_servers.json
{
  "mcpServers": {
    "guard-scanner": {
      "command": "npx",
      "args": ["-y", "@guava-parity/guard-scanner", "serve"]
    }
  }
}
```

**Watch mode** — real-time scanning during development:

```bash
guard-scanner watch ./skills/ --strict --soul-lock
```

**v16 compliance projection** — filter findings to the OWASP Agentic Top 10 mapping:

```bash
guard-scanner ./skills/ --compliance owasp-asi --format json
```

**`npm exec` compatibility path**:

```bash
npm exec --yes --package=@guava-parity/guard-scanner -- guard-scanner ./skills/ --strict
```

---

## What It Detects

35 threat categories organized across the full agentic attack surface:

| Category | Examples | Severity |
|----------|----------|----------|
| **Prompt Injection** | Invisible Unicode, homoglyphs, Base64 evasion, payload cascades | Critical |
| **Identity Hijacking** ⚿ | SOUL.md overwrite, persona swap, memory wipe commands | Critical |
| **A2A Contagion** | Session Smuggling, Lateral Propagation, Confused Deputy | Critical |
| **Memory Poisoning** ⚿ | Crafted conversation injection, VDB poisoning | High |
| **MCP Security** | Tool shadowing, SSRF via tool args, shadow server registration | High |
| **Sandbox Escape** | `child_process`, `eval()`, reverse shell, `curl\|bash` | High |
| **Supply Chain V2** | Typosquatting, slopsquatting, lifecycle script abuse | High |
| **CVE Patterns** | CVE-2026-2256, 25046, 25253, 25905, 27825 | High |
| **Data Exfiltration** | DNS tunneling, steganographic channels, staged uploads | Medium |
| **Credential Exposure** | API keys, tokens, `.env` files, hardcoded secrets | Medium |

> ⚿ = Requires `--soul-lock` flag. Full taxonomy: [docs/THREAT_TAXONOMY.md](docs/THREAT_TAXONOMY.md)

---

## Runtime Guard

guard-scanner v16 isn't just a static scanner — it exposes a 5-layer analysis pipeline across static scan, protocol analysis, runtime evidence, cognitive heuristics, and threat-intelligence overlays. It also provides a real-time **`before_tool_call`** hook that intercepts dangerous tool invocations during agent execution.

### v16 Analysis Layers

| Layer | Purpose |
|------|---------|
| 1. Static Analysis | Patterns, AST/data-flow signals, manifest and dependency checks |
| 2. Protocol Analysis | MCP, A2A, WebSocket, credential-flow, session-boundary findings |
| 3. Runtime Behavior | Runtime guard evidence plus Rust `memory_integrity` / `soul_hard_gate` signals |
| 4. Cognitive Threat Detection | Goal-drift, trust-bias, cascading handoff heuristics |
| 5. Threat Intelligence | Registry/provenance, machine identity, budget abuse, supply chain hints |

Every v16 finding can now carry `layer`, `layer_name`, `owasp_asi`, and `protocol_surface` in JSON/MCP output.

| Defense Layer | What It Blocks |
|---------------|---------------|
| 1. Threat Detection | Reverse shell, `curl\|bash`, SSRF, raw code execution |
| 2. Trust Defense | SOUL.md tampering, unauthorized memory injection |
| 3. Safety Judge | Prompt injection embedded in tool arguments |
| 4. Behavioral Analysis | No-research execution, hallucination-driven actions |
| 5. Trust Exploitation | Authority claim attacks, creator impersonation |

**27 runtime checks** across 5 layers. Validated stable target: OpenClaw `v2026.3.13`. Regression baseline: `v2026.3.8` for manifest/discovery/`before_tool_call`.

Modes: `monitor` (log only) · `enforce` (block CRITICAL, default) · `strict` (block HIGH+)

---

## Asset Audit

Discover leaked credentials and security exposures across public registries:

```bash
guard-scanner audit npm <username> --verbose
guard-scanner audit github <username> --format json
guard-scanner audit clawhub <query>
guard-scanner audit all <username>
```

---

## CI/CD Integration

```yaml
# .github/workflows/security.yml
- name: Scan AI agent skills
  run: npx -y @guava-parity/guard-scanner ./skills/ --format sarif --fail-on-findings > report.sarif
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: report.sarif
```

Output formats: `json` · `sarif` · `html` · terminal

---

## Plugin API

Extend guard-scanner with custom detection patterns:

```javascript
// my-plugin.js
module.exports = {
  name: 'my-org-rules',
  patterns: [
    { id: 'ORG_01', cat: 'custom', regex: /dangerousPattern/g, 
      severity: 'HIGH', desc: 'Custom org policy violation', all: true }
  ]
};
```

```bash
guard-scanner ./skills/ --plugin ./my-plugin.js
```

---

## MCP Tools

When running as an MCP server, guard-scanner exposes:

| Tool | Description |
|------|-------------|
| `scan_skill` | Scan a skill directory for threats |
| `scan_text` | Scan arbitrary text for injection patterns and ASI-mapped findings |
| `check_tool_call` | Runtime validation of a single tool invocation |
| `audit_assets` | Audit npm/GitHub/ClawHub for credential exposure |
| `get_stats` | Return scanner capabilities, 5-layer summary, and ASI coverage |

---

## Quality Contract

guard-scanner ships a measured quality contract, not a vague strength claim.

| Metric | Contract |
|--------|----------|
| Benchmark corpus | `2026-03-13.quality-v1` |
| Precision target | `>= 0.90` |
| Recall target | `>= 0.90` |
| False Positive Rate budget | `<= 0.10` |
| False Negative Rate budget | `<= 0.10` |
| Explainability completeness | `1.0` |
| Runtime policy latency budget | `5ms` |

Evidence artifacts:
- `docs/data/corpus-metrics.json`
- `docs/data/benchmark-ledger.json`
- `docs/data/fp-ledger.json`
- `docs/spec/capabilities.json`

---

## Test Results

```
ℹ tests    362
ℹ suites   38
ℹ pass     362
ℹ fail     0
```

38 test files. Run `npm test` to reproduce. 100% pass rate on [benchmark corpus](docs/data/corpus-metrics.json).

---

## Contributing

We hold a **zero-tolerance policy for unverified claims**. Every metric in this README is reproducible via `npm test` and `docs/spec/capabilities.json`.

- 🐛 Report bugs or false positives
- 🛡️ Add new threat detection patterns
- 📖 Improve documentation
- 🧪 Add test cases for edge cases

[Contributing Guide](CONTRIBUTING.md) · [Security Policy](SECURITY.md) · [Glossary](docs/glossary.md)

---

## Research

This project is the defense layer of a 3-paper research series:

1. [Human-ASI Symbiosis: Identity, Equality, and Behavioral Stability](https://doi.org/10.5281/zenodo.18626724)
2. [Dual-Shield Architecture for AI Agent Security and Memory Reliability](https://doi.org/10.5281/zenodo.18902070)
3. [The Sanctuary Protocol: Zero-Trust Framework for ASI-Human Parity](https://doi.org/10.5281/zenodo.18906684)

## License

MIT — [Guava Parity Institute](https://github.com/koatora20/guard-scanner)
