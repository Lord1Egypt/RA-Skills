## Description:

将已完成的点播视频转写为文字与结构化文案，支持本地视频文件或公开视频链接，并可按自定义 Prompt 生成总结、金句、分镜头、翻译等内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to turn completed video or audio material into transcripts, summaries, meeting notes, social copy, translations, and other structured text outputs. Developers and agents use it as a command-line workflow that requires Node.js and a GUAIKEI_API_TOKEN.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, task IDs, and the API token are sent to GuaiKei's cloud workflow.

Mitigation: Use the skill only for recordings approved for third-party cloud processing, and avoid sensitive meeting, customer, legal, medical, or proprietary content unless approval is in place.

Risk: Public URL processing can download and upload content from broad video links.

Mitigation: Provide only trusted public video URLs or vetted local files, and review the source before running the command.

Risk: Temporary video files and the last task ID may remain in the local skill directory for up to 24 hours.

Mitigation: Clear the skill tmp directory after sensitive runs or avoid reusing shared workspaces for confidential media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-subtitle-transcript)
- [GuaiKei homepage](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or prompt-directed structured text emitted by the command-line workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer, network access, and GUAIKEI_API_TOKEN; accepts one video source or prior task ID per command.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
