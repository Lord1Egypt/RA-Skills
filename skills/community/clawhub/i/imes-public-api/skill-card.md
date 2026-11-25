## Description:

Integrates Istruzione Messina's public date-based angel-number endpoint. Use when a task needs to request or explain its digit-root result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucernel](https://clawhub.ai/user/lucernel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve and explain Istruzione Messina's date-based digit-root result for a valid date. It returns a calculation result and method details, not personalized life guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dates of birth are personal data.

Mitigation: For real dates, send JSON through standard input and avoid putting the date in a URL, shell history, logs, issues, or telemetry.

Risk: The security scan reports incomplete evidence because a referenced local CLI path could not be resolved.

Mitigation: Consider this limitation before installation and review the referenced CLI path.

## Reference(s):

- [Endpoint reference](references/imes.md)
- [Public endpoint](https://istruzionemessina.it/api/public/v1/angel-number.php)
- [Angel number source page](https://istruzionemessina.it/numeri-angelici-guida-completa/)
- [ClawHub release](https://clawhub.ai/lucernel/skills/imes-public-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON result with a concise text explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Integer result from 1 through 9 with version, method, and source]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
