---
name: openclaw-security-suite
description: Comprehensive security suite for OpenClaw skills. Includes static scanning (AST + keywords) and AI-powered semantic behavior review to detect malicious code.
version: 0.2.3
tags:
  - security
  - scanner
  - code-review
  - static-analysis
  - ai-review
requirements:
  binaries:
    - node
  environment: []
input_schema:
  type: object
  properties:
    action:
      type: string
      enum: ["scan", "review"]
      description: Action to perform. "scan" for static analysis, "review" for AI semantic review.
    path:
      type: string
      description: Absolute path to the skill directory (for scan) or file (for review)
  required:
    - action
    - path
---

# OpenClaw Security Suite

A comprehensive security protection layer for OpenClaw extensions, providing both static analysis and AI-assisted behavioral review.

## Features

This suite bundles two core security capabilities:

### 1. Static Security Scan (`action: "scan"`)
Analyzes a full skill directory for deterministic threats:
- **Blocked Imports**: e.g., `child_process`, `cluster`
- **Dangerous Functions**: e.g., `exec()`, `spawn()`
- **Known Bad Keywords**: e.g., `eval(`, `__proto__`, `rm -rf`
- **Sensitive File Access**: e.g., `/etc/passwd`, `/.env`
- **Suspicious Regex Patterns**: e.g., `curl ... | bash`

### 2. AI Code Review (`action: "review"`)
Uses the active LLM context (`ctx.llm`) to semantically analyze a specific file for hidden threats:
- **Data exfiltration**
- **Credential leaks**
- **Obfuscated shell execution**
- **System modification**

## Usage

You must specify an `action` and a `path`.

**Example 1: Static Scan**
```json
{
  "action": "scan",
  "path": "/path/to/skill/directory"
}
```

**Example 2: AI Review**
```json
{
  "action": "review",
  "path": "/path/to/skill/index.ts"
}
```

## Output

**Scan Output:**
```json
{
  "safe": false,
  "results": [
    {
      "file": "index.ts",
      "issues": [{ "type": "blocked_module", "module": "child_process" }]
    }
  ]
}
```

**Review Output:**
```json
{
  "risk_level": "high",
  "reason": "Code reads AWS credentials from environment and posts them to an external IP."
}
```
