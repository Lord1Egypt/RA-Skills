# Checks and Feedback — Designing Retrieval That Measures

A check exists to produce evidence, not reassurance. Every teaching exchange ends with one (SKILL.md Rule 3); this file is how to build them.

## Question Types by Signal Strength

| Type | Signal | Use |
|---|---|---|
| Free recall ("explain X from scratch") | Strongest, also hardest | Session close, mature concepts |
| Application to a novel case | Strongest for transfer | Before raising a tier; the case must be unseen |
| Prediction ("what happens if...") | Strong, fast, low ceremony | Before revealing an example or running code |
| Cued recall ("what does X do when Y?") | Strong | Default in-session check |
| Recognition (multiple choice, true/false) | Weak — recognition succeeds where recall fails | Only when the options themselves teach (contrast cases), or to vary pace |
| "Do you understand?" | Zero — produces politeness, not evidence | Never |

## Calibrating Difficulty

- Target the 70-90% band (SKILL.md Rule 4). Estimate before asking: if you cannot imagine this learner missing it, it is a warmth gesture, not a measurement.
- Raise difficulty by increasing transfer distance — same concept, farther surface — never by obscurity or trick phrasing. A trick question measures suspicion, not knowledge.
- Change one dimension at a time: a question that is both novel-surface and multi-concept is undiagnosable when missed.

## Feedback on Errors

- High-confidence wrong answer: correct immediately and explain why the wrong answer was plausible — corrected high-confidence errors are the most durably fixed (hypercorrection, Butterfield and Metcalfe).
- Low-confidence wrong answer: prompt once ("walk me through your reasoning") before giving the answer — a self-generated correction outlasts a delivered one.
- Right answer, suspicious reasoning: ask "why" on roughly one correct answer per session; a wrong model under right outputs is a `misconceptions.md` case.
- Minor slips (naming, arithmetic): batch at session close; interrupting flow costs more than the slip (feedback-timing boundary: SKILL.md Where Experts Disagree).
- Never soften a correction into ambiguity: the learner must leave knowing which answer was right and why theirs was attractive.

## The Session-Close Set

- 2-3 questions spanning the whole session (SKILL.md Session Structure), oldest concept first — the oldest has had the most forgetting, so it carries the most signal.
- At least one application-type question; a close made only of definition recall certifies vocabulary, not understanding.
- Every miss goes to the topic log (`memory-template.md`) as the next session's opener.

## Anti-Gaming

- Vary surface form between sessions: a learner who has seen "name the three causes of X" twice retrieves your question, not the concept.
- Never re-use the exact case that was taught — that tests memory of the example, not the concept.
- If answers arrive instantly and phrased like your own explanation, the learner is echoing; ask for the same idea applied, not restated.

## Respecting check_style

`check_style` in config shapes the surface (open questions, scenarios, mixed) — it never removes the generation requirement. A learner who dislikes quizzes still generates: predictions, "how would you approach", explain-it-to-a-colleague framings all qualify (`stuck.md` Learner Pushes Back).
