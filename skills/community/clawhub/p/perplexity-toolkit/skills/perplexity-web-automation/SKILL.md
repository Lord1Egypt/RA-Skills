---
name: perplexity-web-automation
description: |
  Use when the user asks to search Perplexity through a real browser. Automate Perplexity via Kimi WebBridge, extract answers and sources, and preserve task-level session state.
metadata:
  version: "0.5.0"
  requires: ["kimi-webbridge", "webbridge-hygiene"]
---

# Perplexity Web Automation Skill

Automate search and extraction from Perplexity AI (Pro account) via Kimi WebBridge browser control.

## Route boundary

This is the direct-browser execution layer, not the default Perplexity route.
Use it when the user explicitly requests a web page, browser, Chrome, WebBridge,
Kimi WebBridge, opening Perplexity, or continuing the current browser thread.
For an ordinary Perplexity request without that wording, the high-level policy
uses the `perplexity` CLI first. Do not invoke the CLI first when this direct
browser route is explicitly selected.

The global `browser-routing` skill remains the browser decision layer. For a
Perplexity direct-browser request it selects `kimi-webbridge`; load
`webbridge-hygiene` with it. This skill is the Perplexity-specific domain
adapter on top of that generic browser driver.

## Red lines (硬红线)

**Model output never becomes a selector, coordinate, or executable code.**
Text produced by an LLM — or extracted from a page — may only be READ as
evidence. It must never decide where to click, where to type, or what JS to
run. Locators come only from the deterministic probe table and the
element-table heuristics; evidence text is advisory and read-only.

Why: text that names an element can otherwise steer the tool into clicking
the wrong control — an ownership-forgery path caught in review (2026-09-28,
fixed under the WARN adjudication: binding requires query text outside the
composer on a concrete element AND an effect signal). Any future feature
that lets model output choose an action target violates this line and must
stop at review.

zh: 模型/页面输出的文字只能读、当证据；永远不能当选择器、坐标或代码。定位只来自确定性探针与元素表启发式，证据文本仅供参考。

## Named-model verification

A workflow mode is not a named model. If the user asks for K3 or another
specific model, select it through the visible Perplexity model control and read
back the label after selection. Return `selected_model` and
`model_label_verified: true` only when the label is actually visible; otherwise
stop with an unverified result and do not infer the model from answer style.

## Prerequisites

