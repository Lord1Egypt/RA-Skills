## Description:

视频转文字 + 文案产出二合一。用户丢来一个视频（链接或本地文件）要求转写、总结、提取文案、改写二创时使用。基于云端大模型完成语音转写与语义理解，自动过滤口误与冗余，按需输出完整文字稿或指定风格的成品文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operations teams, and developers use this skill to turn online or local video into transcripts, summaries, meeting notes, translations, and platform-specific copy through a Node.js command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local media files or downloaded URL content to a cloud service, along with prompts, task IDs, API tokens, and possibly local path names.

Mitigation: Use a sandbox with filesystem access limited to intended media files and avoid processing sensitive paths, credentials, private keys, localhost URLs, internal URLs, or untrusted redirected URLs.

Risk: The release security summary says the skill overstates its network and privacy limits.

Mitigation: Review provider handling claims before production use and restrict outbound network access to the required service endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-wenzi-fetcher)
- [Guaikei service site](https://www.guaikei.com)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown emitted to stdout, with progress and errors emitted to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command accepts a video URL, local file path, prior task ID, and optional prompt; outputs depend on the remote service response.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
