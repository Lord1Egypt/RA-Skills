## Description:

Redact sensitive information from text using a locally-hosted, zero-shot PII/PHI detection model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-newhauser](https://clawhub.ai/user/m-newhauser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to redact PII and PHI from outbound agent responses through a locally operated ClawGuard service before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete draft responses are sent to the configured redaction service before delivery.

Mitigation: Use only a localhost or tightly controlled internal service that you operate, and avoid enabling the skill for sessions containing secrets unless that deployment is trusted.

Risk: The security scan reports weak package provenance for the redaction dependency.

Mitigation: Verify the clawguard-pii package source and release integrity independently before installation, and run the service under a low-privilege account or container.

Risk: ML-based PII and PHI detection can miss sensitive data or redact benign content.

Mitigation: Validate performance on representative data and require human review for high-stakes deployments.

Risk: The include_original option can expose raw personal information in audit workflows.

Mitigation: Keep include_original disabled unless audit storage is access-controlled and approved for sensitive data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/m-newhauser/skills/pii-redactor)
- [clawguard-pii PyPI Package](https://pypi.org/project/clawguard-pii/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with redacted text, warnings, and inline shell or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append a warning when personal information is detected or automated scanning is unavailable.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
