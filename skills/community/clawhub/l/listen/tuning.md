# Tuning — Fixing the Engine Instead of the Transcript

The repair layer handles errors; this file removes them at the source. Threshold: the same 5+ terms recurring across sessions means the fix belongs upstream — repairing "coobernetties" forever when the engine accepts a vocabulary hint is choosing toil.

## Vocabulary Biasing

- **Whisper**: `initial_prompt` conditions the decoder on your vocabulary — a natural sentence containing the problem terms ("Working on Kubernetes webhooks for the Krakatoa project with Sara Kowalski") outperforms a bare word list. Budget is 224 tokens (half the model's context window); spend it on the terms that actually recur, not the whole lexicon.
- **Cloud STT** (Google, Azure, AWS, Deepgram): phrase boosting / custom vocabulary with per-phrase weights. Start at the provider's moderate default; max boost makes the engine hallucinate the boosted term into unrelated audio — the over-biasing failure from SKILL.md Where Experts Disagree.
- **Source of terms**: the lexicon's right-hand column, filtered to `confirmed` entries seen within `lexicon_ttl_days`. Stale project vocabulary biased into a new project causes the exact substitutions this skill exists to fix.

## Language Pinning

- Pin the language explicitly for every user whose `languages` list has one entry; auto-detect adds a failure mode (mid-message flips) and buys nothing.
- Multilingual users: pin the primary language and let the repair layer handle embedded phrases (`multilingual.md`). Only genuinely balanced bilingual dictation justifies auto-detect, and it will still shred code-switched sentences.
- Transcripts arriving translated (user speaks Spanish, English comes out): the engine is in translate mode, not transcribe — a task/endpoint setting, the first thing to check when a multilingual user's meaning feels paraphrased.

## Model and Deployment Tradeoffs

| Choice | Wins | Costs | Pick when |
|---|---|---|---|
| Larger model | Accuracy on names, accents, noise | Latency, compute | Errors are lexical and persist after biasing |
| Smaller/turbo model | Latency | Rare-word accuracy | Conversational use where the repair layer catches the residue |
| Local | Privacy, offline, no per-minute cost | Hardware-bound speed and model size | Sensitive content, or transcripts must not leave the machine |
| Cloud | Best accuracy per effort, biasing APIs | Audio leaves the machine, per-use cost | Default when privacy allows |

Escape hatch reasoning: upgrade the model only after biasing failed — a vocabulary hint is free and usually removes the specific errors that motivated the upgrade.

## Audio-Side Fixes

Engine swaps cannot outrun bad input; check these before touching models:

- **Sample rate ≥16 kHz** — Whisper-family models operate on 16 kHz; upsampled 8 kHz telephony audio underperforms regardless of model size.
- **Mic distance and type** — a headset mic beats a laptop array across the room; the "3+ suspect tokens per message" regime (`degraded.md`) is usually this.
- **Push-to-talk vs voice activation** — VAD clips word edges at both ends (leading/trailing truncation, `degraded.md`); push-to-talk trades a button for clean boundaries.
- **Chunked/streaming capture** — words die at chunk boundaries; if errors cluster at regular intervals, lengthen chunks or add overlap.

## Verification Loop

After any tuning change, re-dictate a fixed test sentence packed with the user's known problem terms and compare against the last run. Without a fixed sentence you are judging noise; with one, a regression shows in a single read. Keep the sentence in `~/Clawic/data/listen/config.yaml` as a comment once established.

## When Tuning Is Not the Answer

- One-off errors: repair layer, by design.
- Errors on common vocabulary in every message: audio chain (`degraded.md` systematic section), not lexicon.
- Errors only on numbers: no vocabulary hint fixes -teen/-ty stress; that stays a repair-layer job forever (`numbers.md`).
