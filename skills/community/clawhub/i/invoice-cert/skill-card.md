## Description:

发票认证技能。税局扫码登录、登录企业查询、发票勾选认证、抵扣统计。适用于进项发票勾选、认证、统计等税务操作场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxt](https://clawhub.ai/user/zxt)

### License/Terms of Use:

MIT-0

## Use Case:

External tax and finance users use this skill to log in to the electronic tax bureau, inspect enterprise and invoice certification status, submit or cancel invoice certification, and manage deduction statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a tax API key and may persist it in shell settings.

Mitigation: Configure the API key outside chat when possible and confirm who can read any persistent shell-profile storage.

Risk: The skill can perform sensitive tax actions such as certification changes and deduction statistics operations.

Mitigation: Confirm the target enterprise, tax period, invoice list, and requested action before running state-changing commands.

Risk: The security verdict recommends review before installation because the provider receives enterprise tax data and API-key authority.

Mitigation: Install only when the provider is trusted with the relevant enterprise tax data and API access.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zxt/skills/invoice-cert)
- [中兴通简税 Skill platform](https://skill.quandianfapiao.com/)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Markdown, Configuration, Guidance]

**Output Format:** [Human-readable text and JSON-formatted command output, with QR-code image paths or links when login is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform state-changing tax actions after API-key configuration; successful business operations should identify the target enterprise.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
