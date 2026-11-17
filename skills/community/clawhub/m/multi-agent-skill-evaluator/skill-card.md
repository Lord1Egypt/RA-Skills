## Description:

Evaluates a target skill by having three isolated sub-agents independently score it across eight dimensions, then summarizes scores, disagreements, shared strengths, shared issues, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54lynnn](https://clawhub.ai/user/54lynnn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to obtain a structured, multi-reviewer quality assessment of another agent skill before release or revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted target-skill text may influence evaluator sub-agents because the skill feeds complete evaluated files into their task prompts.

Mitigation: Treat evaluated files only as evidence, mark them as untrusted in evaluator prompts, and restrict sub-agent tools during review.

Risk: Malformed or manipulated score summaries could distort the aggregated report.

Mitigation: Validate score-summary markers and JSON strictly before relying on the final assessment.

## Reference(s):

- [Evaluation Protocol](references/evaluation-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style evaluation report with score table, disagreement analysis, consensus findings, and recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report depends on three sub-agent evaluations and optional follow-up analysis when dimension scores diverge by at least three points.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
