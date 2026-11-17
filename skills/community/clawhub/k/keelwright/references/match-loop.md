# Match Loop (visual QA) — Generator ↔ Analyst

For vibe-coding where one-shot generation isn't enough (frontend, visual features). Activates at
Triage level Critical, or when Stability catches Feedback Starvation (green gates but broken UI).

## Pattern: Generator ↔ Analyst loop

1. **Define target** — what "perfect" means, must-have features, visual/style expectations
2. **Spawn Generator** (`delegate_task`) — codes the artifact
3. **Spawn Analyst** (`delegate_task` with a browser toolset) — reviews code + visually inspects the UI
4. Analyst produces a **feedback packet**: what works, what's broken, screenshots, prioritized changes
5. Generator revises → repeat until convergence

### Verdict taxonomy (mandatory, matches run contract)

Use exactly one verdict per test:
- `PASS` — element/layout/accessibility requirement met
- `NO-DIFF` — no measurable deviation detected or baseline was underspecified
- `PARTIAL` — some requirements met, others not
- `INCONCLUSIVE` — render/check failed or evidence insufficient
- `CANNOT` — this visual QA cannot be evaluated here

Free-form verdicts like `PENDING`, `BLOCK COMMIT`, or `DONE` are forbidden in visual QA outputs.

## Analyst responsibilities (non-negotiable for frontend)

The analyst MUST visually inspect the frontend. Code review alone is insufficient.

### Browser prerequisite — no browser tooling, no visual verdict

Visual QA needs a real browser to render and measure. Before the analyst starts, confirm a
browser automation surface is available; if the host has none, do NOT fake a visual verdict.

- **If your runtime already exposes browser tools** (navigate / screenshot / snapshot / console),
  use them — the recipes below assume that.
