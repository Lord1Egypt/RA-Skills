# Error Handling (MiniMax-Specific)

The base skill's [`error-handling.md`](../../music-craft/references/error-handling.md) covers generic failures. This file covers MiniMax-specific failure modes, especially for the advanced features (cover, mashup, emotion analysis, lyrics generation API).

## mmx CLI Errors

| Error | Cause | Fix |
|---|---|---|
| `mmx: command not found` | CLI not installed | Install via the MiniMax install guide, or skip mmx-specific features |
| `401 Unauthorized` | Bad or expired API key | `mmx auth login --api-key "$MINIMAX_API_KEY"` |
| `403 Forbidden` | API key does not have the required plan | Upgrade to a Token Plan that includes the feature |
| `429 Too Many Requests` | RPM or Token Plan quota exceeded | Wait 60s; check Token Plan usage; reduce concurrency |
| `Region mismatch` | CLI default region is wrong | `mmx config set --key region --value global` |
| `Network error` | Connectivity issue | Check internet, retry with `--retry 3` |
| `Invalid prompt` | Prompt has forbidden content | Check for copyrighted lyrics, hate speech, etc. |
| `Lyrics too long` | > 3500 chars | Shorten or split into sections |
| `Audio file too large` | > 50 MB | Convert with `ffmpeg -b:a 128k` to lower bitrate |
| `Audio file too long` | > 6 minutes | Trim with `ffmpeg -t 360` |

## Cover Workflow Errors

| Error | Cause | Fix |
|---|---|---|
| `audio_url unreachable` | Local file path is wrong, file is unreadable, or you passed a streaming URL where a `file://` path is required | Confirm the local file exists and is readable; if you only had a streaming URL, fetch it first with the private `music-source-fetch` skill |
| `cover_feature_id expired` | > 24 hours since preprocess | Re-run preprocess |
| `cover_feature_id invalid` | ID was mistyped or not from this API key | Re-run preprocess, copy ID carefully |
| ASR extracted wrong lyrics | Noisy audio, accented vocals, non-English | Use two-step with manually-edited lyrics |
| Output melody is unrecognisable | Style transfer too aggressive | Reduce the prompt's style intensity, or use a less dramatic target style |
| Output is sparse | Anti-sparse rules not applied | Add explicit instruments and "ALL instruments ALWAYS playing" |
| Output is the same as the input | Style transfer did not apply | Check the prompt; make style descriptors more specific |
| Output has vocals when instrumental was requested | `--instrumental` flag was not set, or model does not support the language | Set `--instrumental` and try again |
| Output duration is wrong (too short, e.g. 30-60s when you wanted 3:30) | `--length` is only a hint | Length is driven by **lyrics length** (primary) + **structure tags** (secondary) + **`--length` / prompt hints** (tertiary). For a 3:30 song you need ~150-200 lyrics words with full song structure (`[Verse 1]`/`[Pre-Chorus]`/`[Chorus]`/`[Verse 2]`/`[Bridge]`/`[Outro]`). Add prompt hints like "3 minute song", use `--length 210000`, or use `--structure "intro-verse-pre_chorus-chorus-verse-chorus-bridge-chorus-outro"`. If you need precise length, switch to `music-craft`'s ACE-Step backend which has `audio_duration`. |
| Output duration is wrong (too long, e.g. 5+ min when you wanted 3:30) | Lyrics are too long, or model is filling sections slowly | Trim lyrics to ~120 words, add explicit `[Instrumental Break]` tags to control pacing, or remove the bridge section. |

## Lyrics Generation API Errors

| Error | Cause | Fix |
|---|---|---|
| `mode is required` | Missing `mode` in request body | Add `"mode": "write_full_song"` or `"edit"` |
| `prompt is required` | Missing `prompt` | Add the theme/style instruction |
| `lyrics is required for edit mode` | `edit` mode without `lyrics` field | Add existing lyrics to edit |
| `lyrics too long` | > 3500 chars | Shorten or split |
| `prompt too long` | > 2000 chars | Shorten |
| Output is in wrong language | Prompt did not specify language | Add language: "in French", "en español", "auf Deutsch" |
| Output is too short | Prompt was vague | Add: "with at least 3 verses, 2 choruses, and a bridge" |
| Output is too long | Prompt asked for too much | Add: "concise, 2 verses and 1 chorus" |
| Output is AI-generic | Prompt was generic | Add specific imagery: "mention a specific place, time of day, object" |
| Edit mode did not modify enough | Prompt was not specific about what to change | Be explicit: "make the chorus stronger", "add a bridge about X" |

## Emotion Analysis Errors

