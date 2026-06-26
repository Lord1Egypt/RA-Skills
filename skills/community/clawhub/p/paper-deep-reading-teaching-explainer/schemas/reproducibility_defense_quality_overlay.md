# Reproducibility / Defense / Teaching Quality Overlay

This overlay raises the quality bar for both the authoritative text report and staged cartoon storyboard outputs.

## Core rule

Do not produce generic summaries. The output must help the user:

1. reproduce the method or know exactly why reproduction is blocked;
2. defend the paper in front of a skeptical advisor/reviewer;
3. teach the paper to someone else without hiding formulas, data flow, or limitations.

## Required explanation pattern

For every key concept:

```text
Intuition -> Mathematical formula -> Concrete example -> Limitation
```

For every complex module:

```text
Input -> Output -> Symbols -> Dimensions -> Trainable parameters -> Fixed hyperparameters -> Data flow -> Failure modes
```

## Evidence-status labels

Every important factual or implementation claim should be labeled as:

- `paper-stated`: explicitly reported in the paper, appendix, figure, table, or source.
- `reasonable inference`: not stated verbatim, but directly inferable from the paper's equations, figures, or described procedure.
- `nearby-work inference`: inferred from closely related baselines, cited methods, or common implementation practice.
- `missing / not reported`: needed for reproduction or defense but absent from the available sources.

Do not collapse these categories.

## Experiment audit minimum

For each dataset / experiment / table / chart:

- dataset scale;
- label definition;
- train/validation/test split and sampling protocol;
- preprocessing;
- baseline taxonomy;
- baseline source;
- whether baselines were rerun, reimplemented, adapted, or copied from prior reports;
- metric meaning and failure mode;
- random seed if reported;
- hardware and runtime if reported;
- hyperparameters if reported;
- result exceptions and conditions where the main claim weakens;
- ablation meaning;
- qualitative example interpretation;
- reproduction risks.

If any item is missing, write `未报告` / `not reported` instead of inventing it; 不要编造.

## Numeric walkthrough

Include one small, complete numeric example that links:

```text
raw input -> constructed features / graph / sequence -> model/module computation -> loss or update -> inference score / decision
```

If the paper does not provide exact numbers, create a clearly labeled illustrative toy example. State that the numbers are for explanation only and are not reported experimental values.

## Storyboard translation

When converting the report into cartoon panels:

- preserve the same evidence-status labels where space permits;
- show missing experimental details as visible "not reported" checklist items;
- show module boxes with input/output and data-flow arrows, not only decorative icons;
- include a small numeric walkthrough panel for the most central mechanism;
- keep formulas short but accurate, with a verbal/visual intuition beside them.