- Kimi WebBridge daemon running (`~/.kimi-webbridge/bin/kimi-webbridge start`)
- Perplexity Pro account logged in (uses user's existing session)
- Serial work uses the resident console session (`perplexity-console`); only a genuinely separate parallel/atomic task gets its own **task-specific** session name (example: `hermes-bot-combination-research`), passed on every command in that task.
- Serial Perplexity operations run in the resident `perplexity-console` **purpose** session; mint a separate `task` session only when the console cannot serve (parallel lanes, atomic close). Session/group policy and the duplicate ladder live in `webbridge-hygiene` (see its `references/group-tab-policy.md`). A Perplexity thread is the website conversation and is not the same thing as either the WebBridge session or the Chrome extension connection.
- Before navigating, call `list_tabs` in the chosen session. Do not interpret an empty tab list as a failure: `{success:true,tabs:[]}` means the bridge is healthy and the session has no tab yet.

## Core Workflow

### 0. Connection precheck (verified 2026-09-05)

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"list_tabs","args":{},"session":"TASK_SESSION"}'
```

Interpret the result before changing anything:

- `success:true` with `tabs:[]` → the Chrome extension handshake is healthy; navigate in this same session.
- `success:true` with existing tabs → reuse the intended tab/session and avoid opening duplicates.
- `no extension connected` → the daemon has no current extension handshake. If the daemon itself is unreachable, start it once with `~/.kimi-webbridge/bin/kimi-webbridge start`, then retry `list_tabs`; if the daemon is reachable but the error persists, ask the user to check the extension connection.
- An extension message such as “already linked” is not a Perplexity thread limit. It usually means an existing daemon/session owns the browser connection or a stale pairing is being reported. Reuse the current task session; never stop/restart/close the user's connection automatically.

A successful `navigate` returning a `tabId`, followed by `list_tabs` showing one active Perplexity tab, is the authoritative connection readback.

### 0a. Observed transients & fixes (from a live run, 2026-09-21)

- **First evaluate after idle can 502**: right after an idle period, the first
  `evaluate` may return a 502 or timeout. **Auto-retry (implemented 2026-09-23)**:
  the WebBridge driver now retries `evaluate` once on timeout/502/connect for
  read-only probes (marked `mutating=False` in the JS snippet dispatch); mutating
  calls (submit clicks, file injects) never retry. If the retry also fails,
  the error propagates to `_js` which falls back to its default value; the empty-probe
  fail-fast gate (`bridge.probe-failed`) triggers after 5 consecutive empty probes,
  surfacing the persistent failure as a rich ConsoleError with a
  `WebBridgeError(.kind)` cause (timeout/http_502/connect/protocol).
- **Duplicate tabs in the resident group**: the `perplexity-console` group can show two tabs for the same thread URL (the ledger tracks only 1; the `attach` gate reporting `tab_count: 2` is tolerated and fill/submit/extract still work). **Global rule: the `webbridge-hygiene` duplicate ladder governs (live `list_tabs` verify first, never trust the ledger alone); the console-specific convention below is the site-level fix for this observed incident.** Dedupe convention: **after the task completes** (never close a tab that is mid-use), prefer `find_tab <old-thread-url>` + `close_tab` to drop the stale tab; otherwise close one duplicate of the current thread. Then `list_tabs` to confirm exactly 1 tab remains, and record the collision + resolution in the closeout report.
- **Optional hardening (implemented 2026-09-23)**: auto-retry one 502 at the evaluate layer (read-only probes only); auto-dedupe tabs at attach; flag ledger(1) vs live(2+) tab-count drift as a duplicate collision.

### 1. Search (Proven 2026-08-29; connection smoke-tested 2026-09-05)

```bash
# Navigate to Perplexity
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://www.perplexity.ai","newTab":true,"group_title":"Perplexity Search"},"session":"TASK_SESSION"}'
# Wait 4s for page load

# Snapshot to get @e refs (use compact JSON for regex)
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"snapshot","args":{},"session":"TASK_SESSION"}'
# Textbox: role="textbox", name="问任何事情..." or "输入 @ 以使用连接器"
# Search button: role="button", name="搜索"

# Click textbox FIRST (required to focus it)
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"click","args":{"selector":"@eNN"},"session":"TASK_SESSION"}'

# Fill query
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"fill","args":{"selector":"@eNN","value":"YOUR QUERY"},"session":"TASK_SESSION"}'
# Returns: {"mode":"contenteditable","success":true,"tag":"DIV"}

# Submit via three-event Enter combo (CRITICAL — single keydown doesn't work)
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const el = document.querySelector(\"[contenteditable]\"); el.dispatchEvent(new InputEvent(\"beforeinput\",{inputType:\"insertText\",data:\"\\n\",bubbles:true,cancelable:true})); el.dispatchEvent(new KeyboardEvent(\"keydown\",{key:\"Enter\",code:\"Enter\",keyCode:13,which:13,bubbles:true,cancelable:true})); el.dispatchEvent(new KeyboardEvent(\"keyup\",{key:\"Enter\",code:\"Enter\",keyCode:13,which:13,bubbles:true,cancelable:true})); })()"},"session":"TASK_SESSION"}'
```

### 2. Wait & Expand

```bash
# Wait 10-15 seconds for answer generation
sleep 12

