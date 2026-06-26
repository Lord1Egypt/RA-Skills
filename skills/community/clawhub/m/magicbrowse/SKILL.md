---
name: magicbrowse
description: Browser automation fallback through the magicbrowse CLI with
  goal-driven act as the default primitive and observe/primitives only for
  recovery, with changed page state verified by fresh observation.
homepage: https://www.npmjs.com/package/@mercuryo-ai/magicbrowse-cli
metadata:
  openclaw:
    homepage: https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/openclaw/marketplace/README.md
    requires:
      bins:
        - magicbrowse
    primaryEnv: MAGICPAY_API_KEY
    install:
      - id: npm
        kind: node
        package: "@mercuryo-ai/magicbrowse-cli@latest"
        bins:
          - magicbrowse
        label: Install MagicBrowse CLI (npm)
---

Use `magicbrowse` to reach a target page when your runtime's own
page-control tool cannot do it reliably. "Page-control tool"
means a tool that drives browser pages programmatically and reports page state
back — not the user's desktop browser, and not screen-control of a
browser window. The planner runs two LLM loops per task and is slower
than direct browser control; prefer your own page-control tool
when it suffices. Use `magicbrowse` to *reach* a target page (search, navigation,
traversal through non-sensitive screens). At any login, identity, checkout,
donation, subscription, payment, or human-verification page, stop and surface
to the user — do not invent or type credentials, identity data, payment data,
or any value you do not legitimately have.

For a MagicPay product/payment workflow, use the MagicPay workflow-first
recipe instead of treating a standalone MagicBrowse browser as the product
parent: MagicPay starts the product session, then launches or attaches the
browser as a child resource.

## Fallback Ladder

Try in order. Do not start at layer 4 just because primitives exist.

1. **Your runtime's own page-control tool** — programmatic page
   control owned by your runtime. Screen-control (computer use) of an
   already-open desktop browser does not qualify: takeover needs the
   browser's CDP endpoint, a typical desktop browser starts without one,
   and CDP cannot be enabled on a running browser without a restart. If
   the session may need a MagicBrowse or MagicPay takeover mid-flow,
   start from a browser with a known private CDP endpoint.
2. **`magicbrowse act "<goal>"`** — DOM-only navigator.
3. **`magicbrowse act "<goal>" --use-vision`** — same goal, navigator
   with screenshots. Use only when the user is comfortable sending
   screenshots/page context for this workflow. Vision is a retry mode
   for the same task; keep the granule.
4. **`magicbrowse observe` + primitives** —
   `click <target-id>`, `type <target-id> <text>`,
   `fill <target-id> <value>`, `select <target-id> <option-text>`,
   `press <keys>`. Use only when vision-mode `act` cannot make
   progress, or when single-element precision is required. A primitive
   `completed` result means the direct action ran; it is not a semantic
   proof that the intended page state changed. Re-run `observe` before the
   next decision. `press` is global — `click` first if focus matters.
5. **Surface failure to the user.**

## Preferred Pattern

For public navigation tasks, give `act` the semantic goal and a checkable
terminal condition:

✓ `magicbrowse act "navigate to the public page that lists supported regions and stop when the region list is visible"`

Avoid manually replaying snapshot ids before `act` has failed:

✗ `magicbrowse observe` → `magicbrowse click 13` → `magicbrowse observe` → `magicbrowse click 23`

## Setup Check

1. Run `magicbrowse doctor` first on a fresh install. It verifies the
   gateway config and reachability.
2. If it fails because the API key is missing, run
   `magicbrowse init <apiKey>` (sign up at
   `https://agents.mercuryo.io/signup`).
3. Only proceed to `launch` and `act` once `doctor` passes.

## Hard Rules

> **Consequential actions require approval.** `magicbrowse` may
> navigate, inspect, draft, and prepare. It must stop and ask before
> submitting a form, posting or sending content, accepting terms,
> changing account data or settings, booking, buying, ordering,
> deleting or modifying remote data, or otherwise committing an
> irreversible or account-affecting action. After approval, re-run
> `observe` and execute only the approved final action. A successful typed
> MagicPay approval counts for that exact payment, signing, or confirmation
> action; ask again only if the approved page facts changed.

