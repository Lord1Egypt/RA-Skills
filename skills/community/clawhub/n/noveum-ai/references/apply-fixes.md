# Apply fixes to the codebase (step 7)

Input: a fix with a `diff` (`search`/`replace`/`rule`, plus `basePrompt`/`fixedPrompt`)
from AutoFix, an experiment result, or a NovaPilot recommendation. Output: a minimal,
reviewable PR in the customer's repo — applied by YOU, in THEIR environment. Nothing is
sent to Noveum in this step except, later, the ordinary telemetry that verifies the fix.

## 1. Locate where the prompt lives (three strategies, in order)

1. **Provenance** (when present): newer noveum-trace versions stamp `code.file.path` /
   `code.line.number` / `code.function` and `git.commit.sha` on spans; if the fix carries a
   `sourceRef`, open exactly that location.
2. **Anchor search:** grep the repo for distinctive substrings of `search` (or of
   `basePrompt`). Prompts are often templated/assembled — if the exact string isn't found,
   search for its longest stable fragments and find the template that produces it.
3. **Inference:** locate prompt-construction code (files named like `prompts`, `system`,
   constants passed to `messages=[{"role": "system", ...}]`) and match semantically.

If you cannot confidently locate the prompt, STOP and ask the user — never guess-edit.

## 2. Apply the edit

- `kind: "search-replace"`: replace the `search` text with `replace` at its source
  (template or literal). If the prompt is assembled from fragments, apply the change to
  the fragment that contains the anchor, preserving the template structure.
- `kind: "append-rule"` / `rule`: append the rule text to the system prompt's source in
  the repo's existing style (same formatting, same language as surrounding rules).
- Sanity check: reconstruct the final prompt mentally (or via the repo's tests) and
  compare against `fixedPrompt` — the deployed prompt should match what was backtested.
  Meaningful divergence = flag to the user, don't ship silently.

Also bump the app's `NOVEUM_SERVICE_VERSION` (or however the repo sets `service_version`)
so post-fix traffic is distinguishable — this is what makes verification possible.

## 3. Open the PR (never push to the default branch)

Branch + PR with a body containing:
- What was changed and why (the finding, in one paragraph)
- **Evidence**: validation status (validated win w/ CI + objectiveGain / directional /
  unvalidated recommendation), affected checks/scorers, evidence trace/item ids
- Link to the NovaPilot report / AutoFix run in the Noveum dashboard
- The verification plan (below)

Label unvalidated fixes clearly. One concern per PR — don't bundle unrelated fixes.

## 4. Verify after deploy

Once merged and deployed:
1. Confirm post-fix traffic arrives under the new `service_version`
   (`GET /v1/traces?service_version=<new>&size=5`).
2. If AutoFix is enabled, run the post-apply verify (`experiments-autofix.md` §compare)
   and report the verdict; otherwise re-run the eval job on fresh traffic and compare the
   affected scorers before/after.
3. Report the outcome to the user either way — including "no measurable change" or
   regressions. The loop is only closed by measurement, not by merging.
