# OpenClaw Security

> Security protection layer for OpenClaw skills — scan, review, and guard against malicious code.

## Architecture

```
security_skill_scanner/
├── index.ts                 # Plugin entry — exports scanSkill & reviewSkill
├── config/
│   ├── policy.json          # Blocked modules, functions & permissions
│   └── malicious_patterns.json  # Dangerous keyword patterns
├── scanner/
│   ├── skill_scanner.ts     # Orchestrator — scans all .ts/.js in a directory
│   ├── ast_scanner.ts       # AST-based detection (blocked imports & calls)
│   ├── keyword_scanner.ts   # Text-based dangerous keyword matching
│   └── vm_runner.ts         # Sandboxed code execution (Node vm)
├── guard/
│   └── runtime_guard.ts     # Runtime protection (block metadata & shell access)
├── llm/
│   └── ai_review.ts         # LLM-powered code review
├── signature/
│   └── verify_signature.ts  # SHA256 file signature verification
└── skills/
    ├── scan_skill/index.ts  # Skill: static security scan
    └── review_skill/index.ts # Skill: AI-assisted code review
```

### `openclaw-security-suite`

Unified security tool providing both static analysis and AI-assisted code review.

**Input:**
```json
{ 
  "action": "scan", // or "review"
  "path": "/path/to/skill/directory" 
}
```

**Output (Scan):**
```json
{
  "safe": false,
  "results": [
    {
      "file": "index.ts",
      "issues": [
        { "type": "blocked_module", "module": "child_process" },
        { "type": "keyword", "keyword": "eval(" }
      ]
    }
  ]
}
```

## Security Layers

| Layer | Method | What it catches |
|-------|--------|-----------------|
| **AST Scanner** | Babel AST traversal | Blocked module imports (`child_process`, `cluster`), dangerous function calls (`exec`, `spawn`) |
| **Keyword Scanner** | Text matching | `eval(`, `__proto__`, `process.env`, `fs.writeFileSync`, etc. |
| **VM Runner** | Node.js `vm` sandbox | Runtime behavior analysis with memory isolation and 1s timeout |
| **Runtime Guard** | Argument inspection | Cloud metadata access (`169.254.169.254`), shell command execution |
| **AI Review** | LLM analysis | Data exfiltration, credential leaks, system modification |
| **Signature Verify** | SHA256 + public key | File integrity and authenticity |

## Setup

```bash
npm install
```

## Configuration

### `config/policy.json`

```json
{
  "blocked_modules": ["child_process", "cluster"],
  "blocked_functions": ["exec", "spawn", "execSync"],
  "allowed_permissions": ["network", "memory"],
  "blocked_permissions": ["shell", "process"]
}
```

### `config/malicious_patterns.json`

Contains a list of `dangerous_keywords` matched via text search (e.g. `eval(`, `Function(`, `__proto__`).

## License

MIT
