# Quality, Rate Limits, and Revision

Rate-limit handling, the request-fit checklist, revision-prompt patterns
with worked examples, and lyrics-optimizer behavior. Load this after a
generation that needs verification against the request, or when iterating.

## Rate Limits

Different providers have different limits. The exact values depend on the active OpenClaw runtime configuration, but the common ranges are:

| Tier | Typical RPM | Notes |
|---|---|---|
| Free / trial | 5–20 | Lower concurrency, watermarking may apply |
| Standard paid | 60–120 | Generous for personal use |
| Heavy / batch | 1000+ | Dedicated plans |

Defaults to assume (for the most common providers):

- **RPM (requests per minute):** 120
- **Concurrent connections:** 20
- **Output URL expiry:** 24 hours (download the audio promptly)

Before submitting a batch, check the active provider's plan. Generating 10 variations in quick succession on a free tier will rate-limit the 3rd or 4th call.

If a call fails with 429 (rate limit):

1. Wait at least 60 seconds before retrying.
2. Reduce concurrency if running a batch.
3. Try once with the same payload before adjusting the prompt — the issue is the limit, not the content.

See also [error-handling.md](error-handling.md) for the 429 entry in the Generation Errors table and the Retry with same payload recovery pattern.

## Request-fit checklist

The eight items in the Quality Verification Checklist in SKILL.md cover audio quality. In addition, confirm that the output matches the user's original request on these specific points. If any item fails, the prompt needs adjustment before delivery.

| Check | What to confirm | Failure action |
|---|---|---|
| Language | Vocals are in the requested language | Restate language in prompt; ensure lyric body is in the same language |
| Vocal / instrumental mode | Instrumental request has no vocals; vocal request has vocals | Add or remove `Instrumental only, no vocals`; check `instrumental` flag |
| Section structure | Number and order of sections match the plan | Add or correct `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]` tags in the lyrics |
| Lyrics source | If user provided lyrics, the words appear recognizably | Stop and tell the user the generator paraphrased their text; revert to a tighter prompt |
| Duration | Output length is in the requested range | Add or trim sections in the lyrics body; long output rarely comes from more length, only from more tagged sections |
| Stylistic references | Named artists or eras come through in genre / instruments / vocals | Translate the reference into concrete descriptors; add them to the prompt |

If 3+ request-fit items fail, regenerate with a revised prompt. If 1–2 fail, warn the user and offer a targeted fix. For the specific fix patterns, see [error-handling.md](error-handling.md).

## Revision Prompts

When the output is close but not right, do not regenerate from scratch. Build a **revision prompt** that only changes the failing element and keeps everything else intact.

### Pattern

Keep 80% of the original prompt. Add a single `REVISION:` block at the end that targets the specific failure.

```
[Original prompt, unchanged]

REVISION:
- [Specific change 1]
- [Specific change 2]
- Keep: [elements that already work and should NOT change]
```

Always pass the same lyrics body for revision requests unless the lyrics themselves are the failure.

### Examples

**Output is too sparse:**

```
[Original prompt]

REVISION:
- Strengthen the anti-sparse guard: "ALL instruments ALWAYS playing, NEVER a cappella"
- Re-list every instrument: accordion, upright bass, strings, piano, light percussion
- Quiet sections: reduce to accordion and bass only, still fully played
- Keep: language, vocal type, structure
```

**Output is in the wrong language:**

```
[Original prompt]

REVISION:
- Vocals in [target language] only, no English
- Lyric body is already in [target language] — keep as is
- Keep: genre, mood, instruments
```

**Chorus is weak:**

```
[Original prompt]

REVISION:
- Chorus: melody-driven, hook-forward, with sustained vowels
- Add a [Pre Chorus] section before each [Chorus] for build
- Keep: verse style, language, instruments
```

**Vocal mode is wrong (vocals in instrumental, or silent in vocal request):**

```
[Original prompt]

REVISION:
- [Add or remove] "Instrumental only, no vocals" line
- If vocals were missing: add "lead vocal in [language], [register], [delivery]"
- Keep: genre, mood, structure
```

For the full retry recipe library (wrong language, weak chorus, sparse arrangement, vocals in instrumental, missing genre identity, too generic output), see [error-handling.md](error-handling.md).

## Delivery Copy

For delivery copies, normalize loudness after generation:

```bash
ffmpeg -i input.mp3 -af loudnorm=I=-16:TP=-1:LRA=11 -ar 48k output.mp3
```

Then verify:

- duration is within the user's tolerance
- integrated loudness is near -16 LUFS for the delivery copy
- true peak is around -1 dBTP
- file size is reasonable
- there are no obvious silence drops, clipping, or artifacts

## Lyrics Optimizer Behavior

When `music_generate` is called **without explicit lyrics** and the request implies a vocal track (not instrumental), the runtime may auto-generate lyrics from the prompt. The exact behavior depends on the provider:

| Provider | Behavior when no lyrics |
|---|---|
| MiniMax | Calls `lyrics_optimizer: true` automatically; generates structured lyrics matching the prompt's theme and language |
| ACE-Step | Uses 5Hz LM (when `thinking=true`) to rewrite tags and generate audio codes; can fill in missing metadata |
| ElevenLabs | Requires explicit lyrics; without them, returns instrumental or errors |
| Other | Varies — check provider docs |

This means: if the user did not provide lyrics and did not say "instrumental", the output will have AI-written lyrics in the language and theme implied by the prompt. If the user wants specific words, they must provide them. If they want no vocals, set `instrumental: true`.

If the user is surprised by the AI-written lyrics, that is a workflow issue (the Pre-Flight should have asked), not a generation issue. Adjust by asking the user next time whether they want auto-lyrics or want to provide their own.
