# Interview Answer Forge

**"Use STAR" is the most-given and least-executed interview advice in existence.** This turns it from a tip into a build system: mine your history into a story bank, predict the actual questions from the job description, forge answers with enforced word budgets, and pressure-test with the follow-up chains interviewers really run.

## The Problem

- People prep **answers** (fragile) instead of **stories** (transferable). Ten stories cover ~90% of behavioral questions; fifty memorized answers collapse on question fifty-one.
- The JD literally tells you what will be asked — "fast-paced" predicts a prioritization probe, "cross-functional" predicts an influence story — and almost nobody reads it that way.
- Answers fail in predictable, fixable ways: Situation eats the answer (interviewers score the **Action**), "we" instead of "I" (they hire the "I"), results with no number or timeframe, failure stories where nothing fails.
- Under adrenaline, unprepared people improvise — then can't survive layer-2 follow-ups ("How did you measure that?").

## What It Does

```
python3 scripts/interview_forge.py bank init      # story bank + mining prompts
python3 scripts/interview_forge.py predict jd.txt # JD -> predicted questions -> READY/GAP per probe
python3 scripts/interview_forge.py score story.json # STAR budget check + rule flags + follow-ups
python3 scripts/interview_forge.py mock --theme failure  # question + follow-up chain practice
```

- **Question prediction**: 17 JD signal patterns → the behavioral probes they imply, each mapped to your bank (READY) or flagged (GAP) with mining prompts to close it.
- **Enforced budgets**: Situation ≤15%, Task ≤10%, Action ≥50%, Result ~25% — the script measures your actual ratios and flags off-budget sections.
- **Rule engine**: I-voice in Action, number-or-band in Result, timeframe required, mandatory weak-spot flag on every story.
- **Follow-up chains**: 4 real interviewer probes per theme, so layer-2 ("Why not X instead?") never lands cold.

## Example

`predict` on a JD containing "fast-paced, cross-functional, detail-oriented" outputs:

```
[READY] Tell me about competing deadlines. How do you prioritize?
        (theme: ambiguity; JD signal: /fast[- ]paced/)
[GAP]   Tell me about influencing a team you don't manage.
        (theme: ambiguity; JD signal: /cross[- ]functional/)
GAPS (1): no bank story for:
  - [ambiguity] Tell me about influencing a team you don't manage.
Mining prompts to close them: ...
```

## Who Needs This

Anyone with an interview scheduled: career changers (the bank re-frames old experience for new roles), new grads (coursework/projects become stories), returning after a gap, internal promotions, and anyone who's walked out of an interview knowing they had the experience but fumbled the telling.

## License

MIT © Denis Voronin
