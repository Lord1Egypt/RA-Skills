# L76 Core Architecture Skill

**Version:** 1.0.0  
**Author:** openclaw  
**Emoji:** 🏗️

A complete, production-ready AgentSkills template demonstrating best practices for skill architecture, tool integration, error handling, and publishing workflows.

## Quick Start

```bash
# Test the skill
cd D:\OpenClaw\workspace\skills\l76-core-arch
node index.js

# Validate structure
powershell -ExecutionPolicy Bypass -File scripts/validate.ps1

# Publish to ClawHub (after login)
clawhub publish . --slug l76-core-arch --name "L76 Core Architecture" --version 1.0.0
```

## Structure

```
l76-core-arch/
├── SKILL.md              # Skill manifest + instructions
├── index.js              # Main entry point (Node.js)
├── README.md             # This file
├── MEMORY_ITEMS.md       # 16 memory items (8 core + 8 advanced)
├── references/
│   ├── examples.md       # Basic usage examples and patterns
│   ├── examples-advanced.md    # Advanced complete examples
│   ├── troubleshooting.md      # Diagnostic guide and solutions
│   ├── performance-tuning.md   # Optimization strategies
│   └── extension-points.md     # Extension architecture guide
└── scripts/
    ├── validate.ps1      # PowerShell validation script
    └── validate.sh       # Bash validation script (Unix)
```

## Features

✅ **Complete SKILL.md Structure** — Frontmatter, triggers, workflows, error handling  
✅ **Main Entry Logic** — Reusable Node.js script with StateManager and SkillExecutor  
✅ **Tool Integration Patterns** — Sequential, conditional, error recovery, batch, state  
✅ **Error Handling** — Categorized errors with recovery strategies  
✅ **Validation Scripts** — Automated checks before publishing  
✅ **Memory Items** — 16 knowledge items (8 core + 8 advanced) for long-term retention  
✅ **Examples** — Basic and advanced usage patterns in `references/`  
✅ **Troubleshooting Guide** — Diagnostic flow, common issues, solutions  
✅ **Performance Tuning** — Optimization strategies, profiling, benchmarks  
✅ **Extension Points** — Plugin system, custom executors, tool wrappers  

## When to Use This Skill

- **Creating a new skill** — Use as a template
- **Auditing existing skills** — Compare against this structure
- **Learning AgentSkills** — Study patterns and best practices
- **Teaching others** — Reference for skill architecture
- **Extending skills** — Use extension points for advanced features
- **Debugging issues** — Follow troubleshooting diagnostic flow
- **Optimizing performance** — Apply tuning strategies and patterns

---

## Documentation Index

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [`SKILL.md`](SKILL.md) | Skill manifest and core instructions | First-time setup, trigger conditions |
| [`README.md`](README.md) | Quick start and overview | Getting started |
| [`references/examples.md`](references/examples.md) | Basic usage patterns | Learning core patterns |
| [`references/examples-advanced.md`](references/examples-advanced.md) | Complete advanced examples | Building complex skills |
| [`references/troubleshooting.md`](references/troubleshooting.md) | Diagnostic guide and solutions | When things go wrong |
| [`references/performance-tuning.md`](references/performance-tuning.md) | Optimization strategies | Skills running slow or using too much memory |
| [`references/extension-points.md`](references/extension-points.md) | Extension architecture | Adding custom features, plugins |
| [`MEMORY_ITEMS.md`](MEMORY_ITEMS.md) | Knowledge capture items | After completing skill work |
| [`scripts/validate.ps1`](scripts/validate.ps1) | Automated validation | Before publishing |

## Memory Items Included

1. **Skill Structure Template** — Directory layout and required files
2. **SKILL.md Frontmatter Standards** — Metadata requirements
3. **Tool Integration Patterns** — 5 core patterns for tool usage
4. **Error Handling Strategy** — Categorization and response format
5. **Skill Testing Checklist** — Pre-publish validation
6. **ClawHub Publishing Flow** — Step-by-step publishing
7. **State Management for Skills** — Cross-run persistence
8. **Skill Documentation Standards** — Documentation structure

## Validation

Run validation before publishing:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File scripts/validate.ps1

# Unix/Linux/macOS (Bash)
bash scripts/validate.sh
```

Checks performed:
- Required files present (SKILL.md)
- Optional files present (index.js, references/)
- YAML frontmatter valid
- No placeholder text left behind
- JavaScript syntax valid
- File sizes acceptable

## Publishing to ClawHub

```bash
# 1. Login
clawhub login

# 2. Publish
clawhub publish . \
  --slug l76-core-arch \
  --name "L76 Core Architecture" \
  --version 1.0.0 \
  --changelog "Initial release: complete skill architecture template"

# 3. Verify
clawhub list
clawhub search "architecture"
```

## License

MIT — Use freely for your own skills.

## References

- [AgentSkills Spec](https://github.com/OpenClaw/spec)
- [ClawHub Documentation](https://clawhub.com/docs)
- [OpenClaw Workspace Skills](D:\OpenClaw\workspace\skills)
- [NPM OpenClaw Skills](D:\OpenClaw\app-data\migrated\npm\node_modules\openclaw\skills)

---

**Built for OpenClaw** 🦞 | **Version 1.0.0** | **2026-03-22**
