# Audition Rubric

Structured evaluation of generated music across five quality dimensions. Use
this **after** every generation and **before** delivery, batch selection, or
revision. A track that passes every automated check
([`audio_quality.py`](../../tests/analyzers/audio_quality.py)) can still
fail the rubric — well-formed audio is necessary but not sufficient.

## When To Load

- After a generation completes and you need to decide: accept, revise,
  regenerate, or reject.
- When picking a "best" from a batch of candidates (item 12 of the base
  skill's ROADMAP).
- When iterating with `seed`-locked runs and need to score small deltas.

## Cross-References

- **Existing quality reference:** [`quality-and-revision.md`](quality-and-revision.md)
  (request-fit checklist, revision prompts, delivery copy).
- **Technical analyzer:** [`../../tests/analyzers/audio_quality.py`](../../tests/analyzers/audio_quality.py)
  (auto-fills the Technical Quality dimension; LUFS, SNR, peak, RMS,
  silence, clipping).
- **Lyrics alignment validator:** [`../../tests/analyzers/lrc_validator.py`](../../tests/analyzers/lrc_validator.py)
  (use when the request includes a `.lrc` file).
- **Roadmap item:** `music-craft_ROADMAP.md` § v1.1.5 item 13a.
- **Source:** youtube-studio `LOCAL-MUSIC-CAPABILITIES.md` § "Audition
  rubric (must pass before promotion)" + `MUSIC-CAPABILITIES.md` §
  "Audition rubric (Gate 4 DoD)".

## 1. The Five Dimensions

Each dimension scores **1–5**. Score 3 is the bare-minimum bar for
acceptance; anything below 3 in any dimension triggers a revision or
rejection (see § 3 Decision Matrix).

| # | Dimension | What it measures | Scoring aids |
| --- | --- | --- | --- |
| 1 | **Musicality** | Melody coherence, harmonic movement, rhythmic stability, phrase shape | Listen for repeated motifs, singable contour, no random percussive spikes in a "no percussion" prompt |
| 2 | **Production quality** | Mix balance, mastering loudness, dynamic range, stereo image | Cross-check with `audio_quality.py` peak/RMS/LUFS output |
| 3 | **Prompt adherence** | How well the output matches the user's stated genre, mood, BPM, key, instruments, structure, vocals/lyrics | Re-read the original prompt; confirm every named element is audible |
| 4 | **Vocal quality** *(if applicable)* | Intelligibility, emotion, pronunciation, language match, breath/noise artifacts | Skip and note "n/a (instrumental)" for instrumental outputs |
| 5 | **Technical quality** | LUFS, peak headroom, SNR, silence ratio, clipping, sample rate | **Auto-scored** by `audio_quality.py` — see § 5 |

## 2. Scoring Guide

| Score | Meaning | Action implication |
| --- | --- | --- |
| **5 — Excellent** | Polished, professional, matches every requested element | Accept. Promote as the candidate. |
| **4 — Good** | Solid; minor issue that does not block delivery | Accept with a one-line caveat; consider revision only if cheap |
| **3 — Acceptable** | Meets the bar; noticeable weakness but not a defect | Accept as fallback; revise if a 4-or-better candidate is achievable in the same budget |
| **2 — Weak** | Below the bar; at least one dimension is broken | Revise with a targeted `REVISION:` block (see `quality-and-revision.md`); if revision fails, regenerate |
| **1 — Unusable** | Hard failure (clipping, silence, wrong language, artifact in first 10 s) | Reject immediately; do not revise, regenerate from scratch |

## 3. Decision Matrix

| Lowest dimension score | Action |
| --- | --- |
| **5** in every dimension | **Accept.** Promote as final candidate. |
| **4** in every dimension | **Accept.** Note any 4-dimension issues in the delivery summary. |
| One **3**, rest ≥ 4 | **Accept as fallback** if no better candidate exists; otherwise iterate. |
| One **2**, rest ≥ 3 | **Revise.** Build a `REVISION:` block targeting the failing dimension (see `quality-and-revision.md` § Revision Prompts). One revision attempt, then regenerate if still ≤ 2. |
| Two or more **2**s, or any **1** | **Reject + regenerate.** Do not mutate the failed attempt; create a child revision (`M2_*`, `v2_*`) with a tighter prompt. |
| Any dimension **1** | **Hard fail.** Stop iterating on this prompt family; rethink the prompt or pick a different backend. |

**Rule:** if a track fails the rubric, create a child revision
(`M2_*`, `v2_*`) — never mutate the rejected attempt in place. Preserved
rejections are useful evidence when comparing prompt variants later.

## 4. Mandatory Listenability Checks (must pass before any score ≥ 3)

These three checks come from youtube-studio's Gate 4 DoD. A track that
fails any one of them **cannot score above 2** in Musicality or Prompt
Adherence, regardless of how well it scores elsewhere.

1. **Instrumental coherence.** If the prompt says "no percussion" or
   "ambient pads only", the output must contain no random percussive
   spikes, drum hits, or rhythmic kicks. Likewise, if the prompt names
   specific instruments, each must be clearly audible (silence on a
   named instrument is a failure).
2. **No artifacts in the first 10 s.** Cold-start silence, a clicky
   attack, a glitch, or a sudden volume jump in the first 10 seconds is
   a red flag. Rewind and re-listen to the opening before scoring.
3. **Listenable at the chosen gain.** A bed meant for narration
   underlay (typical mix gain ~0.18 with 2 s fades) should not compete
   with speech when played at that level. If you have to turn the gain
   *down* to avoid distraction, the mix is too busy.

If any check fails, drop the relevant dimension to **2** and route to
**Revise** or **Reject** per the Decision Matrix.

## 5. Integration with `audio_quality.py`

The Technical Quality dimension is automated. Run:

```bash
python tests/analyzers/audio_quality.py path/to/track.wav --json
```

Map the JSON output to the score:

| `audio_quality.py` result | Technical score |
| --- | --- |
| `"passed": true`, all fields inside default thresholds | **5** |
| `"passed": true`, but LUFS is louder than -14 or quieter than -20 | **4** |
| One soft threshold violated (RMS, silence ratio borderline) | **3** |
| One hard threshold violated (peak > -0.5 dBFS, clipping > 0.1 %, silence > 30 %) | **2** |
| `file_read_error` or duration outside `[1 s, 600 s]` | **1** |

The analyzer exits with code `0` on pass, `1` on fail, `2` on error —
use that as a gate before the human-audition step, not as a replacement
for it.

## 6. Integration with `lrc_validator.py`

If the request included a `.lrc` file (see
[`lrc-generation.md`](lrc-generation.md)), validate it alongside the
audio:

```bash
python tests/analyzers/lrc_validator.py path/to/song.lrc --json
```

A valid LRC file raises the Vocal Quality dimension by up to one point
(accurate timing makes vocals easier to assess). An invalid LRC file
(`"valid": false` or any `errors[]`) drops Vocal Quality to **2** unless
the request did not ask for lyrics alignment.

## 7. Example Evaluations

### Example A — Accept (5/4/5/5/5)

> ACE-Step local, 30 s dream-pop instrumental, BPM 92, key Em.
>
> | Dimension | Score | Note |
> | --- | --- | --- |
> | Musicality | 5 | Shimmering guitar arpeggios + pad, gentle 4-on-floor kick, clear verse/chorus shape |
> | Production | 4 | Slightly bright cymbals; otherwise balanced |
> | Prompt adherence | 5 | Genre, BPM, key, instruments, structure all match |
> | Vocal quality | n/a | Instrumental |
> | Technical | 5 | `audio_quality.py` passed; LUFS -16.2, peak -2.1 dBFS |
>
> Mandatory checks: all pass. **Decision: Accept.** Promote as candidate.

### Example B — Revise (4/3/3/3/5)

> mmx Music 2.6, 180 s English vocal pop, BPM 120.
>
> | Dimension | Score | Note |
> | --- | --- | --- |
> | Musicality | 4 | Catchy chorus, but the bridge is harmonically static |
> | Production | 3 | Mix is balanced but the vocal sits behind the synth bus |
> | Prompt adherence | 3 | Genre and BPM match; key drifted from C to G |
> | Vocal quality | 3 | Pronunciation clean, but emotion is flat in the bridge |
> | Technical | 5 | `audio_quality.py` passed |
>
> Mandatory checks: pass. **Decision: Revise** — one `REVISION:` block
> targeting vocal-forward mix + bridge dynamics + key correction.

### Example C — Reject (4/5/2/n/a/2)

> MusicGen local, 30 s lo-fi instrumental, "no percussion" prompt.
>
> | Dimension | Score | Note |
> | --- | --- | --- |
> | Musicality | 4 | Warm Rhodes + vinyl texture; pleasant |
> | Production | 5 | Clean mix, good stereo image |
> | Prompt adherence | 2 | Random shaker hits every 4–6 s — fails Instrumental Coherence |
> | Vocal quality | n/a | Instrumental |
> | Technical | 2 | Silence ratio 0.34 (over the 0.30 threshold) |
>
> Mandatory checks: **Instrumental coherence fails** (percussion present
> despite "no percussion"). **Decision: Reject + regenerate** with the
> prompt re-stating the constraint and adding "no shaker, no kick, no
> hi-hat" explicitly.

## 8. Quick Audit Checklist

When you are short on time, run this in order. If any item fails, the
track fails the rubric.

```text
[ ] 0–10 s opening: no clicks, no silence dropouts, no volume jump
[ ] Prompt-named instruments are audible (silence on a named instrument = fail)
[ ] Prompt-excluded instruments are absent (percussion in "no percussion" = fail)
[ ] `audio_quality.py` exits 0 (LUFS, peak, SNR, silence, clipping all in range)
[ ] If `.lrc` was requested: `lrc_validator.py` exits 0
[ ] At target gain (~0.18 for beds), track does not compete with narration
[ ] Total score across the five dimensions ≥ 3 in every row
```

If seven boxes tick, the track passes.
