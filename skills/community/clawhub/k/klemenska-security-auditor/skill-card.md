## Description:

Scan and audit installed skills for security risks, suspicious patterns, and permission overreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klemenska](https://clawhub.ai/user/klemenska)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage installed or candidate skills for permission overreach, suspicious patterns, risky code behavior, and security review findings before installation or continued use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit results may miss malicious instructions or payloads and may incorrectly report low risk.

Mitigation: Treat results as triage, run the skill in a constrained workspace, and verify important findings with an independent review process.

Risk: The skill examines local skill files and permissions, so its output can affect install or trust decisions.

Mitigation: Review the generated findings before acting on them and do not use the report as the sole approval signal for sensitive environments.

## Reference(s):

- [Permissions Reference Guide](references/permissions.md)
- [Security Audit Rules](references/rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text audit summaries and optional Markdown reports with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include risk levels, flagged patterns, detected permissions, warnings, and review recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