# Click "查看更多" to expand full answer
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const btns = Array.from(document.querySelectorAll(\"button\")); const more = btns.find(b=>b.innerText.includes(\"查看更多\")); if(more) { more.click(); return \"clicked\"; } return \"no expand button\"; })()"},"session":"TASK_SESSION"}'
```

### 3. Extract Answer

```bash
# Get full answer text from main area
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const main = document.querySelector(\"main\"); return main ? JSON.stringify({text:main.innerText, url:location.href, title:document.title}) : \"no main\"; })()"},"session":"TASK_SESSION"}'
```

### 4. Extract Sources

Keep the direct URLs from the page. Record unavailable, paywalled, or contradictory sources explicitly.

### 4a. Candidate-selection evidence (mandatory for “which is better?”)

When Perplexity is used to compare, recommend, shortlist, or assess maturity/adoption, do **not** ask only for features and links. Put the evidence fields in the Perplexity prompt and extract them separately:

```text
For every candidate, provide direct URLs and an as-of date for:
- GitHub stars/forks and a second adoption signal (package downloads, dependents, registry installs, or public production references)
- latest release and latest commit; contributor concentration and a small issue/PR responsiveness sample
- two independent community discussions: date, net votes/replies, author affiliation, and concrete success/failure evidence
- security/permission model and whether a secret can enter LLM context
- exact unknowns. Do not convert missing data into a ranking.
```

Perplexity's metrics and source labels are discovery leads, not verified facts. For finalists, read the canonical repository/registry/official document, record the metric capture date, and preserve `ui_source_count`, `unique_dom_urls`, and canonical-readback status separately. Do not report “popular”, “active”, “many users”, or “best” without the raw indicator and its scope.

The candidate-vs-verified boundary (Perplexity's answer and source labels are candidate output; a claim becomes verified only after canonical page readback) is defined once in Step 3 (Verification) of the `perplexity-search` skill. Apply that definition; do not restate it here. Note that this skill is the low-level browser layer — a `perplexity` CLI/toolkit route also exists; see the `perplexity-conversational-research` skill for when to prefer it.

```bash
# Click "链接" tab
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const tabs = Array.from(document.querySelectorAll(\"[role=tab]\")); const linksTab = tabs.find(t=>t.innerText.includes(\"链接\")); if(linksTab) { linksTab.click(); return \"clicked\"; } return \"not found\"; })()"},"session":"TASK_SESSION"}'

# Extract all source links
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const main = document.querySelector(\"main\"); const links = Array.from(main.querySelectorAll(\"a[href]\")).map(a=>({text:a.textContent.trim().substring(0,200),href:a.href})).filter(l=>l.href.startsWith(\"http\")&&!l.href.includes(\"perplexity.ai\")&&l.text.length>2); return JSON.stringify(links); })()"},"session":"TASK_SESSION"}'
```

### 5. Follow-up Questions

```bash
# Click a follow-up suggestion (by text content)
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const btns = Array.from(document.querySelectorAll(\"button\")); const target = btns.find(b=>b.innerText.includes(\"FOLLOW UP TEXT\")); if(target) { target.click(); return \"clicked\"; } return \"not found\"; })()"},"session":"TASK_SESSION"}'
```

### 6. New Search (Continue in Same Tab)

Use the same task session and current tab. Click the follow-up textbox first, then use `fill`; do not mutate `textContent` directly because React/editor state may not update.

```bash
# Snapshot again if the @e ref may have changed; use the textbox ref or CSS fallback
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"click","args":{"selector":"@eNN"},"session":"TASK_SESSION"}'

curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"fill","args":{"selector":"@eNN","value":"NEW QUERY"},"session":"TASK_SESSION"}'

# Submit with the three-event Enter sequence from Step 1.
```

## Resident console (recommended for repeat / multi-turn use)

For a fixed group+tab workflow, prefer the toolkit's resident console over hand-driving the raw steps:

```bash
perplexity console ask "query" [--task NAME] [--new-thread] [-f json] \
    [--model NAME] [--wait SEC] [--file PATH] [--judge/--no-judge]   # one task = one thread
