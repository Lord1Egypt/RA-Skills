## Description:

Scans OpenClaw configuration, workspace permissions, operation rules, logs, and potential secret exposure, then reports findings, scores risk, and can propose or apply fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ithacajason](https://clawhub.ai/user/ithacajason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to audit local OpenClaw configuration and workspace state for unsafe permissions, missing delete-operation rules, exposed secrets, and log anomalies before deciding whether to apply suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner output can expose sensitive values or paths, especially when JSON output is used with real secrets.

Mitigation: Run scan-only first, avoid JSON output with real secrets until redaction is verified, and review reports before sharing them.

Risk: Repair modes can make unattended changes to .gitignore, operation-rule files, and workspace permissions.

Mitigation: Prefer scan-only or interactive repair, review each proposed change, and use --fix-all only when workspace edits are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text report or JSON, with suggested commands and optional fix results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repair modes can modify workspace files and directory permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
