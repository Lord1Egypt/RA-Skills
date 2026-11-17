## Description:

Review .osop/.osoplog for security risks, permission gaps, and destructive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archie0125](https://clawhub.ai/user/archie0125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review OSOP workflow and execution log files before running or trusting them. It highlights security risks, permission gaps, destructive commands, missing safeguards, cost exposure, and a safe-to-run verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The target OSOP workflow or log may contain secrets that the skill reads while looking for hardcoded credentials.

Mitigation: Use the skill only on OSOP files you intend to review, and avoid pointing it at unrelated private files.

Risk: Risk findings and safe-to-run verdicts are advisory and may miss context outside the reviewed file.

Mitigation: Review the findings before execution and confirm approval gates, permissions, timeouts, and destructive commands against the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archie0125/skills/osop-review)
- [OSOP homepage](https://osop.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk review with a score, severity table, summary, and verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes permissions, secrets, estimated cost, approval-gate status, and execution-log observations when available.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
