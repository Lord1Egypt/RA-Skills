## Description:

Evaluate one or more prompts with an evidence-based static benchmark covering general quality, structure and format, few-shot examples, safety and robustness, target-model compatibility, and cross-model portability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[margaretzybgl](https://clawhub.ai/user/margaretzybgl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and agent builders use this skill to audit prompts, compare prompt variants, diagnose production readiness issues, and identify model-compatibility risks before running dynamic model tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static prompt assessments may be mistaken for measured runtime performance.

Mitigation: Label model compatibility as a static prediction and keep runtime metrics marked as not measured unless separate dynamic tests are run.

Risk: Deterministic lint findings may be false positives or incomplete without semantic review.

Mitigation: Treat lint output as leads, confirm each material finding against prompt evidence, and report confidence for each finding.

## Reference(s):

- [Prompt Benchmark ClawHub Skill Page](https://clawhub.ai/margaretzybgl/skills/prompt-benchmark)
- [Model Compatibility Assessment](references/model-compatibility.md)
- [Report Schema](references/report-schema.md)
- [Static Prompt Benchmark Scoring Rubric](references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown report by default, with an optional JSON report when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static benchmark only; runtime metrics such as accuracy, latency, cost, hallucination rate, and consistency are not measured unless separate dynamic tests are run.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
