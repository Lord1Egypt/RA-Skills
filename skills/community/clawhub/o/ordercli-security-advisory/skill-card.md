## Description:

Security advisory for OrderCLI with 2 high/critical issues found on 2026-05-07T09:15:31Z.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill as a static advisory summarizing OrderCLI audit findings and recommended remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remediation guidance references a local OrderCLI path and audit script that may not match the reader's environment.

Mitigation: Verify that the referenced path and run-audit.sh script are expected before following the advisory steps.

Risk: The advisory discusses high-severity findings involving JSON validation and PII handling.

Mitigation: Review the affected OrderCLI implementation before production use and restrict access to files that contain PII.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/ordercli-security-advisory)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown advisory with findings, remediation guidance, and an inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static advisory content; no executable code or hidden behavior was reported by the security evidence.]

## Skill Version(s):

0.1.202605071715 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
