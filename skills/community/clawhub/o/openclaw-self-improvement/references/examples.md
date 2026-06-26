# Practical Examples for Self-Improvement Eval Loops

Use these examples when you want to turn a repeated operational mistake into a tested guardrail.

---

## Example 1 — Mission Control summary link-complete gate

### Repeated failure
Mission Control agent summaries were updated at the JSON layer but still too thin for operator use. They lacked concrete links, detail blocks, and next handoff context. In some cases the front-end also failed to render the newly added structured fields.

### Target
Make Mission Control summaries decision-ready instead of status-only.

### Baseline
Before the change:
- summary text could say "DELIVERED" without concrete artifact links
- evidence existed in underlying files but not in summary fields
- operator-facing UI could still show "No source links in current summary"

### Single mutation example
Add a summary contract requiring:
- at least one artifact path or URL
- evidence links when external proof matters
- a detail block
- next handoff / recovery action

### Binary evals
- [ ] Does the summary include at least one artifact path or URL?
- [ ] Does the summary include evidence links when external proof matters?
- [ ] Does the summary include a detail block explaining what changed?
- [ ] Does the summary include the next handoff or recovery action?
- [ ] Does the operator-facing surface actually render these fields?

### Result classification guidance
- **KEEP** if the summary and rendered surface both become decision-ready.
- **DISCARD** if the JSON changed but the operator-facing surface still hides the proof.
- **PARTIAL_KEEP** if the summary structure improved but the rendering layer still needs a separate fix.

### Example command
```bash
node scripts/log-experiment.mjs \
  "Mission Control summaries should be link-complete and decision-ready" \
  "DELIVERED summaries lacked links/details and the UI still showed no source links" \
  "Added artifactLinks/evidenceLinks/details/nextHandoff contract to summary schema" \
  "summary has artifact path|summary has evidence links|summary has detail block|summary has next handoff|UI renders structured fields" \
  "Summary JSON improved, but front-end rendering still needed a separate mapping fix" \
  "partial_keep"
```

---

## Example 2 — ClawLite deploy closeout gate

### Repeated failure
Code changes were being treated as effectively live before production verification. Sitemap and page changes could be committed and locally built, while production remained stale or blocked.

### Target
Ensure web changes are never called live without production verification.

### Baseline
Before the change:
- code-ready and build-ready states were often described as if they were live
- no explicit deploy owner existed
- production sitemap verification was not consistently required

### Single mutation example
Add a deploy closeout SOP with Peter as owner and require deploy-state vocabulary plus production verification.

### Binary evals
- [ ] Is the deployed commit hash recorded?
- [ ] Is a deployment ref or URL recorded?
- [ ] Was the production page or sitemap actually verified?
- [ ] Was a structured deployment receipt written?
- [ ] Is the final state classified as CODE_READY_NOT_DEPLOYED / DEPLOY_PENDING / DEPLOYED_NOT_VERIFIED / LIVE_VERIFIED / BLOCKED_DEPLOY instead of vague done/not-done wording?

### Result classification guidance
- **KEEP** if the team stops calling code-ready changes "live" without production proof.
- **DISCARD** if the new SOP adds wording but nobody records deploy refs or production verification.
- **PARTIAL_KEEP** if the receipt/state vocabulary lands but enforcement is still inconsistent.

### Example command
```bash
node scripts/log-experiment.mjs \
  "ClawLite web changes should require production deploy closeout before being called live" \
  "Code/build truth was repeatedly confused with production truth" \
  "Added Peter-owned deploy SOP and deploy-state vocabulary" \
  "commit hash recorded|deployment ref recorded|production sitemap verified|deployment receipt written|state uses deploy vocabulary" \
  "Deploy blocker was surfaced truthfully as BLOCKED_DEPLOY instead of being misreported as live" \
  "keep"
```

---

## Rule of thumb

If the change improves only the hidden back-end layer but leaves the operator-facing truth surface stale, the experiment is not a full keep yet.
