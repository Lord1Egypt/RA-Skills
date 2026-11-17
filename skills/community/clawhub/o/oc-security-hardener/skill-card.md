## Description:

Audit and harden OpenClaw configuration for security by scanning openclaw.json for vulnerabilities, exposed credentials, insecure gateway settings, overly permissive exec rules, and missing security best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to audit OpenClaw deployments, identify insecure configuration choices, detect exposed secrets, and apply or document hardening actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fix mode can copy sensitive OpenClaw configuration into a persistent backup without explicitly securing the backup file.

Mitigation: Run audit first, keep a protected backup, and avoid fix mode on configs containing plaintext secrets unless backup files are created with 0600 permissions or manually chmodded afterward.

Risk: The server security verdict is suspicious.

Mitigation: Review the script before using fix mode and prefer read-only audit or report commands until the backup-permission behavior is accepted or remediated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariusfit/skills/oc-security-hardener)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON audit output, Markdown reports, and OpenClaw JSON configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create configuration backups and Markdown report files when fix or report modes are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
