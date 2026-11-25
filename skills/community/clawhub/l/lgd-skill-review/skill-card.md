## Description:

Reviews AI skill packages with separate structural and semantic scores, evidence-linked findings, prioritized fixes, rerun commands, and an evidence-based appeal workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers reviewing AI skill packages use it to assess release readiness, find evidence-linked issues, prioritize fixes, and rerun the review after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --run mode may execute tests from a reviewed package with the caller’s permissions.

Mitigation: Avoid --run on a regular machine; use an isolated, disposable environment when execution is needed.

Risk: The server security assessment rates the release suspicious with medium confidence and says some code was incompletely inspected; it also reports unsafe appeal-log handling, without establishing malicious intent.

Mitigation: Review the package before installing, and handle appeal logs in a controlled working copy with a backup.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/lgd-skill-review)
- [Scoring criteria](references/scoring.md)
- [Appeal rules](references/appeal.md)
- [Known limits and review corrections](references/faq.md)
- [Sample report](docs/sample-report.md)
- [Related skills](references/ecosystem.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands]

**Output Format:** [Plain-text or JSON review reports with scores, evidence-linked findings, prioritized fixes, and rerun commands; appeal rulings are logged as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings point to files and, when available, lines. Appeals require evidence and do not directly change scores.]

## Skill Version(s):

1.1.21 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
