## Description:

把「含嗯啊口误的原始转写稿」变成「干净可发的文案」。当用户要求视频转文字、提取文案、视频总结、字幕提取、会议纪要、课程拆解、直播复盘、采访整理时使用。基于大模型语义理解转写，输出即用；支持本地视频与抖音、小红书链接，Prompt 可定制任意风格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, educators, and agents use this skill to convert one local or public online video into a transcript, summary, meeting notes, subtitles, or platform-specific copy through Guaikei's cloud service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos, video URLs, prompts, and task identifiers may be sent to Guaikei's cloud service for processing.

Mitigation: Use the skill only with media your organization permits you to upload to that service, and avoid internal-only URLs, private recordings, regulated data, or sensitive meetings unless approved.

Risk: GUAIKEI_API_TOKEN authorizes requests to the service.

Mitigation: Store the token in the environment, keep it private, and rotate it if it may have been exposed.

Risk: Generated transcripts or summaries can be inaccurate for noisy audio, overlapping speech, strong accents, background music, or specialized domains.

Mitigation: Review outputs before publication or decision-making, especially for medical, legal, financial, or other high-impact content.

## Reference(s):

- [Guaikei homepage](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-to-script)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or user-requested structured text/markdown; command examples use shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN, processes one video per command, and uses --prompt to control the requested output style.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
