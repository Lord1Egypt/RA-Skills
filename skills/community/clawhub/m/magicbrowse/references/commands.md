# MagicBrowse Command Guide

Full reference for the `magicbrowse` CLI. The skill workflow uses
`launch`, `act`, `observe`, `click`/`type`/`fill`/`select`/`press`,
`mark-captcha-resolved`, and `close`. Agent setup uses
`magicbrowse init`, then `doctor`. Everything else is for diagnostics,
compatibility, or one-shot developer use.

The hard rules from `SKILL.md` apply to every command: use a fresh
browser by default, get explicit approval before using an existing
profile/CDP session, stop before consequential actions unless a matching typed
MagicPay approval covers unchanged page facts, and stop at memory fills —
never invent or placeholder Memory data.

## Setup And Readiness

### `magicbrowse init <apiKey> [--api-url <url>]`

Writes the gateway config used by LLM-backed `act`. When `--api-url` is
provided, it also stores the gateway base URL. Omit `--api-url` for normal
setup; pass `--api-url <url>` only for a non-default staging, self-hosted, or
test gateway.

Current CLI compatibility note: the persisted config path and environment
override names still use the existing `~/.magicpay/config.json`,
`MAGICPAY_API_KEY`, and `MAGICPAY_API_URL` names. Treat these as gateway
configuration names, not memory-fill ownership.

Exit codes: `0` on success, `1` if `<apiKey>` is missing.

### `magicbrowse doctor`

Verify the gateway config and reachability. Use this as the preflight
before `launch` and `act`.

Exit codes: `0` if config is healthy, `1` if not.

### `magicbrowse browser-status`

Inspect live browser/page/runtime state. Use for diagnostics only.

Exit code: `0`.

## Session Lifecycle

### `magicbrowse launch [url] [--headful] [--profile <name>]`

Start an owned Chrome session and persist it as the current session.
The URL is **positional and optional**. Headless is the default;
`--headful` is a debug/visible-browser override. Use it only when the
user explicitly asks for a visible browser or a live debugging protocol
requires it; do not add it to normal agent workflows or examples.
Advanced flags (`--user-data-dir`, `--chrome-path`, `--user-agent`)
accept overrides for non-default Chrome layouts.

Prefer a fresh owned profile. Use `--profile` or `--user-data-dir`
only after the user explicitly approves that browser state for the
current task.

Exit code: `0`.

### `magicbrowse attach <cdp-url-or-ws-endpoint>`

Attach to an existing CDP browser as the current session. The
endpoint is **positional**, not a `--cdp-url` flag.

Only attach to a private endpoint that the user provided or explicitly
approved for the current task. Treat CDP endpoints as sensitive because
they inherit the authority of that browser session. Attaching to the
browser child that MagicPay launched inside the current approved product
workflow is the normal in-workflow path and needs no separate approval;
the approval requirement targets external or user-owned browsers.

Exit codes: `0` on success, `1` if the endpoint is missing.

### `magicbrowse close`

Close or detach the current session. Always returns `0`.

Use this only when the overall browser workflow is done or recovery requires
teardown. If the current page was handed to another tool or the user, wait for
that handoff to finish before closing a MagicBrowse-owned disposable browser.
Do not close an external/user-owned attach without explicit teardown approval.

## Natural-Language Browser Step

### `magicbrowse act "<prompt>" [--max-steps <n>] [--use-vision] [--format <fmt>]`

Run one natural-language browser step on the current session. The prompt is
**positional** (use double quotes for any prompt with spaces). `act`
does **not** take `--url`.

Use `act` for navigation, inspection, drafting, and preparation. If
the next step would submit a form, post or send content, accept terms,
change account data/settings, book, buy, order, delete, save, or
otherwise commit an irreversible/account-affecting action, stop and
ask for explicit approval. After approval, re-run `observe` and do
only the approved final action. A matching typed MagicPay approval counts for
the exact payment, signing, or confirmation action while page facts stay
unchanged.

Options:

- `--max-steps <n>` — override the navigator step ceiling (default 100).
- `--use-vision` — include screenshots in the navigator's view. Use as
  a retry mode for the same goal only when the user is comfortable
  sending screenshots/page context for this workflow.
- `--format <human|text|json>` — output format. `json` emits JSON
  Lines suitable for an orchestrator. Default is `human`.

Exit codes (mapped from the act `status` field):

- `0` — `completed`, `blocked`, `needs_handoff`, or
  `needs_approval`.
- `1` — `failed` or missing prompt or missing gateway config.
- `2` — `max_steps` (planner did not converge before the step ceiling).
- `130` — `cancelled` (e.g. SIGINT).