> **Memory-managed data — never invent.** Do **not** use `act`, `type`,
> `fill`, or `select` for any of the following on any page:
> - login or signup credentials (email, username, password, OTP),
> - identity-document fields (passport, ID, KYC address, DOB tied to
>   identity),
> - payment-card or banking fields (PAN, CVV, expiry, IBAN, account),
> - any value sourced from a Memory or Memory store, or any value you
>   do not legitimately have.
>
> Reach the page, stop before entering Memory values, and return the
> handoff to the orchestrator or MagicPay Memory fill workflow. Do not
> guess, placeholder, or fabricate Memory values. Be honest about what
> you cannot do.

> **Use `act` before snapshot primitives.** Do not start MagicBrowse work
> with `observe` plus `click`/`type`/`select`/`press`/`fill` before
> attempting `act` on the same goal. Why: the navigator keeps the goal,
> current page context, and completion check in one planner loop instead of
> spreading them across fragile snapshot ids. Use primitives only after
> DOM-only and vision-mode `act` cannot make progress, or when the recovery
> step is deliberately single-element.

> **Target-ids are snapshot-scoped.** Valid only for the `observe`
> snapshot that produced them. Re-run `observe` after any primitive that
> may change the page state before the next primitive — reusing an old id
> silently addresses a different element.
>
> ✓ `observe` → `click 12` → `observe` → `type 7 "hello"`
> ✗ `observe` → `click 12` → `type 7 "hello"`

> **Primitive completion is not goal completion.** For deterministic
> `click`/`type`/`fill`/`select`/`press`, `status: "completed"` means the
> browser action was dispatched through the direct action layer. It does not
> certify that a higher-level page condition is now true. If the next step
> depends on changed page state, observe again and branch on the fresh page
> state. If the task itself needs a completion check, use `act` with a
> checkable terminal condition instead of interpreting a primitive result as
> task success.

> **One workflow per default home.** The current-session pointer at
> `$MAGICBROWSE_HOME/current-session.json` (default `~/.magicbrowse/`) is a
> singleton. Concurrent workflows on the same home overwrite each other. For
> parallel use, set a distinct `MAGICBROWSE_HOME` per workflow, or do not run
> the tasks in parallel.

> **Fresh browser by default.** Prefer an owned, fresh browser session.
> Use `attach`, `--profile`, or `--user-data-dir` only when the user
> explicitly approves that browser/session for the current task. One
> exception needs no separate approval: attaching to the browser child
> that MagicPay launched inside the current approved product workflow —
> that is the normal in-workflow bind of an owned disposable browser.
> Keep CDP endpoints private. Close the session before unrelated work.

> **Page context can leave the browser.** LLM-backed `act` sends page
> state to the gateway; `--use-vision` can include screenshots. Avoid
> private pages unless the user approves that workflow, and stop at login,
> identity, checkout, donation, subscription, or payment pages.

## Primary Workflow

Contract: `launch [url] → act … act → close`. Sequential `act` calls in
one session preserve page state and planner memory.

1. `magicbrowse launch <url>` — start a headless owned Chrome session
   pre-placed at the entry URL. Keep browser launches headless unless
   the user explicitly asks for a visible browser or you are doing live
   debugging. To attach to an existing CDP browser instead, first get
   explicit user approval for that endpoint/session:
   `magicbrowse attach <cdp-url-or-ws-endpoint>` (positional, not a
   `--cdp-url` flag).
2. `magicbrowse act "<goal>"` — natural-language browser step. Prompt is
   **positional**. `act` does **not** take `--url`; you cannot reset
   the page from inside `act`. To re-anchor, `close` and `launch` again.
3. Repeat `act` for the next strategic granule.
4. `magicbrowse close` — release the session when the overall
   MagicBrowse-owned browser task is done. If the workflow hands off to
   another tool or the user on a sensitive page, keep the browser open until
   that handoff completes. After the handoff completes, close only a
   MagicBrowse-owned disposable browser that the user is not taking over; do
   not close an external/user-owned attach without explicit approval.

`magicbrowse run` exists in the CLI for one-shot developer use. **It
is not part of this skill contract** — its bundled `close` destroys
continuity. Do not use it in an orchestrated workflow.

## Goal Granularity

1. **Granule = atomic strategic segment.** End each `act` where the
   orchestrator needs the next strategic decision. Tactics (which form
   field first) live inside `act`; strategy (this partner is wrong, try
   another) lives between `act` calls.
2. **Target horizon: 15-30 navigator steps per `act`; smaller is
   safer.** `maxSteps: 100` is a safety ceiling. The planner
   self-validates terminal status, so longer tasks have more room for
   false-positive completion. Prefer smaller granules when the success
   criterion cannot be checked externally.
