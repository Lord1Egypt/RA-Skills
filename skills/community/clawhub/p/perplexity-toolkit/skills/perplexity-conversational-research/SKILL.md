---
name: perplexity-conversational-research
description: "Use when the user wants deep or multi-turn Perplexity research, follow-up questions on the same thread, or several model perspectives on one topic (say \"用 perplexity 研究\" / \"perplexity 搜一下\"). The single research-policy entry point: picks between the perplexity CLI and the browser route, keeps one session and conversation URL across turns. Quick one-shot lookups go to perplexity-search; raw browser actions go to perplexity-web-automation."
metadata:
  version: "1.1.0"
  requires: ["kimi-webbridge", "webbridge-hygiene"]
  optional: ["perplexity-toolkit"]
---

# Perplexity Conversational Research

Multi-turn Perplexity research uses one of two explicit routes. The route is
selected from the user's wording before any CLI or browser probe:

- Explicit web/browser/Chrome/WebBridge wording → direct
  `perplexity-web-automation` with `kimi-webbridge` and its hygiene pair.
- Otherwise → `perplexity` CLI first. The current CLI is backed by the
  toolkit's WebBridge driver, but it is still the CLI-managed route.

If the CLI is unavailable or fails, stop and report that fact. Do not silently
switch to the user's logged-in browser; ask for explicit authorization before
using the direct WebBridge route or the standalone fallback helper.

## Skill stack and runtime selection

This is the high-level route/workflow entry point for a deep or multi-turn task.
Use `perplexity-web-automation` only for the explicit direct-browser route or
for a browser follow-up that the user has authorized. Do not load
`perplexity-search` as a second full research workflow; it is the shared
quick-lookup and verification policy layer.

The current CLI/toolkit is not an API or headless backend. It ultimately uses
Kimi WebBridge and Chrome; the distinction here is the user-facing controller
and policy route, not the underlying transport.

## When to Use

- User wants deep research from Perplexity with follow-up questions
- User wants different model perspectives on same topic
- User says "用 perplexity 研究" or "perplexity 搜一下"

## Workflow

### Step 1: Select the route before probing

Apply this gate before checking whether the CLI is installed:

```text
if the user explicitly requests a web page/网页方式/browser/Chrome/WebBridge/current browser thread:
    use perplexity-web-automation directly
    do not invoke perplexity CLI first
else:
    use perplexity CLI first
    if CLI is unavailable or fails:
        stop and report the failure
        request authorization before using direct WebBridge
```

When the toolkit is installed, the same deterministic gate is available as
`perplexity route -f json "<the original user wording>"`. It is a local
classifier only; run it on the user's route request, not on a research topic
that merely mentions the web.

Never claim a CLI result that was not actually returned. "Not resolved in this
environment" and "not installed" remain distinct reports, but neither permits
an automatic browser fallback. The standalone
`perplexity-web-automation/scripts/perplexity_search.py` helper is also an
explicitly authorized fallback/diagnostic, not an implicit third route.

```bash
# Availability check (do not print credentials).
# A bare `python3` is NOT a valid probe: the toolkit is installed into one
# specific environment, which is often not the interpreter that resolves on
# PATH. Resolve the console script instead, and only fall back to importing
# the package with the interpreter that ships alongside it.
PERPLEXITY_BIN="${PERPLEXITY_BIN:-}"
for cand in \
  "$PERPLEXITY_BIN" \
  "$(command -v perplexity 2>/dev/null)" \
  "${VIRTUAL_ENV:+$VIRTUAL_ENV/bin/perplexity}"
do
  [ -n "$cand" ] && [ -x "$cand" ] && PERPLEXITY_BIN="$cand" && break
done

if [ -n "$PERPLEXITY_BIN" ] && "$PERPLEXITY_BIN" --help >/dev/null 2>&1; then
  echo "toolkit: available at $PERPLEXITY_BIN"
else
  echo "toolkit: not resolved — report the CLI failure; do not switch routes"
fi

# If unresolved but you believe it is installed, ask the user for the path and
# record it as PERPLEXITY_BIN. Do not guess absolute paths, and do not report
# "not installed" — report "not resolved in this environment".

# If available (use "$PERPLEXITY_BIN", not a bare `perplexity`):
"$PERPLEXITY_BIN" --session-prefix TASK_SESSION search "query" -m search -f json
"$PERPLEXITY_BIN" --session-prefix TASK_SESSION search "query" -m model_council -f json
"$PERPLEXITY_BIN" --session-prefix TASK_SESSION search "query" -m step_by_step -f json
"$PERPLEXITY_BIN" --session-prefix TASK_SESSION search "query" -m deep_research -f json
```