perplexity console status                                              # state + live readback
perplexity console threads                                             # recorded task threads
perplexity console selfcheck                                           # canned full-gate run
perplexity console selfcheck --drift | console drift                   # read-only probe drift report (12 probes, never clicks/types)
perplexity console extract [--peek] [--again] [--strict]               # re-read without consuming / strict
```

Granular steps (intent composition — added 2026-09-21). The composite `ask` and the step commands share ONE implementation per step; each step is also callable alone and composes through a staged-turn ledger (`state.json → pending`):

```bash
perplexity console open <task|url> [--new-thread]                # re-attach / switch threads; `open <url>` binds the NEXT fill/ask to that thread (one-shot, consumed at extract — it continues the opened page instead of starting a new thread)
perplexity console fill "q" [--task T] [--new-thread] [--file F] # stage: attach + fill + verify (no send)
perplexity console submit                                        # submit the staged turn (verified, self-healing)
perplexity console wait [--wait N]                               # wait for the staged answer to settle
perplexity console extract                                       # turn-scoped answer (+sources); consumes the staged turn
perplexity console send "q" [--file F]                           # fill + submit only
perplexity console attach --file F | files | detach NAME         # attachment management (idempotent)
```

Recovery cookbook by error code (all commands print `error_code` in JSON):
- `pending.missing` → nothing staged: run `fill` first. `pending.stale` (>30 min) → re-`fill`. `pending.page-moved` → tab wandered: `console open <task>` then re-`fill`; page-moved now auto-reattaches once per step (but NEVER replays submit — checked at the step level). `pending.not-submitted` → `wait` needs `submit` first.
- `fill.not-committed` → editor desynced; the step already tried one reload — re-run `fill` once, then read the evidence screenshot.
- `act.target-occluded` → the pre-action geometry/occlusion re-check failed (target centre covered by an overlay/浮层, or its rect off the viewport): the click/fill was NOT fired (fail-closed, never a blind click). Dismiss the popup or scroll the target into view, then re-run the step.
- `submit.no-turn` → check the error's last-bubble hint; if a mis-sent turn exists, `console open` (reload) then re-`fill`/`submit`. The error's `gates.submit.no_progress` says per rung (`button`/`combo`) which wait tripped the breaker vs. timed out — `act.no-progress` is only raised when EVERY wait tripped. `act.no-progress` → the no-progress circuit breaker: 3 consecutive polls with a byte-identical substantive signal (URL / bubbles / prose / controls; rect jitter ignored) — the wait failed fast instead of idling out the timeout. Nothing on the page moved: check the tab (hidden tab, dead composer, extension down) before re-firing the action. Exception: the attachment-chip wait gets a 5s slow-page grace (`guard_min_elapsed`) before the streak counts, so slow uploads are not cut off at ~3 polls.
- `complete.timeout` → answer didn't settle in budget: `wait --wait <bigger>` (deep answers run minutes) or `extract` what's there.
- `bridge.probe-failed` → WebBridge gave 5 consecutive empty probes (e.g. 502 outage): retry the whole step.
- `model.tab-hidden` → the console tab is hidden/occluded and trusted clicks would be silently dropped; bring the Chrome tab to the front and retry (`Page.bringToFront` was already attempted). `model.menu-failed` → the menu portal did not open even on a visible tab — retry once, then inspect the model button readback.
- `extract.truncation-risk` → strict mode: the answer's tail has no sentence terminator
  and the action icon suggests the page is still generating (not idle / morph to stop).
  Extract succeeded but the truncated content should not be trusted — re-run with a
  larger wait budget or wait then retry `extract` without `--strict`.
- `probe.fallback-exhausted` → the primary probe AND the element-table fallback rung
  both failed (fail-closed, never a half result). See the fallback ladder below for
  the per-rung meaning and the handling recipe.

### Element-table fallback ladder (probe → element-table rung → `probe.fallback-exhausted`)

Two hard single points get a second rung (added 2026-09-28): the answer body
(`main div.prose`) and submit ownership (the `user-bubble` completion anchor). The
ladder is always `primary probe → element-table rung → probe.fallback-exhausted`,
under fixed rules (external review D1=A / D2=A / D3=B + WARN):

- **D1=A** — rung targets are picked by a PURE deterministic heuristic (no LLM).
  The heuristic only proposes **candidates**; a candidate is adopted only after a
  semantic readback (and, where the rung acts, an effect verification).
- **D2=A** — when the fallback also fails, the unified code is
  `probe.fallback-exhausted`, fail-closed — the console never returns half results.
  If the rung's own probes are dead there is nothing to fall back onto and the
  historical fail-closed code stands (`extract.empty` / `submit.no-turn`).
- **D3=B** — every fallback trigger appends a `runs.jsonl` event
  (`op=fallback`, rung name, ok/status, hit-element snapshot summary). The summary
  is `role/label/text-head`, sanitized (URL query strings stripped, suspected
  tokens masked) and ≤80 chars. `console drift` shows a `fallbacks:` section with
  the cumulative count per rung and the recent summaries.

The three rungs and their semantics:

1. **`prose-table`** (answer text, fires when `div.prose` is missing/empty):
   content-block candidates from the element table + content containers, scored
   deterministically as *text length × container semantic weight*
   (main 1.4 / article 1.3 / section 1.1 / div 1.0) with navigation chrome
   (nav/aside/footer/header/sidebar by role/aria/class/position) excluded. The
   best candidate is adopted only if a second readback still shows a non-empty
   block of ≥200 chars containing sentence punctuation. Success output carries
   `fallback_used: "prose-table"` + `fallback_summary`. No adoptable candidate →
   `probe.fallback-exhausted`. The same rung covers the prose-COUNT path
   (`_JS_INFO` `proseCount`/`lastProseLen`): when `div.prose` is gone the
   completion/scroll waits measure the largest content block instead, with the
   first prose-dead sample as the staleness baseline (a new answer must GROW
   past it — a stale block can never satisfy the gate).
2. **`ownership-table`** (submit ownership, fires only when the user-bubble
   anchor is dead — no new turn marker at all): ownership is claimed ONLY with
   **both** an independent identity binding (this turn's query text present in
   the thread/page, normalized-whitespace containment) **and** an effect signal
   (the answer area starts growing or the completion-marker count increases).
   **WARN red line (highest constraint): composer state, URL changes and count
   changes alone can NEVER prove ownership** — the composer subtree is excluded
   from the binding search because it still holds the query without a submit.
   Missing either half → `probe.fallback-exhausted`, and the send path does NOT
   reload/retry on that code (never re-send on missing identity evidence).
   Success output carries `fallback_used: "ownership-table"` + `fallback_summary`.
3. **`expand-table`** (expand control, fires when the exact-label probe fully
   missed): near-match buttons from the element table (edit distance ≤2 to
   「展开/查看更多/Expand/Show more」 or containing the 「展开/更多/Show more/Expand」
   family). Non-button roles, disabled controls and anything carrying ？/? are
   excluded — follow-up question buttons are NEVER clicked. Each candidate must
   survive a readback AND its trusted-CDP click must grow the answer block
   (effect verification); only then is it success (`fallback_used:
   "expand-table"`). Candidates exist but no click grows the answer →
   `probe.fallback-exhausted`. No expand-like candidate at all = nothing to
   expand (plain `none`, not a failure).

Every rung carries the no-progress circuit breaker semantics: same-turn repeats
with zero substantive progress trip `act.no-progress` instead of spinning.
Precedence: a frozen page (byte-identical samples ×3) → `act.no-progress`; a page
that moves but can never prove the claim → `probe.fallback-exhausted`.

Handling recipes:
- `act.no-progress` → nothing on the page is moving at all (breaker, fail-fast).
  Check the tab (hidden tab / dead composer / extension down), then re-fire ONCE.
  Never blind-retry a send on this code: verify ownership first.
- `probe.fallback-exhausted` → evidence-level failure, NOT a transient: the
  console could not PROVE its claim (no adoptable answer block / no expand
  verification / missing query binding or effect signal). Do NOT auto-retry the
  send. Read `gates.*.fallback*` (`bound`, `effect`, `candidates`, `summary`)
  and the `runs.jsonl` `op=fallback` events to see what was missing, then either
  re-run `fill`/`submit` after inspecting the tab, or extract with `--peek` to
  review the page state.

`ask --model "Grok 4.6"` calls `console_set_model` before the fill, so you switch models
and ask in one command. Available model names are listed by `perplexity console models`.

`extract --peek` returns the same staged answer again without consuming the staged turn
(no disk write, no turn increment); `--again` re-reads a consumed turn. Both disable
page reload (safe for inspection during an active stream). `--strict` fails with
`extract.truncation-risk` when the tail is mid-stream.
- Default practice: ordinary turn → `ask`; anything unusual (partial flows, single-step retries, staged attachments, inspection between steps) → compose the granular steps.

Optional Jev judge (added 2026-09-21; off by default):
- Enable per call (`--judge`) or globally (`PERPLEXITY_CONSOLE_JUDGE=1`); one extra TypeSafe request per judged step, ~$0.00001.
- `ask`/`extract --judge` record an advisory verdict on the extracted answer (`judge: ok|review|concern` from two Nouls: answers-the-question + completeness). A `concern` verdict should make the operator re-check before trusting the answer.
- Failed steps print `hint (Jev): <route> (confidence …)` — one Choice over {retry-step, reload-and-retry, wait-longer, escalate}; `pending.*` codes skip judging (deterministic guidance already in the message).
- **Bounded Jev-directed recovery (fill/wait/extract)**: the route is not just advice — `reload-and-retry` actually reloads the tab, `wait-longer` actually extends the wait, then the step re-runs ONCE under all original gates; the result carries `gates.jev_recovery` (`{route, confidence, applied, attempts}`) and a failed re-run raises with `jev_recovery` in its gates. `escalate` or any non-ok decision re-raises the original error unchanged.
- **Send paths stay advisory-only** (`submit`/`send`/`ask`): Jev never gets execution rights there, so an automatic retry can never double-send.
- Fail-open: no key / network / contract problem → `status: unavailable`, the pipeline is never blocked or changed. Responses are validated before use (probability set/arg-max/sum — adapted from browser-use/jev-ultrafast, MIT); invalid responses are discarded.

Conventions: WebBridge session `perplexity-console`, group «Perplexity 控制台», exactly one tab. Durable state lives in `~/.perplexity-console/state.json` (session, group, per-task thread URL) because session→tab mappings are daemon-memory only and die on daemon restart — the console attach-or-recreates by reopening the saved thread URL. Every step carries a readback gate; failures raise with a screenshot under `~/.perplexity-console/evidence/`.

Live-verified UI behaviors (2026-09-23; bake these into any direct-browser flow):

- The composer is a controlled React editor. `fill` (clear-and-insert) is its ONLY reliable mutation path; CDP key events, execCommand and DOM/range edits get reverted by re-render, and empty/whitespace fill values are silent no-ops.
- `fill` can also silently no-op on a fresh/unfocused editor while returning `success: true` — always read the composer back.
- The submit button is `button[aria-label="提交"]`; its `disabled` flag mirrors the editor's internal state (disabled = state empty even if the DOM shows text). Verify `enabled` before clicking; a DOM/state desync (DOM shows text, button disabled) is healed by one page reload.
- The action button **morphs icon** during generation: idle arrow-up (`#pplx-icon-arrow-up`) → stop icon during generation. The `_JS_INFO` probe captures `action_icon` (the `svg use href`). Busy detection: `action_icon != SUBMIT_ICON_IDLE`. The completion gate (v2.2, 2026-09-23) settles on **new answer seen** (proseCount > base_prose) ∧ length stable ≥2 ∧ icon idle ∧ no visible stop control — never on length alone (original bug: `stable >= 1` early-exit at 175s). The `studied` pill count is an **advisory** signal for Pro-Search turns only (answers without research get no pill). The `generating` regex constant-true noise (model badge 「正在思考」is a reasoning-mode label, not a live status) — never rely on it.
- A late async draft-restore can merge old draft text into the composer AFTER a successful fill; the submission then carries draft+query (seen live). Re-verify composer equality immediately before submitting; repair by re-filling (fill replaces).
- Per-turn scoping (never use `main.innerText` in a thread): user turns = `[class*="user-bubble"]` filtered `:not(.opacity-0)` (text = query + "\nHH:MM"); completion marker = one `已研究` pill per answered turn (count increments); the answer body = the LAST `main div.prose` (one per turn). The expand control in the new UI is a button labeled 「展开」 (the legacy 「查看更多」 did not appear in live mapping).

