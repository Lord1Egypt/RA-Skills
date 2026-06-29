# Reviewer Output Template

```text
Verdict: PASS or REVISE
Score: 0-120

Pass rationale:
{{WHY_THIS_DOES_OR_DOES_NOT_PASS}}

Evidence checked:
{{LIST_WHAT_YOU_EXAMINED_EVEN_IF_BRIEF}}

Must-fix issues:
- {{ISSUE_OR_NONE}}

Optional improvements:
- {{OPTIONAL_OR_NONE}}

120-level approval statement:
{{N/A_UNLESS_VERDICT_PASS_AND_SCORE_120}}
```

Rules:

- `PASS` requires `Score: 120`.
- `PASS` requires `Must-fix issues: - none`.
- All reviews require a non-empty `Evidence checked` field — list what you examined, even briefly.
- Any score below 120 is `REVISE`.
- Do not write a 120-level approval statement unless the verdict is `PASS` and the score is 120.

Score scale:

- **120**: reviewer has zero remaining reservations about this facet — not "meets requirements", but "I have nothing left to object to". This is an intentional signal value: 0–119 always means REVISE, regardless of reason.
- **91–119**: nearly ready; specific items must be resolved before passing.
- **61–90**: substantial issues present; meaningful progress but significant gaps remain.
- **0–60**: fundamental gaps in this facet; the artifact does not yet address core requirements.