3. **Auth walls and CAPTCHA are hard boundaries, not obstacles.** A
   task that reaches auth, CAPTCHA, or human verification ends with
   `status: needs_handoff`, not `failed`. Plan tasks to end *at* such
   a wall, not through it. `magicbrowse` does not solve CAPTCHA and
   does not enter credentials. For a confirmed real CAPTCHA on the current
   approved browser session, have the user or an external solver clear it;
   after a successful solve, run `magicbrowse mark-captcha-resolved` before
   the next `act`. Branch on `handoff.kind`: `captcha` means solve/mark,
   `auth` means stop for user authentication, `identity_verification` means
   stop for user/KYC handling, and `memory_fill` means hand off to the
   MagicPay Memory fill workflow. Memory-fill handoffs include
   `resumeObjective`; after the approved handler fills the form, continue
   with that page-local objective. Never retry the same `act` against the
   same wall. If the page asks for something you cannot legitimately
   provide, be honest about it.
4. **Rely on session memory; do not re-narrate.** Sequential `act`
   calls in one session preserve page state and planner memory. Do not
   write "as we already found, continue with…" into goals — if you
   feel the need to, the granularity is wrong.

## Goal Formulation

1. **No element indexes or selectors in goal text.** Indexes renumber
   on every DOM scan. Describe elements semantically.
   - ✗ `act "click target 14"`
   - ✓ `act "click the 'Continue' button under the price summary"`
2. **Describe the expected terminal state where it adds a checkable
   criterion.**
   - ✗ `act "get to checkout"`
   - ✓ `act "navigate to a checkout page that shows passenger fields and total fare"`
3. **Pass the starting URL to `launch`, not as a separate step.** To
   switch sites mid-workflow, either `close` and re-`launch`, or
   describe the navigation inside the goal text.

## Common Mistakes

> - Element indexes (`[14]`, `target 7`) in goal text.
> - `magicbrowse run` for orchestrated multi-step workflows.
> - `type` / `fill` / `select` / `act` on Memory-managed fields. Stop at
>   the form boundary; if `act` returns a memory-fill handoff, send it to
>   the orchestrator or MagicPay Memory fill workflow and then resume with
>   `handoff.resumeObjective`.
> - Letting `act` submit, post, book, buy, save, delete, or otherwise
>   commit an account-affecting action without explicit approval or a matching
>   typed MagicPay approval for unchanged page facts.
> - Trying to solve CAPTCHA through `magicbrowse`. On a confirmed real
>   CAPTCHA, have the user or an external solver clear it, then
>   `magicbrowse mark-captcha-resolved` before the next MagicBrowse step.
> - Attaching to a logged-in browser or named profile without explicit
>   approval for the current task.
> - Closing a browser that was handed to another tool or the user before the
>   overall task is actually done.
> - Re-narrating prior `act` results into the next goal — sequential
>   `act` calls keep state.
> - Skipping the `act`-first path and starting at layer 4
>   (observe + primitives).
> - Reusing a target-id from before a page mutation.
> - Treating a deterministic primitive's `completed` status as proof that
>   the intended page state changed.

## Status and Errors

`act` returns `status: completed | blocked | needs_handoff |
needs_approval | failed | max_steps | cancelled`. Branch on `status`;
do not parse `finalMessage` to detect missing input, Memory
handoff, handoff subtype, or approval stops. For `blocked`, branch on
`blockedReason: missing_input | item_unavailable | ambiguous | no_path`.
For `needs_handoff`, branch on
`handoff.kind: memory_fill | captcha | auth | identity_verification`.

Layer-4 primitives return direct action results. Branch on their `status`
and `reason`, but verify page-state assumptions with a fresh `observe`;
primitive `completed` is not a substitute for a goal-level completion check.
`finalMessage` is the explanation to show the user or pass upstream.
Memory-fill handoff details are in `handoff.resumeObjective`. Exit
code `0` includes `blocked`, `needs_handoff`, and `needs_approval`; it
does not mean success.
See [references/statuses.md](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/statuses.md).

## References

- [references/commands.md](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/commands.md) — every CLI command.
- [references/workflow.md](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/workflow.md) — worked end-to-end
  example.
- [references/guardrails.md](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/guardrails.md) — long-form hard
  rules.
- [references/statuses.md](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/statuses.md) — outcome codes and
  status handling.
