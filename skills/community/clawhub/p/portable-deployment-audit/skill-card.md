## Description:

Provides read-only file-inspection security audits for OpenClaw deployments, repositories, and local project directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otweihan](https://clawhub.ai/user/otweihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review deployments, server checkouts, workspaces, repositories, and CI targets for exposed credentials, risky configuration, port exposure hints, Docker or compose issues, Git exposure, and Unix permission concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Symlinks in untrusted repositories may cause the scanner to inspect files outside the selected target directory.

Mitigation: Run the skill only on directories you control, and review or remove unexpected symlinks before scanning untrusted repositories.

Risk: Audit findings are advisory and may require environment-specific judgment before changes are made.

Mitigation: Review findings and remediation recommendations manually before changing deployment or repository configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otweihan/skills/portable-deployment-audit)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON audit report with remediation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only file inspection; JSON mode writes a structured report to stdout.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
