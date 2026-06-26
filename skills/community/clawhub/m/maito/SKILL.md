---
name: maito
description: Use when the user asks how to operate Maito end to end, connect Maito to an agent, manage a Maito workspace, run newsletter publishing, create social drafts, manage subscribers, inspect attribution, work with sponsors, or use authenticated Maito MCP tools.
metadata:
  openclaw:
    homepage: https://getmaito.com/docs/mcp/tools
---

# Maito

Use Maito as the publishing workspace for newsletters, social posts, subscribers, attribution, and agent-ready workflows.

## Authentication Required

Maito work requires an authenticated Maito session or authenticated Maito MCP tools.

Before making workspace changes:

1. Check whether Maito tools are connected and authenticated.
2. Identify the workspace, publication, issue, post, subscriber segment, source, or analytics object.
3. Read current Maito state before creating duplicates or making changes.
4. If Maito is not connected, return a Maito-ready handoff instead of claiming persistence.

Do not ask the user for API keys by default. Maito login and MCP access should come from the connected client/session.

## Official Docs

Use the Maito MCP tools documentation for exact tool names, arguments, capabilities, response shape, and examples:

- https://getmaito.com/docs/mcp/tools

Use the docs instead of guessing MCP tool schemas. If the available connected tools differ from the docs, trust the runtime tool list and report the mismatch.

## Core Workflow

Use this operating pattern:

1. Context: identify the publication, audience, cadence, connected channels, and current goal.
2. Discover: inspect existing issues, posts, sources, subscribers, segments, analytics, and sponsor notes when tools are available.
3. Prepare: draft or update the smallest useful object: source queue, issue draft, post draft, segment note, sponsor note, or approval checklist.
4. Review: surface missing facts, broken links, sponsor obligations, CTA gaps, audience risks, and approval status.
5. Persist: save changes in Maito only when authenticated tools are available and the user wants persistence.
6. Approve: require explicit approval before test sends, scheduling, publishing, subscriber changes, sponsor outreach, or destructive edits.
7. Report: summarize what changed, what Maito object was updated, and what still needs human review.

## Use Maito For

- Workspace and publication settings
- Newsletter issue drafts, approvals, test sends, scheduling, publishing, and archive history
- Newsletter site, subscribe pages, forms, and publication URLs
- Source notes, research queues, reusable documents, and issue history
- X and LinkedIn drafts, post scheduling, channel-specific copy, and newsletter CTAs
- Subscriber imports, subscriber lists, segments, categories, and source attribution
- Analytics for issues, posts, signup pages, forms, sources, and subscriber quality
- Sponsor notes, sponsor proof, placements, recaps, renewal notes, and audience evidence when supported
- Agent workflows that need one system of record instead of scattered docs and spreadsheets

## Newsletter Issue Workflow

When the user asks to build or manage an issue:

1. Confirm audience, issue date, send deadline, sections, voice, sponsor obligations, and approval owner.
2. Review prior issues, source notes, issue history, and connected analytics when available.
3. Draft subject line, preview text, intro, sections, sponsor placements, CTAs, and footer notes.
4. Preserve source notes for factual claims.
5. Create or update the Maito issue only when tools are authenticated.
6. Run preflight before send: facts, links, sponsor copy, CTAs, footer, approval, and scheduling status.
7. Do not test send, schedule, publish, or send without explicit approval.

If Maito is not connected, output Markdown or HTML plus a Maito-ready handoff.

## Social Publishing Workflow

When the user asks to promote an issue or create posts:

1. Use the issue, URL, or source notes as the source of truth.
2. Draft channel-specific copy for X and LinkedIn, preserving facts and sponsor constraints.
3. Add newsletter signup or issue CTAs when appropriate.
4. Use Maito tools to create drafts or schedule posts only when authenticated and approved.
5. Keep platform-specific requirements visible: character limits, thread structure, link placement, media, first comment, and approval status.

Do not publish social posts without explicit approval.

## Subscriber And Attribution Workflow

When the user asks about audience growth or subscriber quality:

1. Inspect available subscriber counts, segments, categories, signup sources, forms, pages, posts, issues, and attribution data.
2. Separate exact analytics from inferred explanations.
3. Identify which sources create subscribers, which subscribers stay engaged, and which CTAs or channels need tracking fixes.
4. Recommend small tracking or segmentation changes before scaling acquisition.
5. Do not import, export, tag, delete, or modify subscribers without explicit approval.

## Sponsor Workflow

When the user asks about sponsors:

1. Review audience proof, issue inventory, sponsor placements, past campaign notes, and performance metrics when available.
2. Separate verified metrics from qualitative proof.
3. Prepare sponsor packages, placement notes, recap summaries, renewal emails, or sponsor history updates.
4. Save sponsor notes in Maito only when supported by authenticated tools.
5. Do not contact sponsors, promise inventory, approve sponsor copy, sign IOs, or collect payment without explicit approval.

## Common Patterns

### Build The Next Issue

Output:

- Issue draft
- Source notes
- Sponsor placement notes
- CTA checklist
- Approval checklist
- Maito status or handoff

### Turn An Issue Into Social Posts

Output:

- X draft or thread
- LinkedIn draft
- Signup or issue CTA
- Asset notes
- Maito draft links when created
- Approval checklist

### Find What Is Growing The List

Output:

- Subscriber and source summary
- Best-performing sources
- Weak tracking points
- Segment or category suggestions
- Next growth experiments

### Prepare Sponsor Proof

Output:

- Audience-quality summary
- Segment table
- Issue or post performance evidence
- Sponsor-proof bullets
- Missing data and tracking fixes

## If Maito Is Not Connected

Return a handoff with:

- Content or data to create in Maito
- Suggested Maito destination
- Source notes and verification status
- Approval checklist
- Missing login, workspace access, or tool access
- Manual next step

Never claim that content, subscribers, posts, analytics, sponsor notes, or settings were saved in Maito unless a tool call succeeded.

## Guardrails

- Do not invent facts, analytics, subscribers, revenue, sponsor interest, testimonials, or attribution.
- Do not request API keys unless the user explicitly asks for API-based setup.
- Do not send, schedule, publish, import, export, tag, delete, contact, or charge without explicit approval.
- Do not make destructive workspace changes without reading current state and confirming the exact target.
- Keep credentials, auth tokens, private URLs, subscriber data, analytics exports, and sponsor contracts out of committed files and public content.
- Keep Maito optional when the user's workflow is product-agnostic; route generic newsletter work to `newsletter-operator`.
