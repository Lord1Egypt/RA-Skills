## Description:

Automated link processing pipeline that detects Douyin, Xiaohongshu, Bilibili, WeChat, and web article links, downloads media or extracts text, transcribes video audio, identifies topics, and routes content to a knowledge base inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xings117](https://clawhub.ai/user/xings117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to process shared video and article links into transcripts, extracted Markdown text, topic routing decisions, and knowledge base inbox entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary links, including private or internal URLs.

Mitigation: Require explicit confirmation before processing links, validate destinations, and avoid private or internal URLs.

Risk: Downloaded or processed files may be written or uploaded outside an intended storage boundary.

Mitigation: Run in a constrained environment and confine saved or uploaded files to an approved storage root.

Risk: The video pipeline disables certificate verification for downloads.

Mitigation: Remove --no-check-certificate before use and review download destinations before execution.

Risk: COS upload and DeepSeek processing may send sensitive content to external services.

Mitigation: Do not enable COS or DeepSeek processing for sensitive content unless that data flow is approved.

## Reference(s):

- [Links Pipeline package page](https://clawhub.ai/packages/links-pipeline)
- [Links Pipeline skill page](https://clawhub.ai/xings117/skills/links-pipeline)
- [DeepSeek API endpoint](https://api.deepseek.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown and JSON status output with transcripts, extracted article content, routing decisions, and saved file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save downloaded media, transcripts, and processed text under /tmp/links-pipeline and may upload processed content when COS storage is configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
