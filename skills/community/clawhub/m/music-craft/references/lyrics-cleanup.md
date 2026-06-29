# Lyrics Cleanup

Recipe for turning ASR/Whisper transcripts or messy song-folder lyrics into a
generation-ready lyric body.

## When To Load

Load this when lyrics come from:

- Whisper or another ASR transcript
- `lyrics_whisper_medium.json`
- a copied lyrics file with non-standard markers
- an `info.txt` file that mixes song notes, prior prompts, and lyrics fragments

## Canonical Tags

Normalize to a small set unless the arrangement needs more detail:

- `[Intro]`
- `[Verse]`
- `[Chorus]`
- `[Bridge]`
- `[Outro]`

Use numbered tags only when the distinction matters, such as `[Verse 1]` and
`[Verse 2]`. Avoid opaque tags like `[Section 9]`; they are useful for transcript
segmentation but weak instructions for a music model.

## Cleanup Steps

1. Preserve the user's actual lyric words unless they explicitly asked for a
   rewrite.
2. Remove transcript-only markers such as `[Section N]`, timestamps, ASR
   confidence labels, and repeated machine-generated headings.
3. Convert obvious song sections into canonical tags.
4. Remove repeated hallucinated phrases, stuck loops, and non-lyric artifacts
   such as "thank you for watching" when they came from a video transcript.
5. Re-flow long lines to roughly 80 characters or less so section boundaries are
   easy to review.
6. Keep instrumental moments as tags, not fake lyrics: `[Intro]`,
   `[Instrumental Break]`, or `[Outro]`.
7. Cross-check language against the requested `vocal_language`.

## `lyrics_whisper_medium.json`

Whisper JSON with segment timestamps is a valid input. Use timestamps to place
section tags when the song has long repeated sections or unclear structure.
Prefer the segment text for cleanup, but keep the JSON nearby for traceability.

## `info.txt`

Song folders may include `info.txt` with source URL, release notes, BPM, key,
instrumentation, prior prompt history, and analysis snippets. Treat it as prompt
seed material:

- use BPM/key/instrumentation when they are clearly labeled
- use prior prompt history to avoid repeating failed directions
- do not paste private notes or absolute local paths into the public prompt
- keep final prompts in a separate prompt file for reproducibility

## Quick Example

Before:

```text
[Section 1]
0:03 hello hello hello
[Section 2]
thank you for watching
[Section 9]
we ride on through the night
we ride on through the night
```

After:

```text
[Intro]
hello hello hello

[Chorus]
we ride on through the night
```

If cleanup changes the meaning, stop and ask the user whether they want a
faithful transcript cleanup or a rewritten lyric adaptation.

