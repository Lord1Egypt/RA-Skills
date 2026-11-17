## Description:

What does this video say? Gets the transcript of each video by its link, as one table: link, language and full text. One paid call per video. Use when the user asks this about TikTok, YouTube, Instagram, Reddit. 这条视频讲了什么？按链接取每条视频的字幕，排成一张表：链接、语言和全文。每条视频一次计费调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to retrieve transcripts from TikTok, YouTube, Instagram, and Reddit videos, review them in a table, and ask questions about their contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript retrieval uses a paid external API, and the security scan was partial with medium confidence.

Mitigation: Review the okdata service and state the per-call maximum cost before requesting transcripts; follow the skill's approval steps for runs over 10 calls and keep the API key in environment or client configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conn-ho/skills/okdata-transcripts)
- [okdata transcript skill documentation (English)](https://okdata.online/skills/transcripts/?src=skill-okdata-transcripts)
- [okdata transcript skill documentation (中文)](https://okdata.online/zh/skills/transcripts/?src=skill-okdata-transcripts)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown table followed by a concise answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One row per video with Link, Language, and Text columns; missing values stay blank, and the response reports billed cost and data source.]

## Skill Version(s):

0.2.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