| Error | Cause | Fix |
|---|---|---|
| `librosa.load fails` | Unsupported format | Convert via `ffmpeg -i input.m4a output.wav` |
| `No pitch detected` | Instrumental only | Skip emotion analysis, use basic features only |
| `Very short audio` | < 5 seconds | Skip emotion analysis, warn the user |
| `Too quiet / clipping` | Bad levels | Normalize a delivery copy: `ffmpeg -i input.mp3 -af loudnorm=I=-16:TP=-1:LRA=11 -ar 48k output.mp3` |
| `parselmouth not installed` | Optional dep missing | `pip install praat-parselmouth` (better pitch tracking) |
| `allin1 not installed` | Optional dep missing | `pip install allin1` (neural structure segmentation) |
| Analysis takes too long | Very long audio or many sections | Trim to a representative 3–4 minute segment |
| Output JSON is incomplete | Process killed or error mid-run | Run with `--verbose` to see the error, fix and retry |

## Mashup Workflow Errors

| Error | Cause | Fix |
|---|---|---|
| `Song A audio missing` | User only had a URL and the published skill no longer downloads audio | Fetch the file with the private `music-source-fetch` skill and retry with the local path |
| `Song B style unknown` | LLM does not have training data for Song B | Ask the user for a 2–3 sentence description of Song B's style |
| `Cover preserved wrong melody` | ASR extracted wrong lyrics, the model anchored on the wrong phrases | Use two-step with manually-edited lyrics |
| `Output is sparse` | Anti-sparse rules not applied for the unusual combination | Add explicit anti-sparse text, list every instrument |
| `Output is too long` | Combined content is too rich | Trim the lyrics, drop a verse or chorus |
| `Emotion analysis contradicted by Song B style` | Song A is melancholic, Song B is upbeat | Embrace the tension or adjust one of them; this is a creative call |

## Retry Adjustment Rules

Use one focused retry before widening the workflow. Change the smallest thing that addresses the failure:

| Failure | First retry adjustment | If it still fails |
|---|---|---|
| Cover loses melody | Switch to two-step, add `preserve the original melody contour`, remove half the style adjectives, and keep the original lyric line breaks | Lower the target intensity and simplify the style to fewer descriptors |
| ASR lyrics are wrong | Re-run as two-step and replace ASR text with manually corrected lyrics or a user transcript; add the source language explicitly | Ask the user for the exact lines or fall back to translated/new lyrics |
| Mashup is incoherent | Keep Song A lyrics/structure fixed, reduce Song B to 3-5 style descriptors, and make Song B style secondary to Song A content | Fall back to standard generation with a single combined prompt |
| Emotion is too flat | Add section contrast, `[Break]` and `[Build Up]` tags, and stronger dynamic words for chorus/bridge changes | Narrow to one dominant emotion and drop weak secondary emotions |
| `mmx` flags conflict | Make flags the source of truth for BPM/key/structure and remove the same values from the prompt | Keep only the mandatory flags and shorten the prompt to feel-only language |
| Audio source is a URL (refused by linter) | The published skill no longer accepts streaming URLs | Fetch the file with the private `music-source-fetch` skill and retry with the local path |

## Rate Limits (MiniMax-specific)

The MiniMax Music 2.6 documented limits are:

- **RPM:** 120 requests per minute
- **Concurrent connections:** 20
- **Output URL expiry:** 24 hours (download the audio promptly)
- **Cover feature ID validity:** 24 hours (use the preprocess output within a day)

Under the **Token Plan 3.0** (June 2026+), the actual quota is credit-based rather than RPM-based:

- A unified `general` credit pool covers M3, M2.7, and M2.7-highspeed
- A 5-hour rolling window resets continuously
- A weekly window runs Monday 02:00 CEST → next Monday 02:00 CEST
- Weekly status may be inactive on Plus plan (no weekly cap enforced, but the schema is there)

Practical implication: **the documented 120 RPM is the API limit, but the Token Plan 3.0 quota is what determines your real ceiling.** If you generate 4500 requests in 5 hours on Plus, you will be rate-limited regardless of RPM.

If a call fails with 429 (rate limit):

1. Wait at least 60 seconds.
2. Check the Token Plan usage endpoint (see `## Token Plan 3.0 Specific Issues` below for the usage-check command).
3. If 5h window is exhausted, wait for the reset.
4. Reduce concurrency if running a batch.

## Token Plan 3.0 Specific Issues

Under Token Plan 3.0 (June 2026+), the quota is credit-based. Common issues:

| Symptom | Cause | Fix |
|---|---|---|
| 429 errors with no clear pattern | Token Plan 5h window exhausted | Wait for the 5h reset, or upgrade plan |
| All calls fail with auth error | API key revoked or expired | Regenerate API key in MiniMax dashboard |
| Output quality degrades over time | Quota running low, model degrades to cheaper path | Check Token Plan usage, upgrade if needed |
| Weekly cap hit (rare on Plus) | Weekly window exhausted | Wait for Monday 02:00 CEST reset |

