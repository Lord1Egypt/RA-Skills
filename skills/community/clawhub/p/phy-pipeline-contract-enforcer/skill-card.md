## Description:

Data pipeline contract enforcer that defines expected schemas at pipeline stage boundaries and validates actual data samples against those contracts to catch schema drift before production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and data engineers use this skill to generate, validate, diff, and audit data pipeline contracts across dbt models, DataFrames, Kafka or REST payloads, and CSV or JSON files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented CSV helper may handle filenames unsafely, allowing a malicious filename to influence generated Python code.

Mitigation: Use the skill only with trusted local pipeline files, pass file paths as arguments rather than embedding them into Python source, and sandbox agent execution when processing untrusted filenames.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-pipeline-contract-enforcer)
- [Publisher profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline code blocks, YAML contract examples, shell commands, and concise CI/CD status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated contract drafts, validation findings, drift summaries, fix priorities, and dbt test snippets.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
