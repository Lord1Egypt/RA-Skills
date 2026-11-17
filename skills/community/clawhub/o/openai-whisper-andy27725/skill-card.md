## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use this skill to guide local audio transcription and translation through the Whisper command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Homebrew formula adds the Whisper CLI and its dependencies to the local environment.

Mitigation: Install only in environments where adding the Whisper CLI is acceptable.

Risk: Whisper caches models locally and generated transcripts may contain sensitive audio contents.

Mitigation: Transcribe only intended files and choose output directories that protect sensitive transcripts.

## Reference(s):

- [Whisper research page](https://openai.com/research/whisper)
- [ClawHub skill page](https://clawhub.ai/andy27725/skills/openai-whisper-andy27725)
- [Publisher profile](https://clawhub.ai/user/andy27725)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the local whisper binary is installed and that models may be cached locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
