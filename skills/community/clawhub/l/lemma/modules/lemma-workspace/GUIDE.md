---
name: lemma-workspace
description: "Use for Lemma workspace execution: persistent sessions, dev servers, preview URLs, browser automation, workspace-local CLI usage, and showing live services correctly."
---

# Lemma Workspace

Use this skill when the task is happening inside a workspace session and you need to drive terminals, servers, browsers, or workspace-local tooling correctly.

## When To Use This Skill

Use `lemma-workspace` when the work involves:

- a long-lived terminal session
- a dev server or watcher
- a stateful REPL
- browser automation inside the workspace
- public preview URLs for workspace services
- showing a live service to the user with `show_widget`

## Core Rule

Prefer one persistent workspace session over many disconnected commands when the task involves:

- a dev server
- a REPL
- a long-running watcher
- browser state you want to preserve

Use `exec_command(..., tty=true)` to start the session, keep the returned `session_id`, and use `write_stdin` to continue interacting with it.

## Workspace Environment

Workspace sessions already inject the canonical environment variables:

- `LEMMA_TOKEN`
- `LEMMA_BASE_URL`
- `LEMMA_ORG_ID`
- `LEMMA_WORKSPACE_URL`
- `LEMMA_POD_ID` for pod-scoped sessions only

Use these directly instead of inventing custom bootstrap setup.

## Canonical Patterns

### Keep a shell alive

```json
{
  "cmd": "bash",
  "tty": true,
  "yield_time_ms": 300,
  "max_output_tokens": 3000
}
```

Then continue through the same session with `write_stdin`.

### Use a stateful REPL

Use a persistent shell or Python REPL whenever the work needs state to survive across calls.
Do not restart a fresh one-shot process for each step.

## Preview URL Pattern

If a service listens on port `3000`, the public URL on Kubernetes workspaces is:

```text
https://port-3000-${LEMMA_WORKSPACE_URL#https://}
```

Inside the workspace container, keep using `http://127.0.0.1:<port>`.
Local Docker workspaces may not support the same public preview host pattern.

## Lemma CLI In The Workspace

Inside the workspace, prefer the Lemma CLI when you want backend actions from the current pod context:

```bash
lemma pod get
lemma table list
lemma web search "playwright anti bot headed mode" --limit 5
lemma web search-agent "Summarize the current browser automation tradeoffs for dynamic sites"
```

If the workspace already has the canonical env vars, you usually do not need to pass them explicitly.

## Sandbox Network Troubleshooting

When provisioning or tests stall on network calls, diagnose fast and escalate quickly.

Common failure signatures:

- `Temporary failure in name resolution`
- `Could not resolve host`
- `ENOTFOUND`
- repeated TLS or connect timeout errors to known-good hosts

Fast checks:

```bash
echo "$LEMMA_BASE_URL"
curl -sS "$LEMMA_BASE_URL" >/dev/null
curl -sS https://example.com >/dev/null
```

Escalation rule:

1. run one fast retry after confirming env vars
2. if DNS/network errors persist and block provisioning or verification, escalate immediately instead of looping
3. request elevated or non-sandbox execution so integration and function smoke tests can continue

## Browser Options

### Playwright CLI

Use `playwright-cli` for straightforward browser tasks.

```bash
playwright-cli open http://127.0.0.1:3000 --browser=chromium
playwright-cli screenshot --filename=/workspace/app-shot.jpg
```

### Headful browser plus noVNC

Use `start-browser` when you need a visible headful Chromium session inside the workspace.
It starts Xvfb, Chromium with CDP on `localhost:9222`, and noVNC on port `6080`.

```bash
start-browser
```

After that:

- the agent controls the browser locally over CDP
- the user can view the session through the noVNC URL

### Crawl4AI

Use `crwl` for quick capture and markdown-first extraction.
Good fit for scraping or summarizing web pages inside the workspace.

```bash
crwl https://example.com -o markdown -O /workspace/example.md
```

## Showing Things To The User

Use `show_widget` with `widget_url` when the user should see a live running HTTP service such as:

- a dev server
- a browser session via noVNC
- a Jupyter notebook
- a dashboard

Pattern:

1. start the service
2. confirm it is actually listening
3. compute the public URL
4. call `show_widget` with `widget_url`

Use `widget_code` instead when you are rendering generated HTML or SVG directly.
For inline widget composition, also read `lemma-widget`.

## Verification Rules

Before sharing a preview URL, confirm the service is really running.
Before treating a browser session as ready, confirm the page loaded or the CDP connection works.
Before surfacing a service to the user, check that the port is reachable.

## Common Mistakes

- starting a fresh shell for every step when state should persist
- sharing a preview URL before the server is ready
- assuming local Docker workspaces support Kubernetes preview URLs
- launching a fresh Chromium instance when a running browser should be reused
- forgetting to save the `session_id` from a long-lived session
- retrying blocked DNS/network calls repeatedly without escalating

## Known CLI Behavior

Read shared CLI behavior notes in [`../lemma-main/references/known-cli-behavior.md`](../lemma-main/references/known-cli-behavior.md).

## Related Skills

Route to:

- `lemma-desks` when the workspace is serving or testing a desk
- `lemma-widget` when the result should be rendered inline instead of shown as a live URL
- `lemma-main` when the question is about platform design rather than workspace execution
