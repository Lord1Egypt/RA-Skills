---
name: pattern-lock-tutor
description: "Use when you want to learn or change a repeated motor sequence — a new phone pattern-lock, a keyboard shortcut chain, a piano riff, a controller combo, a keypad PIN under fingers not eyes — with spaced repetition, interference drills (old habit vs new), and per-transposition error tracking. Models the forgetting curve, schedules micro-sessions (60-90 seconds), and knows the three real failure modes: unused transpositions, alternation interference from an old pattern, and speed before accuracy."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [muscle-memory, spaced-repetition, patterns, training, habits, motor-learning]
---

# Pattern Lock Tutor — Motor-Sequence Trainer

## Overview

A pattern lock, a keyboard shortcut chain, a piano riff, a game controller combo, a keypad PIN you must enter without looking — these are **motor sequences**: the fingers learn them, not the eyes. People fail to learn (or re-learn) them for three predictable reasons:

1. **Untrained transpositions** — you can enter the pattern starting from its first node, but a rotated start (the "same" pattern begun from a different point) feels alien, and real-world retrieval never guarantees the trained entry point.
2. **Interference** — changing an old pattern to a new one produces alternation errors: under speed, the old habit wins. The fix is interleaved old-vs-new drills until the new one is faster, not just correct.
3. **Speed before accuracy** — practicing fast embeds errors. Accuracy must reach threshold at a comfortable tempo *before* tempo increases.

This skill runs the standard motor-learning playbook as a command-line trainer:

- **Sequence definition** — a pattern as a node list (3×3 grid indices, keypad digits, piano keys, arbitrary tokens)
- **Spaced repetition** — recall sessions scheduled with an expanding interval (Ebbinghaus-style); a failed recall resets the interval
- **Transposition drills** — the same sequence practiced from every rotated starting point
- **Interference drills** — old sequence and new sequence interleaved; tracks which one wins under alternation
- **Session protocol** — 4–6 blocks of 8–12 reps, accuracy ≥95% required before speed work; per-block error log
- **Progress model** — per-transposition accuracy, mean recall latency, interference win-rate, readiness verdict

## When to Use

- Setting a **new phone/computer unlock pattern** and wanting it fluently yours within days, not weeks
- **Changing** a pattern (new phone, security rotation) — the interference drills are the whole game
- Learning a **shortcut chain** (IDE macros, editor combos) so it survives without looking
- Any short **motor sequence** you must execute blind: keypad entries, safe combinations, instrument riffs, controller combos
- Don't use for: declarative memory (facts → flashcard-forge), long procedural knowledge (algorithms → concept-cartographer), or security auditing of patterns (different domain).

## How It Works

1. **Define the sequence** — `seq add phone-old 1,5,9,3` (grid indices / digits / tokens).
2. **Baseline test** — `test phone-old --reps 8` measures accuracy and seconds-per-rep per transposition.
3. **Train** — `train phone-new --minutes 1.5` runs the block protocol: each block picks the weakest transposition, demands accuracy before speed, logs every error.
4. **Interference** — `interfere phone-old phone-new` alternates old/new prompts; scores which sequence dominates when you must switch — the number that predicts real-world failure.
5. **Schedule** — `due` lists sequences due for recall today with the current interval; successful recall expands the interval (1d → 3d → 7d → 16d → 35d), failure resets it.
6. **Readiness** — `ready phone-new` prints the verdict: every transposition ≥95% accuracy AND interference win-rate ≥80% AND latency ≤1.2× the first-session baseline.

## Commands

```bash
# Define sequences (nodes = grid indices, digits, or any tokens)
python3 scripts/pattern_tutor.py seq add phone-old 1,5,9,3
python3 scripts/pattern_tutor.py seq add phone-new 2,6,4,8,5

# Baseline + training
python3 scripts/pattern_tutor.py test phone-new --reps 8
python3 scripts/pattern_tutor.py train phone-new --minutes 1.5

# The retraining killer feature: old vs new under alternation
python3 scripts/pattern_tutor.py interfere phone-old phone-new --reps 20

# Spaced repetition schedule
python3 scripts/pattern_tutor.py due
python3 scripts/pattern_tutor.py recall phone-new --passed
python3 scripts/pattern_tutor.py ready phone-new

# Progress
python3 scripts/pattern_tutor.py stats phone-new
```

Storage: `pattern_tutor.json` in cwd. Terminal-based, no dependencies — the point is micro-sessions everywhere (SSH, phone terminal, break room).

## Session Protocol (what `train` enforces)

| Block | Content | Pass condition |
|---|---|---|
| 1–2 | Weakest transpositions, slow tempo | ≥90% accuracy |
| 3–4 | All transpositions mixed | ≥95% accuracy |
| 5–6 | Speed work (only after 95%) | latency under target |

A block that fails its pass condition repeats once; two failures end the session (motor learning consolidates in sleep — cramming past failure embeds errors).

## Common Pitfalls

1. **Only practicing from the native start.** Rotated-entry failure is the top real-world failure mode. `test` measures every transposition from day one.
2. **Dropping the old pattern cold.** When changing patterns, old habit interferes for 1–2 weeks. Run `interfere` until the new sequence wins ≥80% of alternations.
3. **Training tired or interrupted.** Motor consolidation happens during sleep; two clean micro-sessions a day beat one long grind. `due` keeps the cadence.
4. **Chasing speed early.** Errors practiced at speed become permanent. The block protocol refuses speed work below 95% accuracy.
5. **Sharing your real pattern.** Practice on a *training* pattern that you discard, or on tokens that resemble but don't match the real one. Never store the real unlock sequence in the JSON — `seq add` warns and asks for confirmation.

## Verification Checklist

- [ ] Training sequence defined (not the real unlock pattern)
- [ ] Baseline `test` recorded for every transposition
- [ ] `train` blocks passed with ≥95% accuracy before speed work
- [ ] `interfere` win-rate ≥80% for the new sequence (if replacing an old one)
- [ ] `due` shows expanding intervals (no resets in the last 3 sessions)
- [ ] `ready` prints READY across all three criteria
