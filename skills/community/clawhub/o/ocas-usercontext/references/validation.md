# Validation Checklist (Step 7)

Run this every time, before finishing. The previous version claimed these limits
but never checked them, so violations shipped daily. Each item is a hard gate.

## Size gates (hard — the file must never exceed the harness cap)

- [ ] **The whole USER.md stays under `context_file_max_chars`.** Resolve the
      effective cap (config override, else dynamic). After patching, the *total*
      file size must be `<= cap`. If it is not, the file would be truncated by the
      harness — re-compress and re-patch until it fits.
- [ ] **The block fits its budget:** `OTHER + block <= cap - margin`, where `OTHER`
      is every section except `## Daily Context`. The 300-word target is secondary
      to this.
- [ ] **No other section grew.** The patch did not enlarge, add, or reorder any
      section but `## Daily Context`; `OTHER` is unchanged from before the run.

## Format gates

- [ ] The block is **under 300 words** (soft target, under the hard size cap above).
      If over, re-compress (bullets to 8 words, mood to 1 dimension, week theme to 5
      words) and re-count.
- [ ] **No em dashes** anywhere in the block. Replace with commas/periods.
- [ ] **No markdown tables** in the block (chat renderers often do not render them).
- [ ] Each day bullet is **<= 12 words**; at most 3 bullets per day.
- [ ] The three dates are correct and consecutive: yesterday, today, tomorrow,
      relative to the actual run date in the host's local timezone (resolved at runtime).

## Content gates

- [ ] **Mood cites evidence or says `quiet (low signal)`.** No mood dimension may
      exist without a traceable session or email signal. If you cannot name the
      signal, delete the dimension. Calendar events are NOT mood evidence.
- [ ] **No fabricated events.** Every bullet maps to a real calendar entry, or the
      day says `No scheduled events`.
- [ ] **Location is real or `unknown`.** Not assumed from home base.
- [ ] **No private content leaked.** No message or email text is quoted in the
      block. Mood evidence is cited by channel only (e.g. `(messages)`). Outcomes
      seen on multiple channels are deduped, not double-counted.
- [ ] **Trajectory applied** when a prior snapshot existed: persisting moods
      marked `still`, changed moods marked `now`/`shifted`, vanished moods dropped.

## Safety gates

- [ ] The patch replaced **only** the `## Daily Context` block. Re-read USER.md
      and confirm the headings before/after Daily Context are byte-identical to
      before the run (identity, preferences, and other sections untouched).
- [ ] The block actually landed (re-read the file; do not trust the patch tool's
      return alone).

## On failure

If a gate fails, fix and re-validate before finishing. If the safety gates fail
(other sections changed), restore USER.md from the pre-run state and re-patch
with an exact `old_string` rather than fuzzy matching. Never leave USER.md in a
state where the patch may have clobbered another section.

## Delivery

Honor the configured `deliver` setting. The default is `local` (silent,
write-only): the patched block in USER.md is the entire deliverable; do not send
it to any chat. If `deliver` is set to a chat target, also push a copy there after
the patch lands. Either way, the patch is what matters; a delivery failure does
not invalidate the run.
