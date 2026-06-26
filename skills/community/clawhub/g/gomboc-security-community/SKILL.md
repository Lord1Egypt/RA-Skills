# Gomboc Code Remediation Skill

**Deterministic, merge-ready code fixes powered by ORL (Open Remediation Language).**

---

## Provenance & External Dependencies

**Source:** This skill wraps the official [Gomboc.ai Community Edition](https://www.gomboc.ai) code remediation engine.

**Official Documentation:** https://docs.gomboc.ai  
**Community Discussions:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions  
**GitHub App:** https://github.com/apps/gomboc-ai-community  

**External API Dependency:**
- **Endpoint:** https://api.app.gomboc.ai/graphql
- **Authentication:** Bearer token (Personal Access Token from https://app.gomboc.ai)
- **Required:** Free account at Gomboc.ai (no credit card)
- **Setup:** Generate token in Settings → Personal Access Tokens

**Token Scope & Security (Least Privilege):**
- **Scope:** Read-only API access (minimal required permissions)
- **Capabilities:** Query account, scans, runs, and fix events only
- **Restrictions:** Cannot modify, delete, or alter Gomboc configurations
- **Safe for CI/CD:** No destructive capabilities, suitable for GitHub Actions and workflow secrets
- **Best Practice:** Generate a dedicated token per environment/workflow; never commit to code
- **Storage:** Use GitHub Secrets (Actions) or CI provider's secure secret management
- **Verification:** Check token scope in Gomboc settings before use in production

**Shipped Files:**
- `SKILL.md` — This documentation
- `README.md` — Quick start guide
- `SECURITY.md` — Security audit
- `scripts/cli-wrapper.py` — Python CLI wrapper
- `scripts/docker-compose.yml` — MCP server configuration
- `examples/vulnerable.tf` — Example vulnerable code
- `references/` — Integration guides

**License:** MIT (see LICENSE.md)

---

Gomboc.ai Community Edition automatically scans and fixes code issues across your entire codebase — infrastructure, applications, configurations, and more — using a deterministic remediation engine (no hallucinations). Unlike traditional scanners that generate alerts, Gomboc delivers merge-ready pull requests that clear your code issues backlogs. This skill wraps Gomboc's power into agent workflows, CLI tools, and CI/CD pipelines, making it the perfect complement to agentic coding.

## How Gomboc Works

Gomboc's **Open Remediation Language (ORL)** engine operates through a multi-stage deterministic process:

```
Policy Definition → Code Analysis → Deterministic Fix Generation → PR Delivery
```

1. **Understands** your environment and code context
2. **Turns policies** into executable rules using ORL
3. **Analyzes** your code with full syntax-tree precision (via Tree-sitter)
4. **Generates** deterministic fixes (same input = same output, always)
5. **Delivers** merge-ready pull requests ready to review and ship

**Key difference:** While generative AI is probabilistic (helpful for reasoning but unpredictable), Gomboc's ORL provides deterministic remediation — predictable, repeatable, and auditable.

## What It Does

- **Scan** any codebase for issues (infrastructure, application code, configs)
- **Generate** deterministic, merge-ready pull requests with fixes
- **Remediate** continuously via GitHub Actions or interactive CLI/MCP
- **Trust** 94%+ fix acceptance rate with zero hallucinations (ORL Engine)
- **Pair with agents** — deterministic remediation that works perfectly alongside agentic coding systems

## Supported Languages & Frameworks

ORL supports remediation across multiple languages and code types via **syntax-tree matching** (Tree-sitter):

- **Infrastructure as Code**
  - Terraform (HCL)
  - CloudFormation (YAML/JSON)
  - Kubernetes manifests (YAML)
  - Helm charts
  
- **Configuration Files**
  - JSON, YAML, HCL
  - Shell scripts
  - Docker files
  
- **Code Languages**
  - Python
  - JavaScript/TypeScript
  - Go, Java, C#, Rust, and 20+ more
  
- **Cloud Providers**
  - AWS, Azure, GCP, OCI
  - Kubernetes, Helm
  
- **Policy Coverage**
  - CIS benchmarks
  - AWS best practices
  - Security hardening
  - Custom org policies

Full language list: `docker run --rm gombocai/orl language`

## Quick Start

### 1. Get a Token

```bash
# Sign up at https://app.gomboc.ai (free, Community Edition)
# Generate Personal Access Token in Settings
export GOMBOC_PAT="gpt_your_token"
```

### 2. Scan Code

```bash
python scripts/cli-wrapper.py scan --path ./src
```

### 3. Generate Fixes

```bash
python scripts/cli-wrapper.py fix --path ./src
```

### 4. Apply Fixes (Optional)

```bash
python scripts/cli-wrapper.py remediate --path ./src --commit
```

## Key Features

✅ **Deterministic AI** — Same fix every time, no hallucinations
✅ **94%+ Accuracy** — Merge-ready fixes users actually accept
✅ **Free Forever** — Community Edition of Gomboc.ai
✅ **Production-Ready** — Battle-tested implementation
✅ **Secure by Design** — No token leaking, proper error handling
✅ **Agent-Friendly** — Perfect for autonomous code improvement loops

## CLI Commands

### scan
Detect issues in your codebase

```bash
gomboc scan path:./terraform
gomboc scan path:./src policy:aws-cis format:markdown
```

### fix
Generate merge-ready fixes

```bash
gomboc fix path:./terraform format:pull_request
gomboc fix path:./src format:json
```

### remediate
Apply fixes directly to code

```bash
gomboc remediate path:./src commit:true
gomboc remediate path:./terraform commit:true push:true
```

### config
Manage authentication

```bash
gomboc config --show-token
```

## Why This Matters for Agents

Gomboc solves the **determinism problem** in AI-driven code improvement:

- **Deterministic Fixes** — ORL ensures same code always produces same fix (no randomness)
- **Repeatable** — Policies execute consistently across runs, repos, and teams
- **Trustworthy** — 94%+ merge rate because fixes are syntax-aware, not brittle regex patterns
- **Safe for Agents** — Agents can autonomously scan → generate → apply without human fear
- **Continuous Improvement** — Perfect for agentic loops: code generation → scanning → remediation → iterate

**The Agent Workflow:**
1. Agent generates code
2. Gomboc scans and identifies issues
3. ORL generates deterministic fixes
4. Agent reviews and applies fixes
5. Repeat with next feature/iteration

This creates a **feedback loop** where agents learn and improve continuously.

## Integration Methods

Gomboc integrates into your workflow through multiple paths:

### 1. VS Code / Cursor IDE (Developers)

Fastest way to try Gomboc interactively:

```bash
# Install: Gomboc VS Code Extension
# Set: GOMBOC_PAT in extension settings
# Run: Gomboc: Scan current file
# Review: Problems panel → Apply Fix
```

- Real-time scanning as you save
- Interactive fix review and apply
- See: https://docs.gomboc.ai/getting-started-ce

### 2. MCP Server (Agents)

Run the MCP server for agent integration:

```bash
docker-compose -f scripts/docker-compose.yml up
# Server runs on http://localhost:3100

# Or: docker run -p 3100:3100 -e GOMBOC_PAT='your_token' gombocai/mcp:latest
```

Agents interact with Gomboc via MCP protocol:
```bash
@gomboc scan path:./src
@gomboc fix path:./src format:pull_request
@gomboc remediate path:./code commit:true
```

See `references/mcp-integration.md` for details.

### 3. CLI Tool (Developers & Scripts)

Use the Python CLI for local scanning:

```bash
export GOMBOC_PAT="your_token"
python scripts/cli-wrapper.py scan --path ./src --format markdown
python scripts/cli-wrapper.py fix --path ./src --format pull_request
python scripts/cli-wrapper.py remediate --path ./src --commit
```

See `references/setup.md` for detailed instructions.

### 4. GitHub App (Automated)

Install Gomboc GitHub App for automatic PRs:

- https://github.com/apps/gomboc-ai-community
- Select repos to monitor
- Gomboc automatically scans on PR, generates fixes

### 5. GitHub Actions (CI/CD)

Automate continuous remediation in pipelines:

```yaml
- uses: gomboc-action@v1
  with:
    path: ./terraform
    auto-fix: true
    policy: default
```

See `references/github-action.md` for configuration.

## Configuration

All configuration is via environment variables:

| Variable | Purpose | Required | Example |
|----------|---------|----------|---------|
| `GOMBOC_PAT` | Personal Access Token | Yes | `gpt_abc123...` |
| `GOMBOC_MCP_URL` | MCP server URL | No | `http://localhost:3100` |
| `GOMBOC_POLICY` | Remediation policy | No | `default` or `aws-cis` |

## Security & Audit

This skill has been:
- ✅ Security-audited for token handling
- ✅ Verified against live Gomboc API
- ✅ Tested with real vulnerabilities
- ✅ Confirmed production-ready

See `SECURITY.md` for complete audit details.

## Open Remediation Language (ORL)

**ORL is the deterministic execution engine** that powers Gomboc fixes:

### Deterministic Remediation
- **Same input = same output, always** (no probabilistic AI)
- Syntax-tree aware (via Tree-sitter) instead of brittle regex
- Safe for bulk remediation across large codebases
- Results are auditable and reviewable

### How ORL Works
1. **Detects** policy violations by analyzing syntax trees
2. **Evaluates** context and code structure
3. **Applies** precise transformations (insert, modify, delete)
4. **Validates** fixes are safe and complete

### Policy-Driven Fixes
- **Policies** define what should be fixed (CIS, AWS best practices, custom rules)
- **ORL rules** execute those policies to generate code changes
- **Policy Sets** let you customize enforcement by environment/team

See: https://docs.gomboc.ai/orl

## Support & Documentation

- **Setup Guide:** `references/setup.md`
- **MCP Integration:** `references/mcp-integration.md`
- **GitHub Actions:** `references/github-action.md`
- **Security Audit:** `SECURITY.md`
- **Changelog:** `CHANGELOG.md`
- **Gomboc Official Docs:** https://docs.gomboc.ai
- **ORL Documentation:** https://docs.gomboc.ai/orl
- **GitHub Feedback:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions

## License

MIT License — See LICENSE file

---

**Ready to remediate?** Start with the Quick Start section above, then explore integration methods that fit your workflow.
