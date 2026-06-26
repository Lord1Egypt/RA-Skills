---
name: open-code-review
description: "Scan AI-generated code for hallucinated packages, stale APIs, security anti-patterns, and over-engineering. Use when: (1) reviewing PRs with AI-generated code, (2) running pre-merge quality gates, (3) scanning repos for AI-specific defects that traditional linters miss. NOT for: basic linting, formatting, or general code review guidance."
homepage: https://github.com/raye-deng/open-code-review
metadata: {"openclaw":{"homepage":"https://github.com/raye-deng/open-code-review"}}
---

# Open Code Review — AI Code Quality Scanner

Scan codebases for **AI-specific defects** that traditional linters (ESLint, SonarQube, Checkstyle) cannot detect.

## What It Detects

| Category | Example | Severity |
|----------|---------|----------|
| **Hallucinated packages** | `import { parseJson } from 'fast-json-utils'` (package doesn't exist on npm) | 🔴 Critical |
| **Stale APIs** | `response.json().then()` with v2 API that was removed in v4 | 🟡 Warning |
| **Context breaks** | Two files reference the same function name with different signatures | 🟡 Warning |
| **Security anti-patterns** | Hardcoded secrets, deprecated crypto, insecure defaults | 🔴 Critical |
| **Over-engineering** | Unnecessary abstraction layers, dead code, excessive indirection | 🔵 Info |

## Quick Start

```bash
# Install
npx @opencodereview/cli scan ./src --sla L1

# With AI-powered deep scan (requires Ollama or API key)
npx @opencodereview/cli scan ./src --sla L2

# Diff mode for CI/CD
npx @opencodereview/cli scan ./src --diff --base origin/main --head HEAD

# SARIF output for GitHub Actions
npx @opencodereview/cli scan ./src --format sarif --output results.sarif
```

## Three Scan Levels

- **L1** — Structural analysis (AST, ~3 seconds, no AI needed)
- **L2** — L1 + Embedding recall (detects hallucinated packages via vector similarity)
- **L3** — L2 + LLM deep scan (understands context, semantics, business logic)

## GitHub Action

```yaml
- uses: raye-deng/open-code-review@v1
  with:
    scan-path: src/
    sla-level: L1
    diff-mode: true
```

## MCP Server

Available on Smithery, Cursor Directory, and npm:

```json
{
  "mcpServers": {
    "open-code-review": {
      "url": "https://open-code-review-mcp.v2ray-seins.workers.dev/mcp"
    }
  }
}
```

Or via stdio:
```json
{
  "mcpServers": {
    "open-code-review": {
      "command": "npx",
      "args": ["-y", "@opencodereview/mcp-server"]
    }
  }
}
```

## Supported Languages

TypeScript, JavaScript, Python, Java, Go, Kotlin

## When to Use This Skill

- A PR contains AI-generated code (Copilot, Cursor, Claude, GPT)
- You want to catch defects that pass all unit tests but will fail in production
- Pre-merge quality gate for AI-assisted development workflows
- Scanning third-party AI-generated code before integration

## When NOT to Use

- Basic linting (use ESLint, Ruff, Checkstyle instead)
- Code formatting (use Prettier, gofmt)
- General code review guidance (use the built-in code-review skill)

## Links

- **GitHub**: https://github.com/raye-deng/open-code-review
- **Portal**: https://codes.evallab.ai
- **npm CLI**: `@opencodereview/cli`
- **npm MCP**: `@opencodereview/mcp-server`
- **License**: BSL 1.1 (free for individuals, commercial subscription for teams)
