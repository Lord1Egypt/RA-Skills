## Description:

Monitors public hot-topic sources, scores content ideas, drafts rough topic elements, writes selected records to Feishu, and prepares Telegram-style recommendation summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytearch1990-beep](https://clawhub.ai/user/bytearch1990-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and agent workflows use this skill to find AI, productivity, and creator-economy topics worth writing about, rank them, and prepare Feishu or Telegram handoff records for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Feishu credentials to write topic records to a Feishu table.

Mitigation: Keep Feishu credentials in environment variables, verify FEISHU_API is the official Feishu endpoint, and review a dry run before enabling writes.

Risk: Scheduled or daemon operation can repeatedly fetch public hot-topic data and prepare external notifications.

Mitigation: Start with manual runs, inspect generated recommendations, and enable daemon mode or notifications only after confirming the configured sources and recipients.

Risk: Automated topic scoring may surface incomplete, stale, or misleading public trend items.

Mitigation: Treat recommendations as candidates and require human review before creating or publishing content from them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytearch1990-beep/skills/inkroam-topic-expert)
- [Publisher profile](https://clawhub.ai/user/bytearch1990-beep)
- [TopHub.today](https://tophub.today/)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown-style recommendation summaries, JSON run summaries, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local topic records and can write selected topic records to a configured Feishu table.]

## Skill Version(s):

1.1.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