Model selector & attachments (added 2026-09-21):

- `perplexity console models` lists the selector menu (name/badges/checked; submenu entries like "GPT-5.6 Sol | Max" are flagged and not programmatic-selectable yet); `perplexity console model "<name>"` switches with a verified readback of the button's aria-label. The menu is a Radix portal: open and select ONLY with trusted CDP mouse clicks at element coordinates (synthetic clicks do nothing); close leftovers with Escape via CDP.
- If the trusted click never lands (the menu probe stays closed with no pointer error), the tab is **hidden/occluded** (Chrome window not front / tab in background). **Corrected 2026-09-27**: trusted CDP clicks (`Input.dispatchMouseEvent`) are *silently dropped* while the tab is hidden — that rung does NOT survive occlusion (the earlier claim here was wrong; verified both ways live). The model-menu flow now runs a visibility gate first: `document.visibilityState` probe → `cdp Page.bringToFront` through the WebBridge channel → re-probe → raise `model.tab-hidden` if still hidden (bring the Chrome tab to the front, then retry). Product paths use the WebBridge/CDP channel only; `osascript`/AppleScript window driving is a development-debug tool, never a product rung. Synthetic `.click()` never works on this Radix portal regardless of visibility.
- `ask --file PATH` (repeatable) attaches local files by building them in-page (base64 → Uint8Array → File → DataTransfer → input change event). This deliberately bypasses the WebBridge `upload` action, which requires Chrome's per-extension "Allow access to file URLs" (off by default, not toggleable by the extension; CDP `DOM.setFileInputFiles` is also blocked with "Not allowed"). Keep injection for files ≤8MB; for larger files point the user to the chrome://extensions toggle. Attachment chips verify via `aria-label="移除 <name>"`; wait ≥2s after chips appear before touching the composer.
- Send hardening: an attachment chip keeps the submit button enabled even while the TEXT state lags — observed live as a FILE-ONLY submission. The pipeline now re-fills right before submit (freshness pass), re-verifies user-turn ownership afterwards, and recovers from a misfire with one reload + file re-inject + bounded retry (guarded by a delayed-ownership recheck so a slow-but-correct turn is never sent twice). The completion gate requires a new answer to appear (proseCount > base_prose) AND the action icon idle (arrow-up, not morphed to stop) AND length stable ≥2 — never settles on length alone (the original bug: stable ≥ 1 early-exited at 175s).

