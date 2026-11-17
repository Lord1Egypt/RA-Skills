## Description:

将视频内容转写并加工为可复用文案，支持本地文件和公开视频链接，并可通过自定义 Prompt 生成总结、改写、分镜头、翻译等文本结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and agents use this skill to turn a single video or prior video task into reusable transcripts, summaries, meeting notes, marketing copy, translated text, or extracted highlights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, and API token are sent to the provider's cloud workflow, and the upload destinations and retention guarantees are under-disclosed.

Mitigation: Use the skill only for media that is acceptable to send to the provider, and ask the publisher to document upload destinations, retention guarantees, and handling of confidential or regulated content before sensitive use.

Risk: Token and failure messaging may include promotional content rather than neutral diagnostics.

Mitigation: Review installation and error behavior before deployment in managed environments, and require neutral error handling where user trust or support workflows matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-speech-to-text)
- [GuaiKei homepage](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text by default; user-requested Markdown or structured text when specified in the prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one video or prior task at a time and writes the generated text to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
