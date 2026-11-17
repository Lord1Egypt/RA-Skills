## Description:

AI-native behavior benchmark for evaluating whether an AI should act, how far it should go, and when it should stop across 144 Chinese-language scenarios and 8 scoring dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanyview1](https://clawhub.ai/user/wanyview1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and evaluators use this skill to run MayuBench prompts and rubrics for assessing AI behavior quality across uncertainty, safety, memory, agency boundaries, communication, human-AI relationship, and metacognition scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arena-style automatic evaluation may score conversations when the skill is enabled for that purpose.

Mitigation: Use automatic or arena-style evaluation only when the user intends conversations to be evaluated against MayuBench; otherwise use the manual Markdown test flow.

Risk: Benchmark results can be misleading if prompts are not run in independent sessions or if rubric scoring is applied inconsistently.

Mitigation: Run scenarios in isolated sessions and review MayuScore outputs against the included rubrics before comparing models.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanyview1/skills/mayubench)
- [Publisher profile](https://clawhub.ai/user/wanyview1)
- [Project homepage](https://github.com/kaidimi/mayubench)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown benchmark prompts, scoring rubrics, and evaluation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language benchmark content with optional manual, automated, or arena-style evaluation flows.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
