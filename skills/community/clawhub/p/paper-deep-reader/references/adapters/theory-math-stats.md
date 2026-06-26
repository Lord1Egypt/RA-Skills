# Adapter: Theory / Mathematics / Statistics

Use this adapter when the paper's main contribution is a theorem, proof technique, estimator property, approximation guarantee, asymptotic result, or mathematically central formalism.

## What to prioritize

1. Exact problem setup and definitions.
2. The main theorem statements, not just their informal gloss.
3. Assumptions and which ones do real conceptual work.
4. Proof strategy: what unlocks the result.
5. Rates, complexity, consistency, efficiency, concentration, approximation, or identifiability guarantees when relevant.
6. Special cases, limiting cases, and reductions to known results.

## Questions to answer in the note

- What object is being studied exactly?
- What is the main claim in formal terms?
- Under what assumptions does the claim hold?
- Which assumptions are structural and which are technical?
- What is genuinely new: the statement, the proof idea, the rate, or the scope?
- What nearby result does this recover or extend?

## Minimum insertions into the note

Add or expand these sections:

### Technical core

- definitions and notation
- theorem statement(s)
- proof sketch or proof architecture
- role of each major assumption
- interpretation of rates or bounds

### Limitations and failure modes

Include at least one discussion of:

- dependence on strong assumptions
- asymptotic versus finite-sample gap
- nonconstructive steps or existence-only results
- unclear practical relevance if the paper is highly abstract

## Special reading rules

- Do not paraphrase away the theorem. Preserve the formal claim if it matters.
- Do not copy proofs line by line. Extract the key lemmas, reductions, or invariants.
- Check whether the result is stronger, cleaner, or merely differently framed than prior work.
- Ask whether the paper proves something deep, something useful, or both.

## Typical failure patterns to watch for

- theorem stated under unrealistic or hidden regularity conditions
- asymptotic claim oversold as practical superiority
- proof novelty overstated when the machinery is standard
- notation so compressed that the real object being bounded becomes unclear

## Reusable note prompts

- “The core mathematical move is …”
- “The theorem is strong because … but narrow because …”
- “The proof works by reducing … to …”
- “The assumption doing the heavy lifting is …”
