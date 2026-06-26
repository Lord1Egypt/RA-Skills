---
name: knowledge-router
description: Build a lightweight routing layer across existing knowledge sources such as MEMORY.md, daily memory files, self-improving notes, skill references, and audit records. Use when you need to decide where a question should be answered from before reading too much, when you want a unified knowledge index, or when you want to detect which knowledge should be promoted into a more durable layer.
---

# Knowledge Router

Route queries to the right knowledge layer before doing broad reading.

## Core workflow
1. Scan known knowledge sources and classify them by role.
2. Infer the query intent: rule, fact, method, evidence, or improvement.
3. Recommend primary and secondary sources.
4. Emit promotion hints when knowledge seems mature enough to move upward into a more durable layer.

## Read references as needed
- Read `references/source-types.md` for the knowledge source model.
- Read `references/routing-rules.md` for intent-to-source routing rules.
- Read `references/promotion-rules.md` for when knowledge should be promoted or extracted.
- Read `references/report-format.md` for the report structure.
- Read `references/release-minimal.md` before packaging or publishing so the first public surface stays minimal.

## Use scripts as needed
- Use `scripts/knowledge_router.py "<query>" [--scope ...] [--output report.txt]` to build a routing report.

## Operating rules
- Prefer routing over re-storing knowledge.
- Prefer a small number of clearly justified sources over broad search noise.
- Treat audit logs as evidence, not as the first answer source for general method questions.
- Keep the first version focused on source typing, query intent, and recommendation quality.
