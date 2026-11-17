## Description:

Pull daily Gumroad product/sales analytics safely (no raw PII persistence by default).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladchatware](https://clawhub.ai/user/vladchatware)

### License/Terms of Use:


## Use Case:

Developers, creators, and operators use this skill to collect daily Gumroad sales and product metrics into summary JSON for lightweight revenue tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gumroad access tokens and API payloads may be exposed locally during execution.

Mitigation: Use a restricted credentials file, avoid raw export mode unless needed, and run the skill only in a trusted workspace.

Risk: Output files may contain business or customer-related Gumroad data.

Mitigation: Apply restrictive permissions to metrics directories and review raw exports before sharing or syncing them.

Risk: Raw diagnostic exports can retain sensitive fields outside the sales redaction path.

Mitigation: Prefer summary-only storage and use an allowlist for any raw export that is kept.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vladchatware/skills/gumroad-analytics)
- [ClawHub homepage metadata](https://clawhub.ai/vladchatware/gumroad-analytics)
- [Gumroad API endpoint](https://api.gumroad.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a daily summary JSON by default; raw sales and product exports are explicit opt-in.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
