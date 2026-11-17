# Misconceptions — Repairing Wrong Mental Models

A wrong model is not a knowledge gap: teaching over it adds a second layer while the model keeps generating new errors. Repair before covering anything that depends on it.

## Detection

| Signal | Read |
|---|---|
| Same error class across different-surface problems | One generator, not several slips |
| Wrong answer delivered fast and confidently | A model, not a guess — guesses hedge |
| Correct answers, wrong reasoning when asked "why" | The model survives beneath right outputs; probe "why" on roughly one correct answer per session (`questions.md`) |
| Analogy properties imported past the mapping | The analogy has become the model — retire it explicitly (`formats.md`) |
| Technical term used with its everyday meaning | Natural-language collision ("significant", "heat", "force", "random") |

## Common Generators

- **Overgeneralized rule**: a rule learned without its conditions of use ("always normalize", "never mutate state") applied outside its domain. Fix: teach the boundary with one case inside it and one outside it.
- **Prior-domain interference**: the last domain's schema imported wholesale (spreadsheet habits in SQL, class-based habits in Rust ownership). Fix: a contrast table — how the old domain behaves vs how this one does.
- **Procedure without model**: steps memorized, no sense of what each does; breaks on any variation. Fix: re-teach the same procedure with a self-explanation prompt per step (`formats.md`).
- **Everyday-word collision**: refute the everyday meaning explicitly; defining only the technical sense leaves both meanings alive and competing.

## Repair Procedure

1. Surface it: have the learner predict a case where the misconception yields a wrong answer — do not announce the error first; the failed prediction is the lever (pretesting effect, Kornell).
2. Refute explicitly: state the misconception, show exactly where it fails, then present the correct model — refutation outperforms presenting the correct model alone (refutation-text effect, Guzzetti).
3. Rebuild from the kernel: most misconceptions are overextensions of something true; name what stays valid so the learner keeps it instead of defending the whole model.
4. Re-test 1-2 sessions later with a new surface: corrected models resurface under load (continued influence effect, Lewandowsky). Log the re-test like any queued miss (`memory-template.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Correcting outputs, not the generator | The model keeps producing new wrong answers on new surfaces | Run the repair procedure, then answer the original question |
| Announcing "common misconception:" before the learner commits | Without a committed prediction there is nothing to refute; the correction reads as trivia | Prediction first, correction second |
| Drilling harder on repeated errors | Practice automates whatever model is running — including the wrong one | Stop drilling, repair, then resume practice |
| Declaring the repair done after one clean answer | Continued influence: the old model returns under speed or stress | Keep the misconception in the review rotation until it passes the 3-session retirement bar (`retention.md`) |
