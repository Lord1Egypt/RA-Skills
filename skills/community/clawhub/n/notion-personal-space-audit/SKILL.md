---
name: notion-personal-space-audit
slug: notion-personal-space-audit
displayName: Notion Personal Space Audit
description: >
  Audit a personal Notion hub and its nested pages and databases: identify
  mixed content types, empty placeholders, weak navigation, and
  sensitivity-boundary problems, then produce a practical
  information-architecture redesign and migration map. Read-only by default —
  it never modifies Notion content without explicit authorization.
  中文摘要：审计个人 Notion 空间及其嵌套页面与数据库，识别混合内容类型、空占位记录、
  弱导航与敏感边界问题，产出信息架构重设计与迁移方案。默认只读。触发词：Notion 空间
  整理、Notion 页面审计、信息架构重构、数据库迁移方案.
description_zh: 个人 Notion 空间审计与重构——只读审计，输出信息架构重设计与迁移方案
description_en: Notion Personal Space Audit
version: "1.0.7"
agent_created: true
not_for:
  - Team or company workspace audits (personal hub focus)
  - Creating new Notion content or writing pages without explicit authorization
  - Building Notion API integrations or automations
  - Migrating content out of Notion to other platforms
  - Executing the migration itself without a separate explicit authorization
---

# Notion Personal Space Audit

## When to use

Use when the user asks to audit a Notion personal workspace or page, inspect secondary pages or inline databases, explain why the space is hard to use, decide where ambiguous materials such as sensitive analysis reports belong, or design a safer and more searchable information architecture.

## Steps

> Steps 2–4 are `[Deterministic]` (Notion API calls); steps 1 and 5–12 are `[LLM]` analysis and synthesis.

1. **[LLM]** Confirm the target page URL and scope. Treat the task as read-only unless the user explicitly authorizes a structural change.
2. **[Deterministic]** Resolve the page ID from the URL and retrieve the page metadata.
3. **[Deterministic]** Recursively retrieve block children. Follow `child_page` blocks and query `child_database` rows; preserve the parent path, page title, block count, and last-edited time.
4. **[Deterministic]** Retrieve database schemas and record property names/types. Separate database rows from true navigation pages when interpreting the root layout.
5. **[LLM]** Build an inventory by content identity using `references/audit-checklist.md`: log/event, analysis report, raw transcript/source, long-form archive, plan, reading item, person record, life utility, or inbox item.
6. **[LLM]** Detect structural issues per the checklist: missing dashboard, mixed responsibilities, inconsistent naming, empty placeholder records, long reports inside short-log databases, stale plans without lifecycle status, and sensitive materials mixed with ordinary notes.
7. **[LLM]** Recommend a small functional top-level architecture. Include an inbox, current actions, sensitive-analysis area, cognition/inputs, memory/archive, life tools, and archive only when evidence supports each area.
8. **[LLM]** Map every major existing database or page to a proposed destination. For ambiguous content, state the rule explicitly: sensitive analysis reports belong in a separate high-sensitivity archive; short event logs retain event records; raw conversations remain source material and link to derived decisions.
9. **[LLM]** Recommend minimal shared fields: content type, domain, status, occurrence date, organization date, sensitivity, and relations. Do not force one schema onto all content types.
10. **[LLM]** Produce a concise Markdown report with evidence, signal-light findings, proposed tree, migration table, phased migration order, and a clear statement that no Notion content was changed.
11. **[LLM]** If the user explicitly authorizes structure creation, create only empty navigation pages and usage instructions after the audit. Never move, delete, rename, or rewrite existing content unless separately authorized.
12. **[LLM]** If the user explicitly authorizes updating an existing audit/guide page, append a clearly marked usage-notes section rather than replacing prior findings; make the write idempotent with a unique marker and read the page back to verify the marker and section headings.

## Hard Rules

1. Read-only by default: no Notion write endpoint is called unless the user explicitly authorizes structure creation or updating an existing guide page; authorized guide-page updates must append rather than replace.
2. Never move, delete, rename, or rewrite existing content as part of an audit or structure setup.
3. Never expose access tokens in reports, logs, or user-facing output.
4. Do not invent content the API did not return; mark inaccessible or uncertain areas explicitly.
5. Sensitive analysis reports are never classified as ordinary log events, and never merged into general archives.

## Pitfalls

- Do not assume a page visible in the root snapshot is a standalone navigation page; inline database rows can appear as pages.
- Do not classify a sensitive analysis report as a log event merely because it concerns the same topic (emotions, relationships, health).
- Do not merge raw conversations, derived reports, and action plans into one record. Keep source, analysis, and action linked but distinct.
- Do not delete empty book/person placeholders during an audit. Put them in an archive or pending-review view first.
- Orphan pages not under any database are easy to miss; enumerate workspace top-level nodes first and recurse. Do not rely on database enumeration alone.
- Do not expose access tokens in reports, logs, or user-facing output.
- Do not modify Notion without explicit confirmation. The audit should produce a migration plan first.
- When structure creation is authorized, use idempotent title checks and create pages under the audited parent; do not move, delete, rename, or rewrite existing content as part of structure setup.
- Notion block append requests must be chunked to at most 100 blocks; use a unique marker to prevent duplicate guide sections, and verify by reading back the full child-block list rather than trusting the write response alone.
- Avoid inventing content that the API did not return. Mark inaccessible or uncertain areas explicitly.

## Failure Handling

| Scenario | Action |
|---|---|
| API returns 401/403 on a sub-page | Mark the branch as inaccessible; continue the audit on accessible areas; report the gap |
| Recursive crawl times out on a very large space | Crawl top two levels fully; sample deeper levels and state the sampling method |
| Database schema unreadable | Record the error and the visible properties; do not guess types |
| Notion API returns 429 / rate limit during the recursive crawl | Back off and retry the limited request; if it persists, crawl the remaining top-level nodes and list the rate-limited branches in the access-gap summary |
| Ambiguous content cannot be classified | List it in a pending-review section with the ambiguity stated, rather than forcing a category |
| User requests in-audit deletion | Refuse; deletion is out of audit scope — produce the migration plan first |

## Output Format

```markdown
# Notion Space Audit Report

## 1. Scope and crawl summary (pages / databases / rows, access gaps)
## 2. Current-state tree (with content-type labels)
## 3. Findings (signal-light: red blocks / yellow friction / green healthy patterns)
## 4. Proposed information architecture (top-level areas with one-sentence purpose)
## 5. Migration table (existing location → proposed destination, with rule for ambiguous items)
## 6. Phased migration order (low-risk first)
## 7. Declaration (no Notion content was changed during this audit)
```

## Verification

- Confirm the recursive crawl completed and report the page/database/row counts.
- Confirm each root database has a schema inventory and row count.
- Confirm the report includes a direct answer for ambiguous materials, especially sensitive reports.
- Confirm no Notion write endpoint was called without explicit authorization, and that any authorized guide-page update was read back to confirm the unique marker and section headings.
- Confirm the output file exists and names the inspected page, scope, findings, and migration plan.
- Access gaps are reported as unreadable resources with their identifiers, never as empty or deleted pages; the report states which parts of the tree could not be inspected.