## Key DOM Patterns

| Element | Selector Strategy | Notes |
|---------|-------------------|-------|
| Input box | `document.querySelector("[contenteditable]")` | Always one contenteditable div |
| Search button | `button` with text "搜索" | Sometimes unreliable; prefer Enter key |
| Model selector | `button` with model name text | Dropdown requires CDP click |
| Answer tab | `[role=tab]` with text "答案" | Default active |
| Links tab | `[role=tab]` with text "链接" | Shows sources |
| Images tab | `[role=tab]` with text "图片" | Image results |
| Expand answer | `button` with text "展开" (new UI) or 「查看更多」 (legacy) | Collapsed by default! `_JS_EXPAND` matches both labels EXACTLY first; only when no exact match exists does it fall back to `includes`, and then only for buttons whose text is essentially just the label (≤2 chars of icon/punctuation noise) — a follow-up question like 「怎么查看更多细节？」 is never clicked |
| Source count | `button` with text "N 个来源" | Inline badge |
| Follow-up Qs | `button` with question text | Below answer — never treated as the expand control |

## Python Helper Script

See `scripts/perplexity_search.py` for a reusable function that:
1. Takes a query string
2. Runs a `list_tabs` connection precheck before navigating
3. Searches Perplexity
4. Waits for results
5. Expands the answer
6. Returns `{answer, sources, url, follow_ups}`

