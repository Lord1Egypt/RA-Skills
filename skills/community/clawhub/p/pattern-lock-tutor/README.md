# Pattern Lock Tutor — Motor-Sequence Trainer

**New pattern locks, shortcut chains, and riffs — fluent in days, not weeks.**

A pattern lock, a keyboard shortcut chain, a piano riff, a keypad PIN: these
are **motor sequences** — the fingers learn them, not the eyes. People fail
to learn (or re-learn) them for three predictable reasons:

1. **Untrained transpositions** — you can enter the pattern from its native
   start, but a rotated start feels alien. Real-world retrieval never
   guarantees your training entry point.
2. **Interference** — changing an old pattern to a new one produces
   alternation errors: under speed, the old habit wins. Interleaved old/new
   drills are the only reliable fix.
3. **Speed before accuracy** — errors practiced at speed become permanent.

This trainer runs the standard motor-learning playbook:

- **Transposition drills** — every rotation of the sequence is a separate
  skill; all are measured from day one, weakest goes first
- **Interference drills** — old vs new under random alternation; reports the
  win-rate that predicts real-world blanking (≥80% = dominant)
- **Accuracy-gated speed** — no tempo work below 95% accuracy per block
- **Spaced recall schedule** — 10min → 1d → 3d → 7d → 16d → 35d expanding
  ladder; failures reset, `due` shows today's micro-sessions
- **Readiness verdict** — READY only when every transposition ≥95%, latency
  ≤1.2× baseline, and interference won

## Quick start

```bash
python3 scripts/pattern_tutor.py seq add phone-old 1,5,9,3
python3 scripts/pattern_tutor.py seq add phone-new 2,6,4,8,5
python3 scripts/pattern_tutor.py test phone-new --reps 8
python3 scripts/pattern_tutor.py train phone-new          # 60-90s, interactive
python3 scripts/pattern_tutor.py interfere phone-old phone-new
python3 scripts/pattern_tutor.py ready phone-new
```

Works over plain SSH or a phone terminal — micro-sessions everywhere. When
stdin isn't a TTY it runs in offline mode (simulated stats) so pipelines and
scheduling still work.

**Security: never store your real unlock pattern.** Train on a pattern of
the same shape; chunking transfers, specifics stay secret.

MIT © 2026 Denis Voronin