The CLI handles navigation, textbox focus, query fill, submit, wait, expand,
extract, sources, and quality checks. Its default session namespace is isolated
per CLI process; pass a stable task prefix when several commands must continue
one task. A non-zero CLI exit or a result containing `error` is a route failure,
not permission to launch a browser fallback.

### Step 2: Authorized direct-browser follow-up

The following WebBridge sequence is allowed only after the user explicitly
authorizes the direct-browser route (or explicitly asks to continue the current
browser thread). A CLI result URL alone is not authorization. If the user did
not request browser execution and the CLI has no follow-up subcommand, report
that limitation instead of silently issuing these browser commands.

```bash
# 1. Navigate to the search result URL (same tab)
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"<URL_FROM_CLI>","newTab":false},"session":"TASK_SESSION"}'

# 2. Wait for page load
sleep 4

# 3. Focus the textbox
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const el = document.querySelector(\"[contenteditable]\"); if(el) { el.focus(); return \"focused\"; } return \"not found\"; })()"},"session":"TASK_SESSION"}'

# 4. Fill with WebBridge fill action (NOT CDP insertText, NOT textContent)
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"fill","args":{"selector":"[contenteditable]","value":"FOLLOW-UP QUERY"},"session":"TASK_SESSION"}'

# 5. Submit with three-event Enter combo via evaluate
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const el = document.querySelector(\"[contenteditable]\"); if(!el) return \"no input\"; el.dispatchEvent(new InputEvent(\"beforeinput\",{inputType:\"insertText\",data:\"\\n\",bubbles:true,cancelable:true})); el.dispatchEvent(new KeyboardEvent(\"keydown\",{key:\"Enter\",code:\"Enter\",keyCode:13,which:13,bubbles:true,cancelable:true})); el.dispatchEvent(new KeyboardEvent(\"keyup\",{key:\"Enter\",code:\"Enter\",keyCode:13,which:13,bubbles:true,cancelable:true})); return \"enter dispatched\"; })()"},"session":"TASK_SESSION"}'

# 6. Wait and extract (same as initial search)
sleep 15-20
```

### Resident console (lock one group for Perplexity)

The default way to satisfy "lock one group for Perplexity" is the toolkit's resident console — one WebBridge session `perplexity-console` = one group «Perplexity 控制台» = one tab; one task = one thread:

```bash
perplexity console ask "query" --task <task> [--new-thread] [-f json]
perplexity console status | threads | selfcheck
```

**Trigger phrases → console**: when the user says 「用网页(版)的 Perplexity 搜/问…」「拿浏览器里的 Perplexity 搜…」「用（perplexity）控制台问…」, run `perplexity console ask` directly — pick one stable `--task` name from the topic (reuse the existing task name to continue an earlier thread). Do not hand-drive the raw browser steps and do not route these through `perplexity search`; the console is the executor for this route.

Continuation semantics: same task → follow-up in the same thread; a new task or `--new-thread` → a fresh thread in the same tab (home → submit). State (per-task thread URLs) persists in `~/.perplexity-console/state.json`, so daemon/browser restarts do not break continuity. Every step is gated (fill equality → user-turn ownership → completion signals → turn-scoped extraction) with loud, evidence-bearing failures. When the console is unavailable, fall back to the manual recipe below.

### Fixed group + one-tab variant

When the user explicitly asks for one fixed group/tab, do not use an explicit
new-tab path for every round. The standard CLI wrappers preflight `list_tabs`,
open one tab only for an empty task session, and reuse it thereafter. Each mode
still carries its own group label; preserve the same task prefix when switching
between commands.

1. Choose one task-named WebBridge session and keep it for the whole lane. Start with `list_tabs`. If the session is empty, create exactly one tab with `newTab:true` and the user-language `group_title`; then use `newTab:false` for all reuse. Serialize every command in that session.
2. Keep the work toolkit-first by injecting the current tab into the toolkit package instead of starting a raw browser search. The package API accepts an explicit `WebBridgeDriver` and `new_tab=False`:

```python
from perplexity_toolkit.config import get_config
from perplexity_toolkit.search import search, model_council
from perplexity_toolkit.drivers.webbridge import WebBridgeDriver

cfg = get_config()
driver = WebBridgeDriver(cfg.webbridge_url, session="<fixed-session>")
result = search(query, config=cfg, driver=driver, new_tab=False)
# or: result = model_council(query, config=cfg, driver=driver, new_tab=False)
```

3. Preserve the original conversation URL before running a model mode. A same-thread WebBridge follow-up stays in that chat; a mode call usually navigates to the home page and starts a separate Perplexity conversation even when `new_tab=False`. Therefore:
   - if the user requires **one exact chat**, use follow-ups only and do not claim that the model changed;
   - if the user requires **model diversity**, run `model_council`/`step_by_step` in the same tab, then navigate back to the saved original URL and verify the tab count/group title. Report honestly that the tab is shared but the mode result may be a separate conversation.
4. Before closeout, call `list_tabs` and verify exactly one task tab, the expected group title, and the intended final URL. Never close the session unless the user asks.

### Source reachability and version-conflict handling

The HEAD-vs-readback rule and the `toolkit-head` / `page-content` two-state recording are defined once in Step 3 (Verification) of the `perplexity-search` skill. Apply that definition; do not keep a second copy here.

If Perplexity produces contradictory versions of a page or feature, keep the contradiction visible until the canonical URL is re-read directly. Prefer the current canonical page's explicit text over an answer summary, and record the access date/version requirement. Do not let a transient or incomplete extraction become a recommendation. A source count, answer score, or model-council agreement is not independent factual verification.

The reusable fixed-tab recipe and the observed source-conflict pattern are in `references/fixed-group-tab-and-source-conflicts.md`.

### Step 3: Named-model gate and mode variety

The four toolkit modes are workflow modes, not named-model selectors. A mode
label or `model_council` result is not evidence that K3 (or any other named
model) answered. If the user requests a specific model, use the explicitly
authorized direct-browser route, select the model in the UI, read the visible
model label back, and record `selected_model` plus `model_label_verified: true`.
If the label cannot be read back, stop with an unverified result; never infer it
from the mode name or answer style.

When user wants different model perspectives, use CLI modes instead of UI model switching:

| Mode | What it does | CLI flag |
|------|-------------|----------|
| `search` | Default single model (usually Grok) | `-m search` |
| `model_council` | Multiple models answer same question | `-m model_council` |
| `step_by_step` | Guided structured answers | `-m step_by_step` |
| `deep_research` | Multi-step, longer, 60-120s | `-m deep_research` |

Run 2-4 searches with different modes on related queries to get diverse perspectives. Summarize and cross-reference results.

## Anti-Hallucination Prompt Pattern

Never ask a bare question. The canonical query wrapper is defined in Step 2 of the `perplexity-search` skill; deep research applies the same wrapper per that definition — do not keep a second copy of the template here.

For Chinese queries, append: `要求：引用来源URL，没有可靠来源要注明。`

## Community-endorsement follow-up

When the user asks whether there is a particularly influential person or a community-endorsed solution, run a bounded community delta instead of repeating the first official-doc answer. Separate **person**, **project**, and **mechanism** before ranking them.

Use an evidence ladder:

- **Strong:** first-party mechanism, or an inspectable active project with substantial adoption signals and an identifiable artifact.
- **Medium:** concrete public artifact plus repeated discussion/forks/limited adoption signals, but no independent behavior evaluation.
- **Anecdotal:** one post, one template, or self-reported improvement; useful as a hypothesis, not a consensus claim.

Always state that stars, forks, installs, and reposts measure reach/adoption, not output quality. Inspect the original GitHub README/file, official documentation, and representative community threads. Require direct URLs, access dates for volatile metrics, and limitations. If no cross-platform canonical person or template emerges, say so explicitly; that is a valid finding.