`blocked`, `needs_handoff`, and `needs_approval` are controlled
browser-task stops, not runtime failures. Branch on `status`, then on
`blockedReason` or `handoff.kind` when present; use `finalMessage` only
as the explanation to show the user or upstream orchestrator.

### `magicbrowse mark-captcha-resolved [--ttl <s>]`

Record that a real CAPTCHA on the current active page was solved by an
external participant. This command does not solve CAPTCHA, click a CAPTCHA
widget, or prove success. It writes a one-shot trusted marker into the
current session, bound to the active page identity. The next `act`
consumes the marker, passes it to the planner/navigator as evidence that
a previously visible CAPTCHA was solved out-of-band, then clears it.

**Not part of the skill workflow.** The default `magicbrowse` contract
on a CAPTCHA is *stop and surface to the user* (`status:
needs_handoff`). This command is a low-level CLI primitive for hosts
that have their own out-of-band solver approved by the user and want
to record that fact for the next `act`. Only call after a real CAPTCHA
on the current page has actually been solved externally. The marker
does not bypass page state: if the next `act` still sees a CAPTCHA, the
planner returns `needs_handoff` again, meaning the solver did not
actually clear the wall. Do not re-mark in that case; surface to the
user.

The marker auto-clears without error in three cases:

- consumed by the next `act` (normal one-shot path);
- TTL elapsed before the next `act` ran (default 300 seconds; override
  with `--ttl <s>`, positive integer);
- the active page identity at `act` time does not match the page
  identity recorded when the marker was written (the page changed in
  the meantime).

Exit codes: `0` on success, `1` on missing/invalid `--ttl`, an
unexpected positional argument, no current session, or runtime error.

## Deterministic Primitives (Layer 4)

All take a `<target-id>` from the most recent `observe`. Target-ids
are bare integers from `[N]<type>text</type>` lines. They are scoped
to that single snapshot — re-run `observe` after any primitive that may
change the page state.

Primitive `status: "completed"` means the direct action ran. It is not a
goal-level completion check and does not prove that the intended page state is
now true. If the next step depends on changed page state, use a fresh
`observe` result before deciding what to do next.

### `magicbrowse observe`

Print the current public page snapshot (`plannerView`). Does not
accept a prompt or any positional argument. Stdout carries the human
snapshot; stderr carries a one-line summary of fillable target counts.

Exit codes: `0` on success, `1` if any positional argument is passed.

### `magicbrowse click <target-id>`

Click an observed action target.

### `magicbrowse type <target-id> <text>`

Type text into an observed text target. `<text>` is the rest of the
command line; quote it if it contains spaces or shell metacharacters.

### `magicbrowse fill <target-id> <value>`

Fill (replace) the current value of an observed text target.

### `magicbrowse select <target-id> <option-text>`

Select a native `<select>` option by visible label.

### `magicbrowse press <keys>`

Send a key chord to whatever the browser currently considers focused.
**Not target-scoped**: there is no way to address a specific element.
`click` an element first if focus matters. Examples: `Enter`,
`Tab`, `Control+A`.

All primitives:

- Return `0` on success and `1` on missing arguments.
- Emit a JSON action result on stdout (blocked or executed).
- Report direct action execution only; use `observe` or `act` when the
  orchestrator must verify page-state change.
- Inherit the same approval boundary as `act`; do not click/press the
  final submit, save, delete, buy, book, accept, or send control unless
  the user explicitly approved that exact action or a matching typed MagicPay
  approval covers the unchanged page facts. Re-observe the page first.

## Developer / One-Shot Compatibility

### `magicbrowse run --url <url> --goal "<goal>" [--use-vision]`

**Forbidden in orchestrated workflows.** Compatibility wrapper for
`launch + act + close`. The bundled `close` destroys session
continuity and persistent agent state, so it is documented here only
for one-shot developer use through `--help`. Hosts running a
multi-step skill workflow must use `launch [url] → act … act → close`.

Exit codes follow `act`.

## Environment Variables

- `MAGICPAY_API_KEY` — API key for the gateway, alternative to
  `magicbrowse init`.
- `MAGICPAY_API_URL` — override the bundled default gateway base URL.
- `MAGICBROWSE_HOME` — root for per-run records and the singleton
  `current-session.json` (default `~/.magicbrowse`). Set distinct
  values per workflow for multi-tenant or parallel use.

## Updating The CLI

If `magicbrowse --version` is missing or outdated, run
`npm i -g @mercuryo-ai/magicbrowse-cli@latest`, then verify with
`magicbrowse --version`.
