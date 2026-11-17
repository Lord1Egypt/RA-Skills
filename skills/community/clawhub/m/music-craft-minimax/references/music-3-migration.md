# Music 3.0 Migration Path

> **Status (2026-07-30): 🔴 BLOCKED.** `music-3.0` is the latest model
> in the MiniMax API but the installed `mmx` CLI (`mmx 1.0.16`) does
> **not** expose it. Skill continues to use `music-2.6` as the daily
> driver. Source: `music-craft-minimax_ROADMAP.md` v1.1.6 item **23**
> (🔴 HIGH) and `music-craft-ENHANCEMENT-PLAN.md` § "MiniMax Token Plan
> 2026 Updates".

## Current State

- **Active model:** `music-2.6` (mmx default). **Free:** `music-2.6-free`.
- **Legacy:** `music-2.5+`, `music-2.5`. **Cover:** `music-cover`,
  `music-cover-free`. **Not in mmx yet:** `music-3.0`.
- Do **not** change the default in `SKILL.md` or
  `mmx-flags-reference.md` until the checklist below completes.

## Verify the BLOCKED Status

Run before assuming Music 3.0 is still unavailable:

```bash
mmx --version                                                # expect 1.0.16+
mmx music generate --help | grep -A 1 -- '--model'
# Pre-migration: music-2.6 (default), music-2.5+, or music-2.5
# Post-migration target: music-3.0 (default), music-2.6, music-2.5+, music-2.5

# Smoke test (only after step 2 lists music-3.0):
mmx music generate \
  --prompt "Cinematic orchestral test, full instrumentation, 90 BPM" \
  --instrumental --model music-3.0 --timeout 600 \
  --out /tmp/music30_smoke.mp3
```

If step 2 still shows only `2.6 / 2.5+ / 2.5`, migration is **still
blocked** — stop.

## Migration Checklist

Execute in order when `mmx` adds `music-3.0`:

1. **Smoke-test.** Run the verification block above. Confirm the output
   is a valid MP3 ≥ 30 s, around `-16 LUFS`, and audible.
2. **Update `SKILL.md`.** Change default `--model` from `music-2.6` to
   `music-3.0`. Keep `music-2.6` as a documented fallback.
3. **Update `references/mmx-flags-reference.md`.** Add `music-3.0` to
   the "Model Selection" table as the new default; mark `music-2.6` as
   **fallback / verified baseline**.
4. **Update `scripts/lint_music_request.py`** if Music 3.0 changes
   prompt limits or duration (current: warn > 1800 bytes, error > 2000).
5. **Update `references/changelog.md`** under the next minor release
   (suggested v1.2.0 or v1.1.7), citing ROADMAP item **23**.
6. **Run one A/B comparison.** Generate the same prompt with
   `--model music-2.6` and `--model music-3.0`. Compare duration, LUFS,
   anti-sparse behaviour, audible quality; record in the changelog.
7. **Close roadmap item 23.** Tick `[x]` in
   `music-craft-minimax_ROADMAP.md` with date, files changed, and
   verification evidence per the tracking protocol.

## What to Watch For

- **`mmx` CLI releases.** Re-run
  `mmx music generate --help | grep -- '--model'` periodically. The
  blocker is the model-ID list, not a separate flag.
- **Token Plan quota.** Music 3.0 may consume a different share of the
  5h pool. Verify with `scripts/check_environment.py --quota` after a
  few generations.
- **Breaking changes.** Look for new prompt-byte limits, `--length`
  semantics, structure tags, or cover-workflow shifts. Canonical source:
  `platform.minimax.io`.
- **Backwards compatibility.** `music-2.6` and `music-2.6-free` must
  keep working — never remove the fallback row from the flag reference.

## Fallback

If Music 3.0 ships but produces broken / truncated / off-policy
output, **stay on `music-2.6`**:

```bash
mmx music generate --prompt "..." --model music-2.6 --out song.mp3
# Or omit --model — music-2.6 is the mmx default.
```

Do not roll back mid-batch. If the smoke test in step 1 fails, revert
the SKILL.md / flag-reference edits and reopen roadmap item 23 with
failure evidence.

## See Also

- `references/mmx-flags-reference.md` — current 2.6-first flag table.
- `references/minimax-generation-caveats.md` — duration / quality
  caveats that may shift with Music 3.0.
- `../music-craft-minimax_ROADMAP.md` item **23** — canonical status.
- `../music-craft-ENHANCEMENT-PLAN.md` § "MiniMax Token Plan 2026
  Updates" — research provenance.
