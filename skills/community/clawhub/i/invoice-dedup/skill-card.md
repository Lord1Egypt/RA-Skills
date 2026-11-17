## Description:

发票查重技能。录入发票进行查重、查询查重记录。适用于验证发票是否重复录入的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxt](https://clawhub.ai/user/zxt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to submit invoice details for duplicate-entry checks and to query existing duplicate-check records by date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends invoice details and an API key to an external invoice service.

Mitigation: Use the skill only when sending those invoice details to the stated service is approved, and use a scoped, revocable API key.

Risk: The security evidence reports unsafe API-key handling, including chat-based key collection and persistence in user shell configuration.

Mitigation: Do not paste real API keys into chat; prefer a proper secret manager or a temporary environment variable limited to the current run.

Risk: The security evidence reports an undeclared file-upload helper in the artifact.

Mitigation: Review or remove the upload helper before deployment and avoid granting file access unless the upload behavior is explicitly required and documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxt/skills/invoice-dedup)
- [ZXT Skill platform](https://skill.quandianfapiao.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown text with shell command examples and readable API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZXT_API_KEY or apiKey argument and sends invoice details to the configured external service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
