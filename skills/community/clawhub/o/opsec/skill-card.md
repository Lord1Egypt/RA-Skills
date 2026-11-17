## Description:

Security review and risk auditing for OpenClaw skills and deployments. Inspect third-party skills, dangerous instructions, credential requests, privilege risks, and generate clear remediation reports before incidents happen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duclawbot](https://clawhub.ai/user/duclawbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use clawguard to inspect local OpenClaw skill directories before installation. It reports risky commands, external downloads, credential requests, privilege concerns, unsafe claims, evidence snippets, severity, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved reports may preserve snippets from scanned files, including sensitive text if broad private directories or credential-bearing files are reviewed.

Mitigation: Review only intended skill directories and avoid scanning files that contain real credentials unless local report retention is acceptable.

## Reference(s):

- [clawguard ClawHub page](https://clawhub.ai/duclawbot/skills/opsec)
- [clawguard homepage](https://clawhub.com/skills/opsec)
- [clawguard philosophy](references/philosophy.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Human-readable report, short summary text, or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include severity, matched location, evidence snippet, impact explanation, remediation guidance, and install verdict.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
