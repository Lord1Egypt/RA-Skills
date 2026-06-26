---
name: openclaw-browser
description: Use the OpenClaw-managed browser for real website interaction, page operations, snapshots, clicks, typing, waits, screenshots, and tab control. Use when the user wants to open a website, operate a webpage, log in, fill forms, inspect page state, or use a dedicated browser profile instead of a generic browser or standalone Playwright/Puppeteer flow.
---

# OpenClaw Browser

Use this skill whenever a task needs a **real browser** under OpenClaw control.

This skill is for:
- opening websites in a managed browser
- operating pages with click/type/wait flows
- using browser snapshots and refs
- keeping browser sessions isolated by profile
- checking tabs, status, screenshots, requests, and errors

This skill is **not** for:
- simple web search that can be answered with search/fetch tools alone
- launching a random system browser window with no automation follow-up
- bypassing OpenClaw browser via standalone Playwright/Puppeteer unless the user explicitly asks

## Core rule

When real browser automation is needed, prefer the **OpenClaw-managed browser flow**.
Do **not** default to:
- the system default browser
- ad-hoc Chrome launches
- standalone Playwright/Puppeteer
- another agent's shared browser profile

## Interface priority

Prefer the highest-level OpenClaw browser surface available in the current environment:

1. **Built-in `browser` tool** when the runtime exposes it
2. **`openclaw browser` CLI** when the CLI is available

Official CLI form:

```bash
openclaw browser --browser-profile <profile> <subcommand> ...
```

The rule is not "use this exact shell string at all costs". The real rule is:
- stay inside the **OpenClaw browser control surface**
- use an explicit profile when possible
- do not fall back to a generic unmanaged browser flow

## Local debugging note

The OpenClaw browser system is backed by a loopback control service. For normal work, use the browser tool or CLI first. Raw HTTP access is mainly for local debugging/integration, not the default operator workflow.

## Built-in browser tool guidance

If the runtime exposes the OpenClaw `browser` tool, prefer it over shelling out.
Use the tool's browser operations with an explicit `profile` whenever possible.
Typical operation sequence is the same:
- status
- start
- open / navigate
- snapshot
- act (click/type/hover/select/drag)
- wait
- screenshot / requests / errors for debugging

The same profile rules in this skill still apply when using the built-in tool.

## Profile policy

### Default behavior

Always choose an explicit browser profile when possible:

```bash
--browser-profile <profile>
```

### Preferred profile order

1. **Current agent's dedicated configured profile**
2. **Task-specific profile explicitly requested by the user**
3. **Configured OpenClaw default profile**
4. **`openclaw`** as the safe fallback

### Profile rules

- Prefer a **dedicated profile per agent / workflow / long-running task**.
- Do not assume arbitrary profile names exist; prefer already-configured profiles.
- If no dedicated configured profile is known, use `openclaw`.
- Do not reuse another agent's profile unless the user explicitly wants shared state.
- Use `user` only when the task truly needs the user's signed-in browser session and the user is present to approve attach prompts.

### Naming guidance for dedicated profiles

If the environment already supports multiple configured profiles, prefer names that identify ownership or scope, for example:
- `agent-main`
- `agent-research`
- `shopify-ops`
- `session-foo`

But do **not** invent and rely on a new profile name unless it is actually configured.

## What OpenClaw browser is

OpenClaw browser is a managed browser system with:
- isolated browser profiles
- deterministic tab control
- snapshots that return action refs
- page actions such as click/type/hover/select/drag/wait
- screenshots, requests, console, errors, cookies, storage, and downloads

The browser is controlled through OpenClaw's local browser control service. The service is loopback-only and its port family is derived from `gateway.port`. Profile CDP ports are also managed by OpenClaw. Normally, **do not hardcode raw ports for normal work**; use the OpenClaw browser CLI/tool surface first.

## Standard operating procedure

### 1) Check status

```bash
openclaw browser --browser-profile <profile> status
```

### 2) Start the browser if needed

```bash
openclaw browser --browser-profile <profile> start
```

### 3) Open the target page