For plain-language AI-agent research, the reusable evidence bank and recommendation pattern are in `references/community-consensus-plain-language-ai-agents.md`. The current pattern is: Output Style for persistent voice, a short CLAUDE.md/AGENTS.md for project facts, Skills for on-demand rewriting, structured `Result / Changed / Verified / Remaining` delivery, and Hooks/tests only for deterministic checks. Treat Caveman-like projects as compression/anti-narration evidence, not automatic proof of natural or readable prose. Do not recommend a giant prompt pack merely because it is popular.

A Perplexity answer score or source count is not source verification. If source reachability is poor or the answer cites snippets/third-party summaries, read the canonical pages before carrying claims into the final response.

### ⚠️ CLI result has no sources

A CLI result URL, an answer string, or a high answer score is not evidence by
itself. If `sources` is empty, the quality verdict is `questionable`, or the
answer contains year/benchmark claims without citation markers, keep it as a
lead only. Do not open the returned conversation URL in the user's browser
automatically; use an already authorized direct-browser route or ask for
authorization first, then fetch canonical source pages before using claims.
If the canonical page does not support the claim, mark it unverified rather
than preserving the Perplexity wording.

### ⚠️ Dynamic page refs and long follow-ups

WebBridge `@e` refs are snapshot-scoped and can change after navigation, generation, expansion, or a follow-up. Take a fresh snapshot immediately before each fill/click and do not reuse refs from an earlier snapshot. For long non-ASCII payloads, send the request as a uniquely named JSON file body when inline JSON is rejected or corrupted; after `fill`, read the current textbox state and confirm non-empty text before submitting. Scope any keyboard/evaluate submission to the current follow-up textbox, or use the current submit control, so a hidden/older contenteditable does not receive the Enter event. After submission, re-snapshot and confirm that a new user turn and completed answer actually exist.

## Pitfalls

### ❌ Follow-up submission fails silently

**Symptom**: Text appears in textbox but Enter doesn't submit.

**Root causes (tried and failed)**:
- `textContent` assignment + `Event("input")` — doesn't trigger React state
- CDP `Input.insertText` + CDP Enter — sometimes doesn't trigger submit
- CDP mouse click on search button — React portal ignores it
- `evaluate` `button.click()` on submit button — synthetic event, not trusted

**Working method**: Use WebBridge `fill` action (handles contenteditable React state) + `evaluate` three-event Enter combo (beforeinput + keydown + keyup). See Step 2 above.

### ❌ Model dropdown doesn't open

**Symptom**: Clicking the model name button (e.g. "Grok 4.6") does nothing.

**Root cause**: Perplexity's model selector is a React portal that renders outside the main DOM tree. Synthetic clicks, CDP clicks, and evaluate clicks all fail.

**Workaround**: Use CLI modes (`model_council`, `step_by_step`, `deep_research`) to get different model perspectives. Don't fight the UI dropdown.

### ❌ Answer collapsed by default

Perplexity collapses long answers. Always click "查看更多" after search. The CLI toolkit handles this automatically.

### ❌ CDP Enter submits a newline instead of the query

If the contenteditable has no text when Enter fires, it creates a newline. Always `fill` first, then submit.

## Research Session Template

For multi-turn research (3-5 searches):

1. **Round 1**: `perplexity search "broad query" -m search -f json` — get overview + sources
2. **Round 2**: `perplexity search "specific follow-up" -m model_council -f json` — multi-model perspective
3. **Round 3**: `perplexity search "edge case or counter-example" -m step_by_step -f json` — structured detail
4. **Round 4** (optional): WebBridge follow-up in same chat for synthesis question
5. **Compile**: Cross-reference answers, note source quality, present organized summary

## Quality Verification

The CLI toolkit runs automatic quality checks:
- Answer quality score (0-100)
- Source URL reachability (HTTP HEAD) — transport diagnostic only; canonical page readback is the source-judgment basis (see `Source reachability and version-conflict handling` in the Workflow section)
- Verdict: good / questionable / poor

For `poor` verdict: re-search with different mode or break into sub-queries.

## Session Management

- Use one task-specific WebBridge session name for all browser operations; do not hardcode `perplexity-research` across unrelated tasks.
- A Perplexity thread is the website conversation; a WebBridge session is the local tab-group namespace; a Chrome extension connection is the daemon handshake. Treat them as separate state.
- Keep the session open by default; call `close_session` only when the user explicitly asks to close or clear the pages.
- CLI searches may be stateless, but preserve the returned result URL when a same-thread follow-up is required.
