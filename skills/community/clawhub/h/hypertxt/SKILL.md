---
name: hypertxt
description: Operate Hypertxt articles and Google Search Console through the Hypertxt MCP server. Use when an agent needs to inspect credits, projects, article templates or drafts; find content opportunities in GSC; generate an article; review or change editorial state; export content; or create a CMS draft or live publication.
---

# Hypertxt

Use Hypertxt as a controlled content-operations layer. Prefer discovery and
inspection before generation, state changes, GSC refreshes, or publishing.

## Preflight

1. Confirm that `account_status` and `list_projects` are available from the
   Hypertxt MCP server.
2. If they are missing, stop and direct the user to
   `https://www.hypertxt.ai/guides/openclaw/`. Do not invent configuration.
3. Never request or echo a Hypertxt API key. Tell the user to store it as
   `HYPERTXT_API_KEY` in the client's environment or secret configuration.
4. Call `account_status` before proposing generation. Report the plan and
   remaining article credits.
5. Discover IDs with list tools. Never guess a project, article template,
   article, GSC connection, or publishing destination ID.

## Permission boundary

Treat these as read-only:

- `account_status`
- `list_projects`
- `list_workflows`
- `list_articles`
- `get_article`
- `export_article`
- `list_integrations`
- `list_gsc_connections`
- `query_gsc`

Obtain explicit user approval immediately before each of these actions:

- `generate_article`: spends one article credit.
- `change_article_state`: records an editorial decision.
- `sync_gsc`: queues a durable refresh.
- `publish_article`: writes to a connected destination; live mode publishes.

Approval for one action does not authorize later actions. Never infer approval
to publish from approval to generate or review.

## Find an opportunity with GSC

1. Call `list_projects`.
2. Call `list_gsc_connections` for the selected project.
3. Call `query_gsc` with a clear grouping and filters.
   - Omit dates for the latest synchronized snapshot.
   - Supply `start_date` and `end_date` for an exact live window.
4. Rank opportunities from returned clicks, impressions, CTR, and position.
   Distinguish observed metrics from editorial inference.
5. Present a proposed title, primary keyword, audience, search intent, and
   brief. Do not generate yet.

## Generate an article

1. Call `account_status` and require at least one article credit.
2. Call `list_workflows` for the selected project.
3. Present the exact project, article template, title, keyword, brief, and
   one-credit cost.
4. Ask for explicit approval.
5. Call `generate_article` once.
6. Report the returned article ID and state. Use `get_article` or
   `list_articles` to monitor; do not repeat generation when status is queued.
7. If Hypertxt returns HTTP 402, report that no article or task was created.

## Review and change state

1. Call `get_article` and inspect the complete content.
2. Summarize material editorial issues and recommend a decision.
3. Ask for approval before `change_article_state`.
4. Explain that `reviewed` and `approved` map to `ready`; `posted` maps to
   `published` as a manual state record and does not contact a CMS.
5. Report the article ID, previous state, and confirmed new state.

## Publish

1. Call `get_article`; require reviewed, ready content.
2. Call `list_integrations` and name the exact destination.
3. Ask whether to create a destination `draft` or publish live.
4. State the article ID, destination, and mode in the confirmation.
5. Call `publish_article` once after approval.
6. Report the returned external URL and final state when present.

A destination draft keeps the Hypertxt article ready. Live publishing changes
it to published. Do not describe a destination draft as publicly posted.

## Finish every workflow

Report:

- project and article IDs used;
- GSC window and filters, when applicable;
- credit count before generation;
- actions performed and actions deliberately not performed;
- current article state and destination URL, when applicable;
- any remaining approval or setup step.

