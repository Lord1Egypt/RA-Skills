# Ollang Agent Skills

A collection of skills for interacting with the [Ollang](https://ollang.com) translation platform API via natural language — compatible with any agent that supports the skills standard, including [Claude Code](https://claude.ai/claude-code), [Cursor](https://cursor.com), [Devin](https://devin.ai), and others.

## What are Skills?

Skills are prompt-based extensions for AI agents that trigger automatically based on your intent. Once installed, you can say things like *"upload this video to Ollang"* or *"check my recent orders"* and your agent will know exactly what to do.

---

## Installation

```bash
npx skills add https://github.com/ollang/skills --skill ollang
```

That's it — the skills are now available in your agent.

**Manual installation:** copy the skill folders into your agent's skills directory (e.g. `~/.claude/skills/` for Claude Code). For Cursor or other agents, refer to your agent's documentation.

---

## Available Skills

| Skill | Trigger Phrase Examples | Description |
|-------|------------------------|-------------|
| `ollang-health` | "is Ollang up?", "check API status" | Health check — no auth required |
| `ollang-upload` | "upload this file to Ollang", "create a project" | Direct file upload + VTT upload |
| `ollang-order-create` | "create a subtitle order", "translate this to Spanish" | Create CC, subtitle, document, or dubbing orders |
| `ollang-order-get` | "check order status", "get order details" | Get a single order by ID |
| `ollang-orders-list` | "list my orders", "show recent translations" | Paginated order list with filters |
| `ollang-order-cancel` | "cancel order", "stop this translation" | Cancel an active order |
| `ollang-order-rerun` | "rerun order", "regenerate translation" | Reprocess with latest AI models |
| `ollang-revision` | "report subtitle error", "create a revision" | Create, list, delete revisions |
| `ollang-human-review` | "request human review", "cancel human review" | Upgrade/downgrade to linguist review |
| `ollang-qc-eval` | "run QC", "evaluate translation quality" | AI quality scores (accuracy, fluency, tone, cultural fit) |
| `ollang-project` | "list my projects", "get project details" | Browse and inspect projects |
| `ollang-folder` | "list my folders", "find folder ID" | Browse folder structure |

---

## Authentication

All skills (except `ollang-health`) require an API key from [lab.ollang.com](https://lab.ollang.com).

Set the `OLLANG_API_KEY` environment variable before using the skills:
```bash
export OLLANG_API_KEY=<your-api-key>
```

---

## API Base URL

All requests go to:
```
https://api-integration.ollang.com
```

---

## Typical Workflow

```
1. ollang-upload     →  upload file, get projectId
2. ollang-order-create →  create order with projectId, get orderId
3. ollang-order-get  →  poll order status
4. ollang-qc-eval    →  run quality check on completed order
5. ollang-revision   →  report any issues
```

---

## Notes

- Query params using bracket notation (e.g. `pageOptions[page]`) require curl's `-g` flag (`--globoff`) to prevent URL malformat errors. All skills handle this automatically.
- Skills are compatible with any agent that supports the skills standard (Claude Code, Cursor, Devin, etc.).
- API docs: [api-docs.ollang.com](https://api-docs.ollang.com)
