# Constraints and Design Rationale

## Hard constraints

- **Whole-file size cap (hard).** USER.md is a context file; the harness truncates
  it (head + tail, middle dropped) above `context_file_max_chars`, which can lose or
  corrupt the block. The whole file must stay under the effective cap. This wins
  over every other length rule.
- **Under 300 words (soft target).** USER.md loads into every session; this block is
  pure overhead on every interaction. Over budget → compress (cut bullets first, then
  mood dimensions, then week theme). The hard cap above always takes precedence.
- **Access: use only what is already reachable.** Never request, prompt for, or
  expand access/scopes/permissions to run this skill. Reachable = in scope;
  unreachable = absent. No opt-in, no access-seeking.
- **No fabrication.** Empty calendar day → `No scheduled events`. No mood signal
  → `quiet (low signal)`. No location signal → `unknown`. A fabricated snapshot
  is worse than a thin one because the agent acts on it.
- **Mood is inferred from interaction, never from the calendar.** See
  `mood-inference.md`. This is the single most-violated rule in this skill's
  history.
- **No weather.** `ocas-vesper` owns weather. Duplicating it adds noise.
- **No advice.** This reports state; it does not prescribe. Advice belongs in
  `ocas-mentor` / `ocas-vesper`.
- **No em dashes.** Many chat renderers mangle them. Use commas and periods.
- **No markdown tables in the output block.** Chat renderers often do not render them.
  (Tables are fine inside these reference files; they are not delivered.)
- **No meta-narration.** No "here's what I found." Just the snapshot.
- **Touch only the `## Daily Context` block.** USER.md holds identity,
  preferences, and other sections owned by other skills. Overwriting them is data
  loss. Patch from the `## Daily Context` heading to the next `##` or EOF, nothing
  else.

## Why the cron and the skill must be kept in sync

In the common Hermes setup the runtime is a cron job whose prompt is **inlined**
in `cron/jobs.json`, not loaded from this SKILL.md. The cron does not read the
skill at generation time. Therefore:

- This skill is the **design** source of truth (rationale, full workflow, the
  mood engine, gotchas).
- The cron prompt is the **runtime** source of truth (what actually executes on
  schedule).
- A change in one that is not mirrored in the other is a silent divergence — and
  divergence is exactly how this skill drifted before (the cron carried an old
  format while the skill described a newer one). When you edit the workflow or
  output format here, mirror the essential instructions into the cron prompt in
  the same change, and vice versa.

This is a known structural fact of how Hermes crons run, not a bug to fix in this
skill. Prose in a skill file does not change a cron's behavior; only editing the
cron prompt does.

## Word-budget rationale

300 words is roughly 400 tokens loaded on every session. At dozens of sessions a
day that is the most-amortized text the agent maintains, so the bar for every
line is "does the agent need this to act correctly today." Static identity facts
do not belong here (they live elsewhere in USER.md); only the freshest signal
does.