The `list_tabs` precheck runs before every navigation: `{success:true, tabs:[]}` is healthy and the run continues; a `no extension connected` response or any non-success result aborts with a connection error instead of blindly navigating.

The CDP `Input.insertText` fallback (used when `fill` fails) applies to the **initial** search only. The follow-up path must not use CDP insertText — keep follow-ups on the click/fill path, consistent with the conversational skill.

## Known Limitations

1. **Answer truncation**: long answers arrive collapsed behind a fade mask; click the 「展开」 control (new UI; legacy label "查看更多") — and scope extraction to the LAST `div.prose` so earlier thread turns never leak into the answer
2. **Element refs change**: Every session gets different @e refs; use role+name or JS selectors
3. **Model dropdown**: React synthetic events; may need CDP for model switching
4. **Rate limits**: Perplexity Pro has usage limits; batch carefully
5. **No Deep Research automation yet**: Need to map the Deep Research UI flow
6. **Focus modes not mapped**: Academic, Writing, Math modes need exploration
7. **File upload not mapped**: Need to explore the upload flow
8. **Fill is the only reliable editor mutation path** — keyboard/CDP/DOM edits are reverted by the controlled re-render, empty fills are no-ops, and a fill can silently no-op while reporting success. Read the composer back and require equality.
9. **Draft-restore merge**: a late async draft restore can merge leftover draft text into a successfully-filled composer; the submitted message then contains draft+query. Re-verify the composer immediately before submit and re-fill on mismatch.
10. **DOM/state desync**: the editor's visible text can disagree with its internal state (submit button disabled while the DOM shows text). Use the submit button's `disabled` flag as the state signal, and heal with a single page reload.
11. **Thread extraction scoping**: in a multi-turn thread `main.innerText` contains the whole conversation; extract only the last `div.prose` and identify turns via `user-bubble` + `已研究` counts.

