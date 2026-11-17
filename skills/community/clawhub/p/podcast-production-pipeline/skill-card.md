## Description:

End-to-end podcast production automation for pre-recording research, outlines, show notes, SEO descriptions, social media promotion, and platform-specific publishing assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, podcast teams, and developers use this skill to automate repeatable podcast production tasks before and after recording. It generates research-backed outlines, interview questions, show notes, SEO descriptions, social posts, and highlight templates for international and Chinese platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the package ships real-looking secrets.

Mitigation: Remove bundled credentials, rotate any exposed keys, and supply API keys only through secure local configuration before use.

Risk: The release security summary says episode metadata can be sent to Discord without clear opt-in.

Mitigation: Make Discord posting explicit and opt-in, delete bundled gateway tokens, and confirm destination channel IDs before running workflows.

Risk: Podcast inputs may include confidential guest names, unreleased topics, or private transcripts.

Mitigation: Avoid sensitive podcast content until credentials are removed, outbound posting is opt-in, and all API keys come from the user's own secure configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/skills/podcast-production-pipeline)
- [Use Case Source](https://github.com/AlexAnys/awesome-openclaw-usecases-zh/blob/main/usecases/podcast-production-pipeline.md)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Xiaoyuzhou Podcaster Portal](https://podcaster.xiaoyuzhoufm.com/)
- [Ximalaya Creator Center](https://zhubo.ximalaya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; optional Whisper support; writes episode preparation and publishing assets under the configured storage path.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
