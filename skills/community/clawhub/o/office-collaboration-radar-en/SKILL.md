---
name: office-collaboration-radar-en
description: >-
  Extract an evidence-linked collaboration status card from chat logs, meeting notes, and project updates.
  Use only when a user explicitly asks for project progress, confirmed decisions, owner-and-deadline actions, blockers,
  cross-functional dependencies, human-review items, an executive summary, a radar chart, or stable JSON.
  Do not trigger merely because the user pasted text. Use this English package only when the user requests English output. It processes user-supplied local files,
  redacts common PII and credential patterns, and writes only to an explicit output path.
allowed-tools: "Bash(python3 scripts/process.py:*) Bash(python3 scripts/radar_chart.py:*) Bash(python3 scripts/export_card.py:*) Read Write"
---

# Office Collaboration Radar — English

Turn scattered collaboration records into a stable, auditable project status card. Extract only facts supported by the supplied material. Do not produce a full weekly report, judge individual performance, send reminders, or write to external systems.

Language choice: use this package only after the user requests English analysis or output. For Chinese material, use [Office Collaboration Radar](https://clawhub.ai/yamyeed/skills/office-collaboration-radar).

## Capabilities

- Produce seven fixed modules: overview, progress, decisions, actions, risks and dependencies, cross-functional relationships, and human-review items.
- Attach evidence snippets of at most 80 characters; use `Not provided` when no reliable evidence exists.
- Redact phone numbers, email addresses, government IDs, bank-card numbers, common API-key and token forms, authorization headers, passwords, private-key blocks, and user-supplied entity names.
- Flag conflicting owners, deadlines, or statuses for human review.
- Rank actions as P0/P1/P2, synthesize an executive summary, and generate an SVG collaboration-health radar.
- Export the structured card to CSV, Feishu/Bitable mapping JSON, or Notion mapping JSON.

## Input

Accept Markdown, plain text, exported chats, meeting notes, or project logs. Label the source of each segment when combining materials. Optional metadata includes project name, time range, departments, and a list of known entities to redact.

If the material does not state a project name, time range, owner, deadline, or department, use `Not provided`. Do not infer or complete it.

## Workflow

1. Separate facts from opinions, questions, tentative statements, small talk, and duplicates.
2. Draft the seven-module card using the key order in `templates/json-output-schema.md`.
3. Keep owner and deadline values verbatim. If an exact value cannot be found in the supplied source, replace it with `Not provided`.
4. Pass both the model-produced draft JSON and its original source to the deterministic enforcement layer:

   ```bash
   python3 scripts/process.py enforce --card draft-card.json --source source.txt --out enforced-card.json
   ```

   `process.py` does not perform semantic extraction from raw source text. It validates and hardens a draft card. Do not pass it only a source file and expect a card.

   For multiple sources, draft and enforce one card per source, then aggregate the card JSON files. `aggregate` does not accept raw text:

   ```bash
   python3 scripts/process.py aggregate --cards card-1.json card-2.json --entities entities.txt --out aggregated.json
   ```

   Omit `--entities` when there is no user-supplied entity list. Aggregation always reapplies built-in PII and credential redaction.

5. Optionally generate a radar chart:

   ```bash
   python3 scripts/radar_chart.py generate --card enforced-card.json --out collaboration-radar.svg
   ```

6. Optionally export a downstream mapping:

   ```bash
   python3 scripts/export_card.py export-card --card enforced-card.json --format csv --entities entities.txt --out actions.csv
   ```

   Omit `--entities` when no entity list is needed. Every export format reapplies built-in PII and credential redaction before serialization.

7. Return the Markdown card, JSON result, and executive summary. Before publishing or changing the skill, run:

   ```bash
   python3 scripts/process.py selftest
   python3 scripts/radar_chart.py selftest
   python3 scripts/export_card.py selftest
   ```

All file-producing commands require an explicit `--out` path and refuse to replace an existing file unless the user deliberately adds `--force`. Never reuse an input path as an output path.

## Local access boundary

- Read only the exact `--card`, `--source`, `--entities`, or `--cards` paths supplied by the user. Do not enumerate directories or search for other files.
- Do not read environment variables, credential stores, browser data, shell history, or unrelated workspace content.
- Do not use the network or transmit source material. This skill has no MCP or external-service dependency.
- Write only to an explicit `--out` path. Every file-producing command, including exports, requires `--out`.
- Treat `--force` as explicit permission to replace only the named output file. Never infer overwrite permission.

## Output contract

Keep every heading in this order, even when a section contains only `Not provided`:

```markdown
# Collaboration Status Card

## Project Overview
## Progress
## Confirmed Decisions
## Owner × Deadline Actions
## Risks / Blockers / Dependencies
## Cross-functional Relationships
## Human Review Required
## JSON Output
```

Use `templates/collaboration-status-card.md` for the Markdown layout and `templates/json-output-schema.md` for the machine-readable contract.

## Evidence and safety boundaries

- Do not turn tentative intent into a commitment or invent owners, deadlines, decisions, departments, or launch dates.
- Use `Conflict detected; human review required` consistently and add a matching human-review item.
- Sanitize all user-derived Markdown table values and escape CSV formula prefixes.
- Escape SVG titles before rendering them.
- Recompute every evidence snippet from the supplied source; never trust a prefilled evidence field.
- Redact common credential patterns, but do not treat the deterministic redactor as a complete secret scanner. Ask the user to pre-redact live credentials, customer data, and sensitive HR material.
- Do not send messages, email, or calendar invitations, and do not modify Jira, Feishu, Notion, CRM, calendars, or other systems.
- Do not convert interpersonal friction or emotional language into performance judgments or blame.

Illustrative data in the bundled self-tests is synthetic and demonstrates processing behavior only; it is not evidence of a production deployment or business outcome.