To check current Token Plan usage:

```bash
curl -s -H "Authorization: Bearer $MINIMAX_API_KEY" \
  https://www.minimax.io/v1/token_plan/remains | jq .
```

## Sparse / A Cappella Output (MiniMax-Specific)

MiniMax is more aggressive than other providers in interpreting "sparse" as "remove all instruments". Special fix path:

1. **Add the canonical anti-sparse text** to the prompt:
   ```
   ALL instruments ALWAYS playing throughout the entire song, NEVER go a cappella or silent at any point
   ```

2. **List every instrument** you want to hear, even if they are obvious:
   ```
   accordion, upright bass, orchestral strings, piano, light percussion
   ```
   Do not say "with strings" — say "orchestral strings (violin, viola, cello)".

3. **Add explicit treatment of quiet sections**:
   ```
   quiet sections: reduced to accordion and bass only, still fully played, NOT silent
   ```

4. **Use `--avoid` with the canonical list**:
   ```
   sparse, a cappella, minimal arrangement, electronic sounds, synthetic textures
   ```

5. **If still sparse after one retry**, switch to a different style. The combination of style + prompt may be incompatible.

6. **Never** use these phrases alone in a MiniMax prompt:
   - `sparse arrangement`
   - `minimal instrumentation`
   - `stripped back`
   - `a cappella section`
   - `quiet and sparse`
   - `minimal but present`

   If the user asks for any of these, translate into the explicit-instrument form.

## Anti-Sparse (MiniMax-Specific Deep Dive)

<!-- Same-recipe note: this section and ## Sparse / A Cappella Output (MiniMax-Specific) above cover the same failure mode in different wording. The section above is the step-by-step fix path; this section is the diagnostic framing. Keep both; see also the section above for the canonical prompt text and phrase list. -->

The base skill's anti-sparse rules apply. The MiniMax-specific failure mode is more severe than other providers:

**MiniMax interprets "sparse" or "minimal" as "remove all instruments"**, even more aggressively than other providers. The model has been observed to:

- Remove all instruments in quiet sections when the prompt uses the word "quiet"
- Drop percussion entirely when the prompt uses "intimate"
- Go a cappella on build-up sections when the prompt uses "build"

Mitigation:

- **Never use the words "sparse", "minimal", "stripped back", "quiet" in a MiniMax prompt without pairing them with explicit instruments.**
- Always add: `"ALL instruments ALWAYS playing throughout, NEVER go a cappella or silent at any point"`.
- Always list every instrument you want to hear.
- For quiet sections, use the explicit form: `"quiet sections: reduced to accordion and bass only, still fully played, NOT silent"`.

If a generation comes back sparse despite these rules, retry once with an even more explicit instrument list. If it fails again, the prompt has a structural issue — try a different style.

For the canonical anti-sparse text, worked examples, and the phrase blocklist, see `## Sparse / A Cappella Output (MiniMax-Specific)` above and the base skill's Anti-Sparse Rules section.

## Output Verification (Covers, Mashups, Style Transfer)

After generation, run a post-generation check that is specific to the route. Use the analysis orchestrator's output on the generated file when possible.

### Verification Checklist per Route

**Cover (`minimax_cover`)**

- [ ] Melody recognisable as the source (basic-pitch MIDI compare or ear-test)
- [ ] Target style is clearly audible (genre/mood keywords present)
- [ ] Source BPM is within ±10 BPM
- [ ] Source key is preserved (or user agreed to shift)
- [ ] Lyrics decision respected (original / translated / new / instrumental)
- [ ] `--avoid` flags respected

**Mashup (`minimax_mashup`)**

- [ ] Song A's lyrics and emotional arc recognisable
- [ ] Song B's style is dominant in the production
- [ ] Vocal intensity matches Song A's emotion curve
- [ ] Section structure feels coherent (not random)
- [ ] `--avoid` flags respected for Song B's style

**Style Transfer (`minimax_style_transfer`)**

- [ ] Source style (the reference track) is reproduced in timbre, instrumentation, and feel
- [ ] Output melody is NOT recognisable as the source (it is a new composition in the source style)
- [ ] Target genre/mood keywords audible
- [ ] BPM and key reasonable for the new style (not forced from source)

**Emotion Prompt / Precision (`minimax_emotion_prompt`)**

- [ ] Per-flag values (BPM, key, structure, avoid) match the flags
- [ ] Prompt language and flags are not contradicting (linter clean)
- [ ] Lyrics reflect the requested theme and language

### Failure Signatures and Fixes

