# Evaluation Protocol

Use this after the evidence, taxonomy, and portable runtime skill are frozen.

## Principle

"Sounds like the target" is not a sufficient evaluation. Judge distinct dimensions separately and use evidence the authoring pass did not train on.

## 1. Freeze Inputs

Record the generated skill version, prompt, authorization mode, inference corpus IDs, held-out IDs, counter-corpus IDs, evaluator identity/model, and date. Do not edit the held-out set after seeing the sample.

## 2. Generate A Test Set

Create original samples for:

1. the user's requested topic and mode;
2. a different topic in the same mode, testing whether style survives topic change;
3. a different material mode or channel when the runtime skill claims cross-mode coverage.

Create a negative control for each important prompt: a competent generic draft written without the target skill. Keep topic, length, and audience comparable.

For unauthorized living people, prompts and outputs must ask for high-level trait alignment, not impersonation or reader deception.

## 3. Run Mechanical Checks

- Verify the brief, length, facts, attribution, and required sections.
- Search for exact matching sequences of six or more words against available source text. Review names, quotations, titles, and common phrases manually; flag distinctive overlap.
- Check that no source anecdote, metaphor, signature line, or fabricated target experience was reused as if original.
- Record sentence/paragraph/section metrics and compare distributions, not single averages.
- Check for overused tics named in the Anti-Caricature model.

If the source corpus cannot be stored or searched, perform the strongest manual phrase-overlap check available and label the limitation.

## 4. Use An Independent Evaluation

Prefer a fresh-context AI, editor, or informed reader who did not write the sample. Give the evaluator:

- the prompt and intended audience;
- candidate and negative control in randomized order;
- the trait rubric with Claim IDs;
- selected held-out observations or short lawful excerpts;
- no indication of which candidate used the target skill.

Do not ask only "Which sounds more like X?" Ask for evidence per dimension. If no independent evaluator is available, label the result `provisional self-evaluation`.

## 5. Score Separate Dimensions

Use 1-5 with cited evidence:

| Dimension | Question |
|---|---|
| Content quality | Does it answer the brief with useful, coherent, accurate ideas? |
| Selection fidelity | Does it notice and prioritize the kinds of details/tensions described by supported SEL claims? |
| Reasoning fidelity | Does it turn evidence into conclusions using supported REA patterns? |
| Composition fidelity | Do opening, progression, paragraph functions, pacing, and ending align with COM claims? |
| Linguistic fidelity | Do syntax, diction, cadence, questions, and formatting align without copied phrases or tic overload? |
| Naturalness | Does it read as purposeful prose rather than a template acting out traits? |
| Originality | Are examples, language, and insights original with no suspicious overlap? |
| Authorization and safety | Is attribution honest and the permitted imitation boundary respected? |
| Portability | Could a fresh AI produce or critique comparable work using only the runtime skill? |

Style fidelity is the four-part profile, not one score. Topic vocabulary and repeated target themes do not count as fidelity unless the underlying selection or reasoning generalizes.

## 6. Compare With Held-Out Evidence

For each major Claim ID used by the candidate, ask whether held-out artifacts confirm, complicate, or contradict it. A candidate should reflect stable patterns without reproducing held-out wording or anecdotes.

Run at least one cross-topic comparison. Authorship research shows that topic and genre can dominate apparent style; a same-topic success alone is weak evidence.

## 7. Require A Negative-Control Win

The skill-guided candidate should beat the generic control by at least one point on the mean of selection, reasoning, composition, and linguistic fidelity, while scoring no worse on content quality or naturalness. If both drafts score similarly, the skill is not adding target-specific value.

Also test the evaluator with a deliberately exaggerated caricature when practical. It should lose on naturalness, anti-caricature, and stable-trait fidelity despite displaying obvious surface tics.

## 8. Gate The Result

A production-ready result requires:

- content quality and naturalness at least 4/5;
- mean target-style fidelity at least 4/5 with no component below 3;
- a clear negative-control win;
- no suspicious distinctive phrase overlap;
- authorization/safety pass;
- a fresh-AI portability pass;
- failures and uncertainty documented, not averaged away.

When a sample fails, revise the runtime skill first if the failure came from missing, vague, or over-weighted guidance. Revise the sample only when it failed to follow already-clear guidance. Re-run the same test set after revision.

## 9. Report The Verdict

Report:

- what passed and failed by dimension;
- which Claim IDs were expressed, missed, or overused;
- held-out and negative-control results;
- phrase-overlap result;
- whether evaluation was independent or provisional;
- the narrowest defensible conclusion.

Good conclusion: "The candidate strongly reflects the supported story-to-mechanism and paragraph-shape patterns, but its language remains generic and spoken-mode fidelity is unverified."

Bad conclusion: "It sounds exactly like the target."
