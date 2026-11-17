## Description:

Triage, redact, clean up, and resolve OpenClaw GitHub Secret Scanning alerts in issues or PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw repository maintainers use this skill to handle secret scanning alerts by removing exposed credentials from supported issue, pull request, and comment locations, notifying affected users, and resolving alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because scanners report GitHub Discussion comment changes beyond its stated issue and pull request purpose, while the referenced script was unavailable for assessment.

Mitigation: Review the full skill scope and inspect the referenced script before installing; proceed only if you are comfortable with its scope and the remaining uncertainty.

## Reference(s):

- [OpenClaw Secret Scanning](https://github.com/openclaw/openclaw/security/secret-scanning)
- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/oc-secret-scanning-maintainer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted content and alert-resolution summaries.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
