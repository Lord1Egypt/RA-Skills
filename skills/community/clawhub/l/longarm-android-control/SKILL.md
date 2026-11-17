---
name: longarm-control
description: Use the longarm Android remote-control app through its HTTP API or MCP server. Trigger when the user asks to remotely tap, long-press, swipe, scroll, pinch, rotate, screenshot, inspect screen geometry, show or hide the overlay, open Android apps/intents, run saved or inline batch tasks, inspect batch history/screenshots, or connect an agent to longarm MCP tools.
---

# longarm Control

Use this skill to drive an Android device running longarm. The app exposes HTTP endpoints for gestures, screenshots, overlay state, app/intent launch, and batch task management, plus an MCP server exposing equivalent tools for agents.

## Required Connection Details

Ask the user for any missing values before issuing commands:

- HTTP base URL: `http://<device-ip>:<port>`, shown in longarm after the web server starts.
- Optional bearer token: required only when longarm's "require token" setting is enabled.
- MCP URL/port: shown in longarm if using the MCP server instead of direct HTTP.

The Android device must have longarm running, the relevant server started, accessibility/overlay permissions granted, and network reachability from this machine.

## HTTP Helper

Use `scripts/longarm.sh` for direct HTTP control:

```bash
export LONGARM_URL="http://192.168.1.50:8080"
export LONGARM_TOKEN="la_xxxxx" # omit if token auth is disabled
scripts/longarm.sh status
scripts/longarm.sh screen-info
```

Always run `status` first. It confirms reachability and returns the current Plus state plus the gesture endpoints available on that device.

For positional requests, fetch `screen-info` and compute pixels from the returned width/height. Do not assume resolution. Coordinates use Android screen pixels with origin `(0,0)` at top-left, `x` increasing right, and `y` increasing downward.

## Common Commands

```bash
scripts/longarm.sh screenshot /tmp/longarm.png
scripts/longarm.sh screenshot-grid /tmp/longarm-grid.png 'gridSize=1cm&gridColor=80FF0000&gridWidth=2&scale=true'
scripts/longarm.sh open-app com.android.settings
scripts/longarm.sh open-url https://example.com
scripts/longarm.sh batch-run-file docs/jobs/google-news-explore.json
scripts/longarm.sh batch-status
scripts/longarm.sh batch-history
```

Plus-only gestures are `swipe`, `pinch`, `two-finger-swipe`, and `rotate`. If the device lacks Plus, HTTP returns `403` with `{"error":"Plus subscription required"}` and MCP omits those tools.

## Batch Workflow

Use batch tasks for multi-step automation or repeatable flows. A task contains `name`, optional `variables`, and `steps`. Steps support gestures, screenshots, app/intent launch, overlay show/hide, delays, variable assignment, and loops.

Batch run endpoints return immediately with a `runId` and `status: "processing"`. Poll `batch-history-get <runId>` until the status becomes `finished`, `failed`, or `aborted`. Screenshot steps are saved in history and can be downloaded individually or exported as a zip.

## MCP Workflow

When the user wants an agent/tool client connected to longarm, use the MCP server instead of raw HTTP. Read `references/mcp.md` for available tools and connection behavior. MCP tools are gated by the same Plus state as HTTP.

## References

- Read `references/api.md` for complete HTTP endpoint specs, request bodies, responses, auth behavior, screenshot grid query options, and batch JSON shape.
- Read `references/mcp.md` for MCP server methods and tool names.
- Read `scripts/longarm.sh` when constructing a request not directly covered by a subcommand.