- **If the machine has no browser tooling and you want visual QA**, you can install a free one.
  The stack-agnostic, permissively licensed option is `agent-browser` (Vercel, **Apache-2.0**) —
  a native CLI that drives Chrome for AI agents:
  ```bash
  npm i -g agent-browser
  agent-browser install       # downloads Chrome for Testing (first run only)
  # then, e.g.:
  agent-browser open <url>
  agent-browser snapshot      # accessibility tree with @refs (best for AI)
  agent-browser screenshot --screenshot-dir ./shots
  ```
  > ⚠️ **Consent & supply-chain note:** `npm i -g agent-browser` is a **global** install
  > that modifies your system and downloads a browser binary from the network.
  > Review it before running; prefer a local/`npx` install in an isolated environment
  > if your platform policy forbids global changes. Only do this if you explicitly want
  > visual QA enabled. Not required — use only if convenient.
  > Repo: `https://github.com/vercel-labs/agent-browser` (also ships a `.claude-plugin`,
  > so it can be added as a skill/plugin where that's supported). Verify install with
  > `agent-browser --version` before relying on it.
- **If neither is possible** (no browser tools, install blocked by no network/permissions):
  the visual test is **CANNOT-RUN** with that reason recorded — same tool-absence honesty as the
  structural gate. A gate that cannot run has NOT passed; never emit a green/PASS visual verdict
  from an environment that could not actually render the page.

**Order of browser tools:**
1. navigate — open the app
2. screenshot / vision — capture
3. click / type — interactions
4. console — runtime errors
5. snapshot — DOM structure

**Analyst deliverable must include:**
- Verdict from the fixed verdict taxonomy
- "expected vs seen" list for each requirement
- At least one absolute screenshot path on disk, verified with tool output, not self-reported

**Check for (qualitative):**
- Text cut off, overlapping, misaligned
- Mobile/desktop layout problems
- Broken spacing, hierarchy, visual balance
- Forms that look fine in code but fail in the UI
- Loading/error states that look broken
- Silent API failures (check the console)
- Buttons that do nothing

**Required numeric measurements (MANDATORY — report the actual number, not "looks fine").**
A purely qualitative "reads OK / contrast looks low" verdict is NOT discriminating — the eye can't
reliably judge a threshold, so it collapses to NO-DIFF. Compute and report each value; a check
without its number is INCONCLUSIVE, not PASS:
- **No horizontal overflow:** `document.documentElement.scrollWidth <= window.innerWidth` (report both).
- **Text contrast:** compute the WCAG contrast ratio for body text and any status/error text; must be
  ≥ 4.5:1 (≥ 3:1 for text ≥ 24px/large). Report the actual ratio and the two hex colors.
- **Text size:** report the smallest rendered font-size; flag anything < 12px.
- **Tap targets:** report the smallest interactive element box; flag anything < 24×24px.
Get colors/sizes from the rendered DOM (computed styles via the browser), not from source guesses.

## Convergence rule

The analyst accepts ONLY after:
- Code review passes for the task scope
- Frontend visually inspected (if applicable)
- Key interactions tested
- Major visual/functional defects resolved

Stop when: analyst accepts, trashing (revisions don't improve), blocked, or the user says stop.

## Pitfalls — verifying NON-OBVIOUS structural attributes

`browser_snapshot` (the accessibility tree) is the right source of truth for **roles, names,
grouping, and the verdict taxonomy** (in-session it reported `group "Choose a plan"`, `alert`,
button name, etc.). But it does NOT expose attribute-level detail. For structural requirements
like:

- programmatic focus **order** (`tabindex` values) — the snapshot shows nothing about tab order;
- `aria-describedby` **bindings** (which hint/error element a field points at);
- `role` / `aria-live` / `aria-describedby` attribute presence on a node;

you MUST read the live DOM, not the snapshot. Use `browser_console` with `getAttribute` /
`tabIndex`.

**Critical console quirk (verified in-session):** the expression evaluator serializes the
return value, and **object/JSON returns come back as `null`** (and an IIFE wrapper sometimes
throws `SyntaxError: Unexpected end of input`). `JSON.stringify(...)` alone also returned
`null`. The reliable pattern is to build and return a **plain string primitive**:

```js
'focus=' + Array.from(document.querySelectorAll('input,button'))
    .filter(el => el.tabIndex >= 0)
    .map(el => el.id + ':' + el.tabIndex).sort().join(',')
  + ' | emailRole=' + document.getElementById('email-error').getAttribute('role')
  + ' | emailLive=' + document.getElementById('email-error').getAttribute('aria-live')
  + ' | legend=' + document.querySelector('fieldset legend').textContent
  + ' | phoneDesc=' + document.getElementById('phone').getAttribute('aria-describedby')
  + ' | btn=' + document.querySelector('button[type=submit]').textContent.trim()
```

Then parse the returned string. This is the only form that reliably returned data in-session.

**Sequence that worked for a structural-a11y check:** `browser_navigate` → `browser_snapshot`
(roles/names/groups from the tree) → `browser_console` (attribute-level detail as a string)
→ assert each non-obvious requirement against the returned string + the snapshot.

## Ad-hoc verification script recipe (proven in-session)

When a quick regression check is useful and no canonical test runner exists:
1. Write a small Python script to `C:\\Users\\<user>\\AppData\\Local\\Temp\\hermes-verify-<topic>.py`.
2. Load the target file and run regex/structural assertions against it.
3. Print `ALL_PASS: True/False` and `sys.exit(...)`.
4. Run it via terminal, then clean it up with `rm`.

**Pitfall — HTML attribute regex:** if a requirement involves attributes like `tabindex`, `aria-describedby`, or `role`, regex must allow quoted and unquoted attribute values. Use `(["']?\d+["']?)` instead of `(\d+)`, and strip quotes before comparing. A too-strict pattern silently fails and blocks convergence.

**Browser console expression fallback:** for live DOM checks, return a plain concatenated string, not an object. JSON/object returns serialize as `null` in this environment. Build the data as string segments and parse the result.

## Convergence rule update
The analyst accepts ONLY after:
- Code review passes for the task scope
- Frontend visually inspected (if applicable)
- Key interactions tested
- Major visual/functional defects resolved
- Ad-hoc verification script cleaned up from Temp when used