```bash
openclaw browser --browser-profile <profile> open <url>
```

### 4) Take a snapshot before acting

```bash
openclaw browser --browser-profile <profile> snapshot
```

For dense pages, prefer interactive snapshots:

```bash
openclaw browser --browser-profile <profile> snapshot --interactive
```

### 5) Operate using refs from the snapshot

Examples:

```bash
openclaw browser --browser-profile <profile> click <ref>
openclaw browser --browser-profile <profile> type <ref> "hello" --submit
openclaw browser --browser-profile <profile> wait --text "Done"
```

### 6) Re-snapshot after navigation or large DOM changes

Refs are not stable across navigations. If an action fails or the page changed, take a fresh snapshot and use the new refs.

## High-value commands

### Browser / tabs

```bash
openclaw browser --browser-profile <profile> tabs
openclaw browser --browser-profile <profile> tab
openclaw browser --browser-profile <profile> focus <targetId>
openclaw browser --browser-profile <profile> close <targetId>
```

### Inspection

```bash
openclaw browser --browser-profile <profile> snapshot --interactive
openclaw browser --browser-profile <profile> screenshot
openclaw browser --browser-profile <profile> console --level error
openclaw browser --browser-profile <profile> errors
openclaw browser --browser-profile <profile> requests --filter api
```

### Actions

```bash
openclaw browser --browser-profile <profile> navigate <url>
openclaw browser --browser-profile <profile> click <ref>
openclaw browser --browser-profile <profile> type <ref> "text"
openclaw browser --browser-profile <profile> hover <ref>
openclaw browser --browser-profile <profile> select <ref> <value>
openclaw browser --browser-profile <profile> press Enter
openclaw browser --browser-profile <profile> wait "#main" --url "**/dashboard" --load networkidle
```

## Decision rules

### Use OpenClaw browser when
- the task needs a real logged-in or stateful browser session
- the task needs clicking, typing, file upload, downloading, or page verification
- the task needs deterministic tab control or screenshots
- the task should stay isolated in a dedicated browser profile

### Use `user` profile only when
- the task truly requires the user's live signed-in browser state
- the user is at the computer to approve browser attach prompts
- the increased risk of acting in the user's real session is acceptable

### Do not switch away from OpenClaw browser just because
- a page looks dynamic
- you want raw selectors
- another automation stack feels more familiar

First try the OpenClaw browser flow properly: status → start → open → snapshot → act → re-snapshot.

## Debugging workflow

If something fails:

1. Run a fresh interactive snapshot.
2. Use the newest ref.
3. If targeting is unclear, use `highlight <ref>` or `screenshot`.
4. Inspect `errors` and `requests`.
5. If the page navigated or rerendered, re-snapshot.

Useful commands:

```bash
openclaw browser --browser-profile <profile> highlight <ref>
openclaw browser --browser-profile <profile> screenshot --full-page
openclaw browser --browser-profile <profile> errors --clear
openclaw browser --browser-profile <profile> requests --filter api --clear
```

## Anti-patterns

Avoid these unless the user explicitly asks:

- launching a generic browser with no OpenClaw control path
- mixing one agent's task into another agent's profile
- assuming refs remain valid after navigation
- skipping snapshots and guessing actions blindly
- bypassing OpenClaw browser with standalone Playwright/Puppeteer for ordinary website work
- hardcoding raw browser control ports for normal usage when the CLI/tool already exposes the operation

## Minimal quick-start template

```bash
PROFILE=<configured-profile-or-openclaw>

openclaw browser --browser-profile "$PROFILE" status
openclaw browser --browser-profile "$PROFILE" start
openclaw browser --browser-profile "$PROFILE" open https://example.com
openclaw browser --browser-profile "$PROFILE" snapshot --interactive
```

## Success criteria

A correct OpenClaw browser workflow should usually show all of the following:
- browser status can be queried
- a target page can be opened in the selected profile
- snapshot returns page structure with refs or a readable page tree
- at least one follow-up action such as click/type/wait/screenshot works in the same profile

If these are true, the page is being controlled through the proper OpenClaw browser path.
