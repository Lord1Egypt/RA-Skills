## Description:

A passive anti-distillation monitoring and alerting skill that monitors request patterns, detects potential knowledge-distillation behavior, and alerts the operator without modifying responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to monitor read-only request-pattern metadata for potential knowledge-distillation behavior and receive alerts for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires read-only request-pattern metadata access and operator alert delivery.

Mitigation: Install only when that access is acceptable, and confirm the monitored metadata scope excludes request bodies, response bodies, identity fields, headers, cookies, and location data.

Risk: Webhook or email alerts can expose alert details or credentials if configured carelessly.

Mitigation: Keep webhook and email channels disabled unless intentionally configured, store credentials in platform secret storage, and restrict alert recipients.

Risk: Detection alerts may be false positives and could lead to unnecessary manual enforcement.

Mitigation: Review alert evidence before taking operator action; the skill is documented as passive and does not apply automated countermeasures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/omg)
- [Publisher profile](https://clawhub.ai/user/wscats)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON alert examples and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Passive monitoring posture; webhook and email alert channels require explicit environment configuration.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
