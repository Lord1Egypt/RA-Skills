# Voice Contract

> `humanize-text-skill` adds an explicit addition layer. The positive target for subtraction lives in [positive-style.md](./positive-style.md); this file defines what it means to pull a text toward a target voice and what "pulled correctly" looks like.

Both parent projects stop at "do not sound AI-generated." `avoid-ai-writing` uses voice profiles as constraints, such as shorter sentences or more contractions in casual mode. `shuorenhua` explicitly avoids fitting a named individual. `humanize-text-skill` goes one step further: it accepts a target voice and pulls the text toward it. But pulling is not flattening. The addition layer has its own boundaries.

## 1. What the addition layer is not

- It is **not** a house-style machine that flattens everyone into the same voice.
- It is **not** allowed to sacrifice information or terminology just to lower drift.
- It is **not** a replacement for subtraction; remove the residue first, then pull the voice.
- It is **not** imitation of private identity traits; it only fits observable writing-style dimensions.

## 2. What the addition layer is

It adjusts observable style dimensions toward a target profile:

| Dimension | Chinese measure | English measure | What it controls |
|---|---|---|---|
| Mean sentence length | characters per sentence | words per sentence | rhythm |
| Sentence-length CV | character variance | word variance | breathing room |
| Connector preference | preferred Chinese connectors | preferred English connectors | tone |
| Punctuation density | punctuation per character | punctuation per word | pacing |
| Contraction rate (`en`) | — | contractions per word | conversational looseness |
| First-person tendency | `我 / 我们` frequency | `I / my / we` frequency | stance |

Target values come from [policy/voice.toml](../policy/voice.toml) (`none` plus 6 profiles and `custom`) or are calibrated from an author sample via `voiceMode: 'custom'`.

## 3. What a correct pull looks like

### 3.1 Rhythm alignment, not sentence-by-sentence alignment

If the target average is 12 words, that does **not** mean every sentence should become 12 words long. A correct pull creates a plausible spread, including a few shorter interruptions that break metronomic uniformity.

### 3.2 Connector preference, not connector stuffing

If the target prefers `but` or `so`, that does not mean every transition should be replaced with those words. A correct pull uses target-favored connectors only where they sound natural.

### 3.3 First-person when the target allows it, but never faked

If `first_person_ok: true`, the layer may encourage forms like `I think` or `we changed`, but it must never invent stance or judgment just to satisfy the profile. First-person voice must still come from the content.

## 4. Hard boundaries: the fidelity gate always wins

Voice suggestions must **never**:

- alter protected spans such as numbers, commands, paths, errors, versions, or quotes
- invent facts, sources, or judgments that are not already present
- replace necessary technical terms with casual substitutes
- damage information integrity for the sake of lower drift

When voice advice conflicts with fidelity, **fidelity wins**. A higher drift score is acceptable. Distorted text is not.

## 5. How to read drift

- **0-20**: already close to the target voice; little or no addition work needed
- **20-50**: some distance remains; after subtraction the text may naturally move closer, so only light suggestions are needed
- **50-80**: clearly off-target; the addition layer should give concrete split, vary, or connector guidance
- **80-100**: strong style mismatch; often the wrong voice profile was chosen, or the text needs rewriting before voice pull is worth doing

High drift does **not** mean bad writing. A technical document can have high drift against `casual` and still be correct. In that case, the right fix is often to choose `technical`, not to force the document into casual voice.

## 5.1 Clean but still flat

A low `score` only means the subtraction layer is clean. It does not mean the text already sounds human. Common cases:

- the vocabulary is clean but sentence lengths are still too uniform
- obvious AI phrases are gone, but the paragraph still has no stance or breathing room
- every sentence is acceptable, but all of them feel like default-template sentences

When this happens, stop hunting more patterns. Look at `voice.drift` and whether the chosen scene and voice actually match.

Useful interpretation:

- low `score` + high `voice.drift`: clean, but stylistically off-target
- low `score` + medium `voice.drift`: basically sendable, with light addition-layer work
- low `score` + low `voice.drift`: subtraction and addition are both in good shape

At the user level, the explanation should stay plain: "This version no longer reads very AI-like, but it is still flat and templated, so I only made light voice-pull edits and did not reopen the factual layer."

## 6. Three independent dimensions

`score` (AI density), `fidelity` (truth-preservation gate), and `voice.drift` (distance from target voice) are **independent dimensions** and must never be collapsed into one number.

- high `score` + high `drift`: remove residue first, then consider voice pull
- low `score` + high `drift`: the text is clean but stylistically off-target; this is pure addition-layer work
- high `score` + low `drift`: rare, but possible when a real person writes AI-shaped prose in a voice that otherwise matches

See [evals/voice-samples.md](../evals/voice-samples.md), especially `VS-03`, for the independence check.
