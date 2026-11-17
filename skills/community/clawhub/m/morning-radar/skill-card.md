## Description:

Morning Radar searches Baidu Qianfan AI Search for configured news topics, formats a prioritized Markdown digest, and sends it to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diomedeak](https://clawhub.ai/user/diomedeak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect recurring topic-based news, generate a concise morning digest, and deliver it to a Feishu recipient or scheduled workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured search topics are sent to Baidu Qianfan.

Mitigation: Use non-sensitive topics and review query configuration before running the skill.

Risk: Generated digests are sent through Feishu to the configured receiver.

Mitigation: Confirm the receiver Open ID and use least-privilege Feishu app permissions.

Risk: Baidu API keys and Feishu app secrets are required for operation.

Mitigation: Store credentials in environment variables or a protected local config file, and do not commit local secrets.

Risk: Automatic cron scheduling can send recurring messages without manual review.

Mitigation: Review the cron schedule and output destination before enabling daily automation.

## Reference(s):

- [ClawHub morning-radar release page](https://clawhub.ai/diomedeak/skills/morning-radar)
- [Baidu Qianfan Platform](https://qianfan.baidubce.com)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown/plain text digest with links, dates, summaries, and priority labels; setup guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Baidu Qianfan and Feishu credentials; supports optional query, keyword, item-count, source-name, and title settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
