---
name: reviewing-notification-workflows
description: "Reviews a Notifly environment's notification setup: workflows with their steps and channels, topics, and recent delivery activity. Use when the user asks 'which workflows do we have and on which channels', 'what does this workflow do', 'what topics exist', 'audit our notification setup', 'which workflows send SMS', or wants an overview of their notification workflows. Read-only; never sends."
---

# Notifly workflow review

Give the user a clear map of what their Notifly environment sends, on which channels, and how it has been doing.

## Connecting and calling the tools

Every tool in this skill comes from the `notifly` MCP server, the Notifly connector, and is written here as `notifly:<tool>`.

- **Tools listed by name:** call them directly, for example `notifly:list_workflows`.
- **Only `notifly:search_tools` and `notifly:execute_typescript` listed (Code Mode, the default):** call `notifly:search_tools` first, then call each tool inside `notifly:execute_typescript` as `external_<tool>` (for example `external_list_workflows`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `notifly:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects Notifly and approves that scope.
- **No `notifly` tools at all:** Notifly is not connected yet. Install the Notifly power, which adds the server; it signs in with OAuth on first use.

The Notifly server's default surface lists two tools, `notifly:search_tools` and `notifly:execute_typescript`. Call `notifly:search_tools` for the declarations, then call each operation below as `external_<name>(...)` inside a `notifly:execute_typescript` program. Fetch several workflows in one program with `Promise.all` over `external_get_workflow`. A denied call throws an Error whose message starts with its code. If the operations are listed as individual tools instead, call them directly.

## Tools you will use

- `notifly:list_workflows`: the workflows in the connected environment with identifiers, names, tags, and status.
- `notifly:get_workflow`: one workflow's steps, channels, and status.
- `notifly:list_topics`: named subscriber groups used for fan-out.
- `notifly:list_notifications`: recent send events with channels and delivery status.

## Workflow

1. Call `notifly:list_workflows`. Show a table: name, identifier, status, tags.
2. For each workflow the user cares about (all of them if there are only a few), call `notifly:get_workflow` and add its steps in order and its channels to the table.
3. Call `notifly:list_topics` and list the topics by name.
4. Call `notifly:list_notifications` for a recent sample. Count events per workflow and note any channel with failed or skipped deliveries.
5. Point out what the data shows plainly, for example: inactive workflows, workflows with no recent sends, a channel that keeps failing, or a workflow that uses a channel with no recent successful delivery.
6. For one workflow in depth ("what does password-reset do?"), describe its steps in order, the channel of each step, and the payload fields it uses.

## Rules

- Never call `notifly:trigger_workflow` from this skill. If the user wants to send, offer the `sending-notifications` skill.
- The review covers only the environment picked on the consent screen. Say which one when it matters.
- Do not show internal fields such as `_id`, `_environmentId`, `_organizationId`, or `_creatorId` unless the user asks.
- Report only what the tools return. The activity feed is a list of events, not analytics; do not present rates the data does not support.
