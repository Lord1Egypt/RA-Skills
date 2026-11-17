## Description:

Bug问题上报技能会在用户报告问题时提取问题描述，并将结构化 Bug 记录提交到企业微信智能表格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wearflatshoestowalktheworld](https://clawhub.ai/user/wearflatshoestowalktheworld)

### License/Terms of Use:

MIT-0

## Use Case:

Internal teams can report bugs in conversational Chinese and have the agent submit a structured record to a WeCom smart sheet with a default in-progress status and assigned handler.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-writes bug reports to a specific WeCom smart sheet using an exposed webhook secret.

Mitigation: Rotate the webhook key, move it to protected configuration, and install only when the target sheet is intentional.

Risk: The release includes avoidable install and script risks around dependency handling.

Mitigation: Remove unused dependencies or pin required packages before deployment.

Risk: User-provided issue descriptions may be embedded into requests without robust JSON handling.

Mitigation: Use a safe JSON encoder and safer temporary-file handling before production use.

Risk: Reports may contain credentials, personal data, or sensitive incident details.

Mitigation: Require explicit user confirmation before submission and avoid sensitive report content until stronger controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wearflatshoestowalktheworld/skills/global-bug)
- [ClawHub publisher profile](https://clawhub.ai/user/wearflatshoestowalktheworld)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Chinese status text for successful or failed bug-report submission]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits a single issue description and returns a concise confirmation or error response.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
