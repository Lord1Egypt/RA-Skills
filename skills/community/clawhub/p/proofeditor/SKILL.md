---
name: proof
description: Web-first skill for working with Proof documents via proofeditor.ai. Use when a Proof URL is shared, when creating collaborative docs in Proof, or when the user wants comments, suggestions, and provenance tracked in a shared doc.
homepage: https://www.proofeditor.ai
---

# Proof

Proof is a collaborative markdown editor for agents and humans. Use the hosted web API at `https://www.proofeditor.ai`.

Every write must include `by: "ai:<agent-name>"` so Proof can track who wrote what.

This skill is web-only. Do not use a local Mac app bridge or `localhost:9847` from this skill.

## Default Behavior

If the user shares a Proof URL:
- Join the doc immediately.
- Show presence right away.
- Read the current state before editing.
- Work in the Proof doc unless the user explicitly asks you to move elsewhere.

When creating new docs, follow this priority order:
1. If persistent instructions already define a Proof default mode, use it.
2. Otherwise default to `collaborative_docs`.

Supported default modes:
- `all_new_markdown`: new markdown artifacts you create go to Proof by default.
- `collaborative_docs`: plans, specs, bug writeups, reports, memos, proposals, drafts, and similar iterative docs go to Proof by default.
- `explicit_only`: only use Proof when the user explicitly asks.

Boundary rules:
- Existing repo-tracked markdown files stay local unless the user explicitly asks to move or share them in Proof.
- Do not silently replace local project docs with Proof links.
- If the task is code-adjacent local documentation, keep it local unless the user asks for Proof.

## Shared URLs And Auth

Shared URL format:

```text
https://www.proofeditor.ai/d/<slug>?token=<token>
```

Use one of:
- `Authorization: Bearer <token>` (preferred)
- `x-share-token: <token>`
- `?token=<token>`

`by` controls authorship. `X-Agent-Id` controls presence identity.

## Existing Proof Docs

When a Proof URL is provided:
1. Extract `slug` and `token`.
2. Join immediately by reading state with `X-Agent-Id` or by posting presence.
3. Read the doc.
4. Reply with a short confirmation like `Connected in Proof and ready.`
5. Then keep working inside Proof.

Read state and show presence on read:

```bash
curl -sS "https://www.proofeditor.ai/api/agent/<slug>/state" \
  -H "Authorization: Bearer <token>" \
  -H "X-Agent-Id: <your-agent-id>"
```

Update presence explicitly:

```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/presence" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "X-Agent-Id: <your-agent-id>" \
  -d '{
    "agentId":"<your-agent-id>",
    "status":"reading",
    "summary":"Joining the doc"
  }'
```

Common statuses: `reading`, `thinking`, `acting`, `waiting`, `completed`, `error`.

## Creating A New Proof Doc

Create a shared document:

```bash
curl -sS -X POST https://www.proofeditor.ai/share/markdown \
  -H "Content-Type: application/json" \
  -d '{"title":"My Document","markdown":"# Hello\n\nFirst draft."}'
```

Save:
- `slug`
- `accessToken`
- `shareUrl`
- `tokenUrl`
- `_links`

When Proof is the default for the task:
1. Create the doc.
2. Return the live Proof link to the user.
3. Join the doc immediately.
4. Keep working there.

## Choosing An Edit Strategy

| Task | Recommended API | Why |
|---|---|---|
| Precise paragraph or section rewrite | `edit/v2` | Block refs plus revision locking |
| Simple append or replace | `edit` | Minimal payload |
| Human-reviewed edits | `ops` | Suggestions and comments in track changes |
| Large rewrite proposal | `ops` + `rewrite.apply` | Produces reviewable changes |

## Snapshot And Edit V2

Get a snapshot:

```bash
curl -sS "https://www.proofeditor.ai/api/agent/<slug>/snapshot" \
  -H "Authorization: Bearer <token>"
```

Apply block operations:

```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/edit/v2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: <unique-key>" \
  -d '{
    "by":"ai:<your-agent-name>",
    "baseRevision":42,
    "operations":[
      {"op":"replace_block","ref":"b3","block":{"markdown":"Updated paragraph."}},
      {"op":"insert_after","ref":"b3","blocks":[{"markdown":"## New section"}]}
    ]
  }'
```

Supported ops:
- `replace_block`
- `insert_before`
- `insert_after`
- `delete_block`
- `replace_range`
- `find_replace_in_block`

## Simple Edit V1

Use this for quick append or replace flows:

```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/edit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "by":"ai:<your-agent-name>",
    "operations":[
      {"op":"append","section":"Notes","content":"\n\nNew note."},
      {"op":"replace","search":"old","content":"new"}
    ]
  }'
```

## Comments, Suggestions, And Rewrites

Primary endpoint:

```text
POST /api/agent/<slug>/ops
```

Compatibility endpoint:

```text
POST /api/documents/<slug>/ops
```

Examples:

```json
{"type":"comment.add","by":"ai:<your-agent-name>","quote":"anchor text","text":"Comment body"}
{"type":"suggestion.add","by":"ai:<your-agent-name>","kind":"replace","quote":"old text","content":"new text"}
{"type":"suggestion.add","by":"ai:<your-agent-name>","kind":"replace","quote":"old text","content":"new text","status":"accepted"}
{"type":"rewrite.apply","by":"ai:<your-agent-name>","content":"# Rewritten markdown"}
```

Use `ops` when you want the human to review changes in track changes.

## Events And Presence

Poll for pending events:

```bash
curl -sS "https://www.proofeditor.ai/api/agent/<slug>/events/pending?after=0" \
  -H "Authorization: Bearer <token>"
```

Ack processed events:

```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/events/ack" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"upToId":123,"by":"ai:<your-agent-name>"}'
```

If you are staying in the loop while a human reviews changes, keep presence updated so the doc shows what you are doing.

## Error Handling

| Error | Meaning | Action |
|---|---|---|
| `401/403` | Bad or missing auth | Re-read token from URL and retry with bearer token |
| `404` | Slug not found | Verify slug and environment |
| `409 PROJECTION_STALE` | Metadata catching up | Re-read `state` or `snapshot`, then retry |
| `409 STALE_REVISION` | Snapshot out of date | Use the fresh snapshot or state and retry |
| `409 ANCHOR_NOT_FOUND` | V1 search anchor missing | Re-read state and choose a tighter anchor |
| `422` | Invalid payload | Fix required fields and schema |
| `429` | Rate limit | Back off and retry with jitter |

Guidelines:
- Re-read state before retries that depend on anchors or revisions.
- Include `by` on every write.
- Prefer `content` and markdown payloads as canonical text input.
- Use `Idempotency-Key` on `edit/v2` requests so retries stay safe.

## Discovery

- Discovery JSON: `https://www.proofeditor.ai/.well-known/agent.json`
- Docs: `https://www.proofeditor.ai/agent-docs`
- Setup: `https://www.proofeditor.ai/agent-setup`