## Session Management

- Session/group policy lives in `webbridge-hygiene` (session classes + duplicate ladder); this section adds only Perplexity-specific practice. Serial Perplexity operations — follow-ups and source pages included — run in the `perplexity-console` purpose session; mint a task session only for parallel lanes or atomic close.
- Reuse the current tab for a related follow-up; use `newTab:true` only when pages genuinely need to coexist (or to attach-or-recreate a lost keeper).
- Do not close the session automatically. Per `kimi-webbridge`, `close_session` is user-initiated only (for example, the user explicitly asks to close or clear the tabs); never `close_session` the purpose console as cleanup — use `close_tab`.
- If the extension says it is already linked, inspect `list_tabs` and continue with the existing daemon/session instead of creating a new thread/session.
- Tabs accumulate in the session's group only when deliberately opened with `newTab:true`; keep the group within the hygiene purpose quota (target 1–3, ceiling 5) and readable.

## Local review notes

Machine-local audit trail (referenced by name, not part of this repo): the Obsidian project **Perplexity Robustness Review** (`Projects/perplexity-robustness-review/`) holds the DOM fragility audit of this skill's probes, the hardening decision log, the jev-ultrafast structural comparison, and the A/B iteration protocol. Consult it before changing selectors/probes; record probe-drift findings there.
