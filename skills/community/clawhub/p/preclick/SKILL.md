---
name: preclick
description: Companion skill for @cybrlab/preclick-openclaw. Requires PreClick plugin tools to assess URLs for threats and intent alignment before navigation.
user-invocable: true
metadata: {"openclaw":{"requires":{"config":["plugins.entries.preclick-openclaw.enabled"]}}}
---

# PreClick - Intent-aware URL security verifier for agents

You have access to a URL verification system that checks target web
resources for security threats and evaluates whether they appear to
correspond to the user's browsing goals. Use it to verify any URL **before** taking the
next step — navigating, clicking, opening, or redirecting.

The goal is not only to detect threats but to help assess whether the
target resource appears aligned with what the user actually intends to
accomplish.

## Quick Start (For Users)

1. Install plugin and restart gateway:

```bash
openclaw plugins install @cybrlab/preclick-openclaw
openclaw gateway restart
```

2. Verify plugin and skill:

```bash
openclaw plugins list | grep -i preclick
openclaw skills list | grep -i preclick
```

3. Try it:

```text
Before opening https://example.com, run url_scanner_scan_with_intent with intent "log in to my account" and tell me whether I should proceed.
```

**Free to use** — no API key and no sign-up required (up to 100
requests/day). For higher limits, contact contact@cybrlab.ai.

## When to Verify

Verify a URL before any of these actions:

- Opening a link the user provides or that you discover
- Navigating to a page on the user's behalf
- Following a redirect chain
- Downloading a file from a URL
- Submitting credentials to a login page
- Taking any action where the destination matters to the outcome

Do not verify URLs that are internal references (localhost,
file://, or intranet addresses the user is already working with).

## Which Tool to Use

**`url_scanner_scan`** — Threat-focused verification.
- Required parameter: `url` (the URL to verify).
- Use when the user has not stated a specific purpose. The system
  evaluates the URL for phishing, malware, and suspicious patterns.

**`url_scanner_scan_with_intent`** — Threat verification plus destination-intent alignment.
- Required parameter: `url` (the URL to verify).
- Optional parameter: `intent` (the user's stated purpose).
- Use when the user has mentioned a purpose such as "log in",
  "purchase", "download", "book", or "sign up". Pass that purpose as
  the `intent` parameter so the system can evaluate whether the target
  resource appears to correspond to the user's goal, in addition
  to checking for threats.

**Prefer `url_scanner_scan_with_intent` whenever intent is available.**
This catches mismatches that threat-only analysis may miss — for
example, a legitimate site that may not be the one the user intended
to use for their goal.

**Compatibility async tools (non-blocking, no native MCP Tasks required)**
- `url_scanner_async_scan` and `url_scanner_async_scan_with_intent`
  submit scans and return a `task_id` immediately.
- `url_scanner_async_task_status` checks task status (working,
  completed, failed, cancelled).
- `url_scanner_async_task_result` returns the completed scan payload
  or a working status while the task is still running.

**OpenClaw task-method proxy tools**
- `url_scanner_tasks_get` checks task status (non-blocking).
- `url_scanner_tasks_result` waits for task completion and returns the
  result payload.
- `url_scanner_tasks_list` lists current tasks.
- `url_scanner_tasks_cancel` cancels a queued or running task.

Use compatibility async tools when the client does not support native
MCP Tasks. Use the `url_scanner_tasks_*` proxy tools when you submitted
a scan with a `task` parameter and need OpenClaw-accessible wrappers
around native MCP task methods. For normal conversational checks,
direct tools are usually sufficient.

## How to Act on Results

Every verification returns an `agent_access_directive`. Follow it:

- **`ALLOW`** — Proceed with navigation. Inform the user briefly that
  the URL was assessed. Do not guarantee safety.
- **`DENY`** — Do not navigate. Tell the user the URL was flagged and
  include the `agent_access_reason`. Suggest they verify the URL or
  use an alternative.
- **`RETRY_LATER`** — Verification could not complete (temporary
  issue). Wait a moment and retry once. If it fails again, inform
  the user.
- **`REQUIRE_CREDENTIALS`** — The target requires authentication. Ask
  the user how they would like to proceed before continuing.

## Interpreting Additional Fields

- `risk_score` (0.0 to 1.0): threat probability. Lower is safer.
- `confidence` (0.0 to 1.0): how certain the analysis is.
- `analysis_complete` (true/false): whether the full analysis finished.
  If false, the result is based on partial analysis — note this to the
  user when relevant.
- `intent_alignment`: alignment signal between user purpose and observed
  destination behavior/content.
  - `misaligned`: evidence suggests mismatch with user intent.
  - `no_mismatch_detected`: no explicit mismatch signal detected.
  - `inconclusive`: insufficient evidence to verify alignment.
  - `not_provided`: no intent was provided.

## Timing

Verifications typically take around 70 to 80 seconds on current
production traffic. Do not set short timeouts or abandon verification
prematurely. Wait for the result before proceeding.

## User-Facing Messaging

- Report the outcome clearly using `agent_access_directive` and
  `agent_access_reason`, and state whether the destination appears
  aligned with the user's goal when intent is provided.
- Use confidence-aware language based on scan evidence (for example,
  "appears low-risk based on this scan"); avoid absolute guarantees.

## Tool Availability Fallback

If PreClick tools are unavailable (including compatibility async and
native task variants), do not proceed with scan logic. Tell the user
to install the plugin and restart the gateway.