When the generated track does not match the request, identify the failure signature and apply the matching fix. The most common signatures:

| Failure signature | Likely cause | Fix |
|---|---|---|
| **Copied too closely** (cover sounds like a remaster, not a new style) | Prompt did not specify the new style firmly enough, or `--avoid` list left the original instrumentation unguarded. | Add explicit target style language, list new instruments, expand `--avoid` with the source's dominant sounds. Re-run. |
| **Lost source melody** (cover no longer recognisable) | `--prompt` overrode the cover model, or the source audio was too noisy / clipped. | Switch to the two-step cover workflow (preprocess + generate with `cover-feature-id`); reduce style strength in the prompt. |
| **Wrong tempo** (BPM noticeably off) | Prompt and `--bpm` disagreed, or vocal delivery speed misled the detector. | Lint prompt + flags first. Re-run with the linter-clean pair. If still off, set `--bpm` explicitly and drop the BPM number from the prompt. |
| **Wrong key** (key shifted up/down) | Prompt mentioned a key but flags used another. | Lint the pair. Use the same key in both. If MIDI confirms a different source key, trust MIDI over prompt. |
| **Muddy mix** (low clarity, washed out) | Overly dense instrumentation, lack of anti-sparse guard, or too many `--avoid` exclusions. | Reduce instrument count, raise `--bpm` for tightness, add explicit "all instruments clearly audible". |
| **Vocals too neutral** (no emotion) | Emotion analysis not run, or intensity curve not transferred. | Run `analyze_vocal_emotion.py` on the source and feed `intensity_curve` into the prompt. Add explicit "vocal intensity: ..." clause. |
| **Weak chorus** (chorus does not lift) | Structure line lacks a build cue, or the prompt was a single energy. | Add structure with explicit build cues: "verse: intimate, chorus: soaring, all instruments louder in chorus". |
| **Style mismatch** (output does not match the requested genre) | Prompt used vague genre words or the wrong dominant instrument. | Replace vague words with concrete genre + instrument list. Use the canonical `mmx` prompt schema in `examples.md`. |

### Revision Prompt Templates

When a generation comes back with one of the failure signatures above, build a revision prompt that preserves the source identity while changing the failing dimension.

**Template: stronger style change (cover too close)**

```
Same melody and lyrics as before. Re-imagine the production as [TARGET_STYLE] with [INSTRUMENT_LIST].
ALL instruments always playing throughout, never go a cappella.
Avoid: [STYLE_CONTRADICTING_WORDS from previous run].
```

**Template: keep the melody (cover lost it)**

```
Re-apply the original melody from the source audio. Keep the recognizable hook at [HOOK_TIME].
Use a softer production in [TARGET_STYLE] but DO NOT change the melodic contour.
Avoid: [WORDS_THAT_PUSHED_TOO_FAR].
```

**Template: fix tempo drift**

```
Keep the source BPM (use --bpm [SOURCE_BPM]). Do not slow down or speed up the vocal delivery.
Avoid: rubato, half-time, double-time, slowing down, speeding up.
```

**Template: fix key shift**

```
Stay in [SOURCE_KEY]. Do not transpose. Use the same chord progression as the source.
Avoid: key change, modulation, transpose.
```

**Template: fix muddy mix**

```
Make every instrument clearly audible. Reduce instrument count to [N].
Add contrast: quieter verses, louder choruses. Keep vocals upfront in the mix.
Avoid: dense layering, atmospheric washes, sustained pads throughout.
```

**Template: lift the chorus**

```
Chorus: soaring, all instruments louder than the verse, fuller chords, more reverb on the lead vocal.
Verse: intimate, single voice, soft drums, breathy delivery.
Bridge: build tension, add a melodic lift before the final chorus.
```

These templates pair with the failure-signature table. After the revision, re-run the verification checklist above.

## When to Give Up and Ask the User

If after 2 retries the result is still unacceptable:

1. Show the user the best attempt so far.
2. Explain what was tried and why it failed.
3. Ask the user for:
   - A clearer direction (specific style, reference artist, sample audio)
   - Permission to try a different model (`music-2.6` vs `music-2.6-free`)
   - Permission to switch to standard generation instead of cover (for mashups)
   - Acceptance of the best result with a note about the limitation

Never loop forever. Always give the user an off-ramp.

## When to Fall Back to the Base Skill

If the MiniMax-specific features are causing problems, fall back to `music-craft`:

- Cover is failing → use standard generation with the style as a reference (no melody preservation)
- Mashup is failing → use standard generation with a combined prompt
- Emotion analysis is failing → skip it, build the prompt from LLM knowledge of the songs
- mmx CLI is unavailable → use the `music_generate` tool with prompt-only

The base skill is the safety net for the advanced features.
