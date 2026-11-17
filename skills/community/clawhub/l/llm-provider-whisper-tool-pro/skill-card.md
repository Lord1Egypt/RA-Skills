## Description:

Whisper语音转文字专业版 helps agents guide enterprise Whisper transcription workflows, including batch transcription, GPU acceleration, speaker diarization, custom vocabulary prompts, and API service deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to set up and run local or API-based Whisper transcription workflows for meeting notes, video subtitles, and speaker-labeled transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt agents to read and write files or run setup commands for transcription workflows.

Mitigation: Review dependency installs and generated commands before execution, and narrow activation to explicit transcription, subtitle, or diarization tasks.

Risk: API deployment examples could expose confidential recordings or transcripts if deployed without controls.

Mitigation: Use authentication, retention controls, and clear storage locations for transcripts, logs, caches, and temporary files before processing sensitive recordings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/llm-provider-whisper-tool-pro)
- [PyTorch CUDA wheel index](https://download.pytorch.org/whl/cu121)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dependency installation commands, API service examples, batch transcription configuration, and security guidance for local audio/video processing.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
