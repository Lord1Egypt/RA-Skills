## Description:

上传长文档/文章/PDF/合同，自动生成结构化摘要、关键条款提取、执行清单。支持20+种摘要格式。安装即用，无需API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees can use this skill to summarize long documents, articles, PDFs, contracts, emails, meetings, and conversations into structured summaries, key points, action items, and comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local summary history, saved summaries, templates, preferences, and statistics may retain sensitive document content under ~/.openclaw/summarize-pro.

Mitigation: Use the skill only when local retention is acceptable for the material, and review or delete the stored files when handling sensitive content.

Risk: Summarization triggers and history logging can accidentally process or retain user-provided text when the user invokes summary-related commands.

Mitigation: Confirm intent before summarizing sensitive material and clear local history or saved summaries after use when retention is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-summarizer)
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and structured text summaries with optional local JSON settings, history, saved summaries, and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may maintain local summary history, saved summaries, templates, preferences, and usage statistics under ~/.openclaw/summarize-pro.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
