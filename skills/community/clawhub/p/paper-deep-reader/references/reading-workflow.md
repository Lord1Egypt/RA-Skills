# Reading Workflow

Use this workflow when reading a paper for a detailed note.

## 1. Build the paper map first

Before drafting prose, identify:

- research question
- problem setting
- assumptions
- main contribution(s)
- paper type: theory / method / empirical / systems / survey / mixed
- the minimum set of sections that carry the paper's intellectual load

Write a one-paragraph internal map:

> The paper studies __ under __ assumptions. Its main move is __. It claims gains in __, supported by __. The key technical objects are __.

If you cannot write this map, you do not understand the paper yet.

## 2. Read in layers

### Pass A: framing

Read title, abstract, introduction, conclusion, and figure/table captions.
Goal: understand what the authors want you to believe.

### Pass B: technical core

Read method / model / theory sections carefully.
Reconstruct notation and derive the main equations in your own words.
For proofs, do not copy everything; isolate the lemmas and proof ideas that actually carry the result.

### Pass C: evidence

Read experiments / empirics / case studies / benchmarks / robustness.
For each important claim, ask:

- what exact evidence supports it?
- compared to which baselines?
- under what setting?
- what is missing?

### Pass D: limits and connections

Read limitations, appendices if needed, and related work selectively.
Place the paper in context:

- what earlier idea does it extend, relax, or contradict?
- what cost did it pay to get the new result?
- where should a researcher be skeptical?

## 3. Extract the mathematical spine

The note should preserve the paper's core technical objects. Depending on the paper, extract some or all of:

- notation table
- objective function
- likelihood / loss / estimator
- optimization steps
- theorem statement and assumptions
- complexity or scaling law
- algorithm or pseudocode
- identification argument or causal design
- data generating process

Useful template:

```text
Inputs:
State / latent variables:
Objective:
Constraint / assumptions:
Update rule / estimator:
Claim:
Evidence:
```

## 4. Evaluate contribution, not just novelty language

A paper can be worth noting for different reasons:

- new theorem or proof technique
- new model / algorithmic mechanism
- unusually clean empirical identification
- decisive negative result
- strong synthesis or simplification
- practical systems gain with credible benchmarking

Do not confuse buzzwords with contribution. Ask:

1. What changed relative to the strongest nearby baseline?
2. Why is that change nontrivial?
3. What evidence shows the change matters?

## 5. Write the note as a teaching document

The reader of the note should be able to answer:

- what problem is being solved?
- why are existing approaches insufficient?
- what exactly is the new idea?
- how does the method or argument work step by step?
- what evidence should I trust?
- what are the limits, failure modes, and open questions?

The note is not an abstract rewrite. It is a guided reconstruction.

## 6. Adapt emphasis by paper type

### Theory

Prioritize assumptions, theorem statements, proof strategy, and what is genuinely new in the argument.

### Methods / ML / statistics

Prioritize objective, architecture or estimator, computational complexity, ablations, baselines, and implementation-sensitive details.

### Empirical / economics / social science

Prioritize identification strategy, data, measurement, threats to validity, robustness, and interpretation versus causality.

### Systems

Prioritize bottleneck, design tradeoff, workload, hardware or software setting, latency / throughput / memory metrics, and fairness of comparisons.

## 7. Final self-check before saving

Do not save the note until you can answer yes to all of these:

- Could someone reconstruct the main idea from my note alone?
- Did I include the key equations or assumptions?
- Did I distinguish claims from evidence?
- Did I identify at least one limitation or open question?
- Would this note still be useful six months later?
