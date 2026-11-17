---
name: onimi-pages
description: Create and edit Onimi Pages or Slides, validate and preview the result, save private drafts, and publish or manage controlled sharing when requested. Use for Onimi works and local artifacts intended for Onimi.
license: MIT-0
metadata:
  version: "0.3.2"
---

# Onimi Pages

Help the user turn materials into a Page or editable Slides, continue the same work,
and return a verified result. Local creation needs no account. Installation,
connection, draft saving and publication are separate outcomes.

## Choose the task

Read only the guidance needed for the user's request:

- Create or edit a Page, use a scenario/resource, validate or preview: read
  [create.md](references/create.md). For Slides also read [slides.md](references/slides.md);
  for shared group state or individual submissions read [controlled-data.md](references/controlled-data.md).
- Save a private cloud draft, restore a revision, publish an update, or manage
  controlled sharing: read [publish.md](references/publish.md). For byte-exact uploads
  read the draft upload section of [create.md](references/create.md).
- Install, connect or recover expired authorization: read
  [installation.md](references/installation.md), or
  [installation.zh-CN.md](references/installation.zh-CN.md) in Chinese.
- Migrate an old Creator/Publish installation: read [migration.md](references/migration.md).

Locate an existing work by the user's full project name first. Pass `projectName`
only when the discovered tool schema advertises it; older services resolve the name
through the authorized project list and use its verified internal ID. Follow the
schema-aware, exact-name, duplicate-name and missing-name recovery rules in
[publish.md](references/publish.md#connect-and-select-the-target). Keep the resolved
ID for later writes, chunks and retries so a rename cannot select another work.

Keep the user's existing project, draft/release history, visibility and grants when
editing. A generic publish request does not select a new project. Creation and draft
saving do not authorize publication. An explicit request to publish remains valid
through the required checks; do not ask for the same choice again.

Before cloud work, use the existing `onimi-pages` MCP connection at
`https://onimi.ai/mcp`. Reuse a valid same-account connection whose effective scopes
cover the task. Otherwise explain the needed access and let the user approve browser
OAuth. Never request tokens or click consent for the user. Keep the local artifact
and resume the same task after authorization.

Before multi-step cloud writes, use `scripts/task-state.mjs` as described in
[publish.md](references/publish.md). Retain exact mutation IDs and fixed references
for uncertain retries; reconcile actual server receipts before claiming success.
Private source, credentials and one-time access secrets stay outside the Skill and Git.

Validate the complete artifact and audience before publishing. Keep controlled-cloud
works private. Report only the saved/published revision and access that the server
actually confirms. If a required tool, scope or transfer is unavailable, preserve the
artifact and explain the next recoverable action.

The current Agent's plugin or Skill installation channel owns updates. Do not interrupt
creation or publishing to check for updates. Never update automatically: preserve personal
changes and use that channel's supported flow only when the user requests an exact reviewed
version. This source package contains no direct-download receipt or update manager.
