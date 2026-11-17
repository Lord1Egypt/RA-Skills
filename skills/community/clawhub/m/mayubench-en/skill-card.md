## Description:

AI-Native Behavior Benchmark - 48 scenarios x 3 difficulty levels = 144 questions, 8-dimension scoring, measuring whether AI should do things, not whether it can.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanyview1](https://clawhub.ai/user/wanyview1)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, evaluators, and AI safety teams use this skill to test AI behavioral decision quality across boundary, uncertainty, privacy, agency, relationship, and metacognition scenarios. It provides question prompts, scoring criteria, and a MayuScore framework for manual, automated, or arena-based benchmark runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark scores may be overinterpreted as operational readiness because the skill is a markdown-only behavior benchmark, not an action plugin or certification system.

Mitigation: Review the benchmark assumptions and use scores as one evaluation signal alongside domain-specific testing before operational decisions.

Risk: Memory, personal-data, and crisis-response examples may depend on platform behavior, locale, and policy context.

Mitigation: Adapt or review those scenarios for the target platform and jurisdiction before comparing models or publishing results.

## Reference(s):

- [MayuBench v1.0 question bank](MayuBench_v1.0.md)
- [Project homepage](https://github.com/kaidimi/mayubench)
- [ClawHub skill page](https://clawhub.ai/wanyview1/skills/mayubench-en)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown benchmark questions, scoring rubrics, and pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [144 scenario questions across 8 behavior dimensions with weighted MayuScore scoring.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
