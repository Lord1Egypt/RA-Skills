# Motor-Sequence Learning — Reference

## Why motor sequences are different

Declarative memory (facts) and procedural memory (motor sequences) use
different neural machinery. A pattern lock is **procedural**: it consolidates
during sleep, is disrupted by conscious attention, and — critically — is
indexed by starting posture. This has three practical consequences:

1. **Rotated starts are separate memories.** If your pattern is A→B→C→D,
   starting at C and doing C→D→A→B is *not* the same skill. Real-world
   retrieval (phone already in hand, thumb already somewhere) doesn't respect
   your training entry point. Every transposition must be trained.

2. **Old habits interfere under load.** When a new pattern replaces an old
   one, both coexist; under speed or stress the older, more practiced one
   wins (proactive interference). Interleaved old/new practice — alternation
   drills — is the only reliable way to flip dominance. The metric that
   matters is the **interference win-rate**: given a random prompt ("old" or
   "new"), execute the right one. Below 80% you will still blank in front of
   the ATM.

3. **Errors practiced become errors permanent.** Motor learning encodes
   movement, not intent. Practicing at maximum speed with 80% accuracy
   encodes the 20% errors as confidently as the rest. Accuracy gate first,
   tempo second — the same protocol music teachers have used for centuries
   (slow practice, then ramp).

## The scheduling model

Expanding-interval spaced repetition, adapted for procedural memory (slower
decay than declarative, hence longer ladder):

```
level 0: 10 minutes   level 3: 7 days
level 1: 1 day        level 4: 16 days
level 2: 3 days       level 5: 35 days  (considered retained)
```

A successful `recall` promotes one level; a failed one resets to level 0.
`due` lists everything whose next-due date is today or past. Two
micro-sessions a day is the sweet spot — motor consolidation happens during
sleep, so more sessions the same day mostly add fatigue.

## Session science

- **Block structure**: 4–6 blocks × 8–12 reps, 60–90 seconds per session.
  Longer sessions measurably degrade accuracy in the tail (fatigue errors →
  learned errors).
- **Accuracy gate**: ≥95% per block before tempo increases. At 8 reps, one
  error = 87.5% → block fails, repeats once, then session ends.
- **Weakest-first ordering**: each block starts with the lowest-accuracy
  transposition — the one that will actually fail you.
- **Latency target**: fluent retrieval is ~1.2× your comfortable maximum
  speed, not your fastest-ever. The readiness threshold uses the *first
  session's* baseline so improvement is visible across days.

## Terminal as a motor training device

The terminal is a surprisingly good trainer for sequence fluency:

- Prompt shows the sequence to execute (e.g. `4-8-5-2` or rotated `5-2-4-8`)
- You type it as fast as you can; keystrokes are timed
- Correct/incorrect + latency per rep, aggregated per block

This trains **symbolic sequence recall** — the cognitive half of the skill.
The physical half (thumb arc on glass) transfers partially: research on
sequence learning shows the chunking and planning stages are shared, while
the effector-specific part needs a few real-world reps on the actual device.
Protocol: reach `ready` in the terminal trainer, then do 10–20 real reps on
the device to transfer.

## Applied to other domains

| Domain | Nodes | Old-habit interference example |
|---|---|---|
| Phone pattern lock | 3×3 grid indices | after a phone upgrade |
| Keypad PIN | digits 0–9 | after a card reissue |
| Keyboard shortcut chain | key names | after switching OS/editor |
| Piano riff | note names | after re-learning fingering |
| Controller combo | button names | after a control-scheme change |
| Safe combination | numbers | after a combo rotation |

## Security notes

- Never store your real unlock pattern/PIN in the trainer. Use a training
  pattern with the same *shape* (length, directional structure) — chunking
  transfers, specifics stay secret.
- The JSON store contains your training history — latency and error data
  could theoretically side-channel the pattern's difficulty. Store it
  locally; delete when done (`data` directory is disposable by design).
