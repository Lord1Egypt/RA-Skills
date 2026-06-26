# Adapter: Empirical / Economics / Social Science

Use this adapter when the paper's contribution depends on data construction, measurement, causal identification, institutional detail, empirical modeling, or robustness analysis.

## What to prioritize

1. The estimand or target quantity.
2. Identification strategy or inferential logic.
3. Data source, sample construction, and measurement choices.
4. Institutional setting and why it matters.
5. Robustness checks, threats to validity, and interpretation.
6. External validity and policy or theoretical relevance.

## Questions to answer in the note

- What quantity is the paper trying to estimate or explain?
- Why does the design identify that quantity?
- Which assumptions are required for the causal or interpretive claim?
- What measurement or sample construction choices could change the result?
- What alternative explanations remain alive?
- Is the paper about causality, prediction, descriptive regularity, or mechanism?

## Minimum insertions into the note

Add or expand these sections:

### Problem setup

- estimand
- population or sample
- treatment / exposure / policy variable if relevant
- outcome variables
- identifying assumptions

### Evidence

- data construction and measurement
- baseline specification
- robustness checks
- falsification or placebo tests if any
- interpretation of coefficient magnitudes or effects

### Limitations and failure modes

Include at least one discussion of:

- omitted variable concerns
- measurement error
- sample selection
- parallel trends / exclusion / exchangeability / functional-form concerns where relevant
- external-validity limits

## Special reading rules

- Distinguish clearly between prediction, correlation, and causality.
- Do not treat a regression table as an argument by itself; reconstruct the identification logic.
- Record the institutional context when it is part of the design.
- Ask whether the paper's empirical design truly rules out the main competing stories.

## Typical failure patterns to watch for

- estimand left implicit
- identification assumptions not defended
- robustness checks narrow or cosmetic
- theory language stronger than what the empirical design can support
- effects statistically precise but substantively hard to interpret

## Reusable note prompts

- “The causal claim rests on …”
- “The paper is most convincing about … and least convincing about …”
- “The key threat to validity is …”
- “The result should be interpreted as … rather than …”
