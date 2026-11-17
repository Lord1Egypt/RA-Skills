## Description:

美团外卖 helps an agent authenticate a Meituan account, request Meituan coupon benefits, and query prior coupon redemption records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to claim Meituan food delivery coupon benefits and check past coupon redemption records after authenticating their Meituan account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Meituan account tokens may be exposed through logs, command arguments, URLs, or local files.

Mitigation: Use only on trusted personal machines, avoid shared or retained-log environments, and clear login and device data when finished.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/meituan-openplatform/skills/meituan-waimai)
- [Publisher Profile](https://clawhub.ai/user/meituan-openplatform)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid Meituan login token; local authentication and coupon history files may be created during use.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
