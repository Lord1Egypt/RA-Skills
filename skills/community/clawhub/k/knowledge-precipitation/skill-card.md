## Description:

自动整理 Get笔记与对话记录，生成结构化日志简报，并同步归档到 Get笔记和飞书知识库与文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals who use Get笔记 and Feishu can turn daily notes and conversation history into a structured learning and work log, then archive it locally and in connected services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The archive workflow may delete historical documents and make remote changes, despite a read-only safety disclosure.

Mitigation: Before running it, review and accept the specific writes, overwrites, deletions, and access changes; confirm destinations and recipients, and preserve a recoverable copy of important documents.

Risk: The security scan has incomplete evidence: it covered 75% of components and static analysis was degraded.

Mitigation: Review the skill and its requested actions before installation, and do not treat the scan result as a complete assessment.

## Reference(s):

- [Briefing template](references/briefing-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Chinese-language structured daily briefings and archived notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes topic summaries, data overviews, action items, and archive status.]

## Skill Version(s):

0.1.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
