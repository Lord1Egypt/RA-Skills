## Description:

Podcast Generator turns a user topic into a short podcast by retrieving recent web information, drafting a conversational script, selecting a suitable iFlytek TTS voice, synthesizing an MP3 under three minutes, and sending the audio file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn a requested topic or news angle into a short spoken podcast episode, primarily in Chinese, with recent web context and automatic TTS voice selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or web-influenced script text could be handled through a heredoc shell pattern in a way that turns content into local shell commands.

Mitigation: Write generated script content as data through a file API or stdin, review the skill before installation, and validate the TTS script path before execution.

Risk: Podcast requests may include sensitive topics or proprietary content that should not be sent through external retrieval or TTS workflows.

Mitigation: Avoid sensitive or proprietary prompts for this skill and review its behavior before use in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/podcast-gen)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Conversational podcast script, local synthesis command pattern, and MP3 audio file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets podcast audio of about two to three minutes and requires configured iFlytek TTS credentials through the dependent xfyun-tts skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
