## Description:

Data Analyzer Pro helps an agent load CSV or JSON datasets, compute descriptive statistics, detect outliers, assess trends, calculate correlations, and persist analysis results as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users can use this skill to analyze structured CSV or JSON data for summaries, outliers, trends, and correlations. It is suitable for operational reports, A/B test review, data-quality checks, and metric monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report output paths can overwrite arbitrary writable local files when a filename is supplied.

Mitigation: Use only explicit trusted output paths, keep generated reports in a dedicated directory, and confirm before overwriting existing files.

Risk: Broad activation or manifest disclosures may invoke the skill in contexts where local file writes are not expected.

Mitigation: Avoid broad auto-invocation and review the intended dataset and output path before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-data-analyzer)

## Skill Output:

**Output Type(s):** [text, code, JSON, files]

**Output Format:** [Markdown guidance with Python code examples and optional JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be written to a user-supplied local output path.]

## Skill Version(s):

2.0.0 (source: server release, SKILL.md frontmatter, hub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
