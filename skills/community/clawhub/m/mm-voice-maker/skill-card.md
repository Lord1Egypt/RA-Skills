## Description:

Enables voice synthesis, voice cloning, voice design, and audio post-processing using MiniMax Voice API and FFmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blue-coconut](https://clawhub.ai/user/blue-coconut)

### License/Terms of Use:


## Use Case:

Developers and content producers use this skill to turn text or segmented scripts into speech, create or manage custom voices, and process generated audio with MiniMax Voice API and FFmpeg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys, private text, and voice recordings that may be sent to MiniMax.

Mitigation: Use only a MiniMax API key approved for this use, avoid sensitive text or recordings, and upload voice samples only when owned by the user or used with explicit permission.

Risk: A custom MINIMAX_API_BASE value could send requests and credentials to an untrusted host.

Mitigation: Keep MINIMAX_API_BASE on the trusted MiniMax endpoint unless the alternate endpoint has been reviewed and approved.

Risk: Voice deletion and cleanup helpers can remove custom voices or local temporary files.

Mitigation: Review the exact voice IDs and file paths before deletion, prefer dry-run or manual cleanup, and avoid broad cleanup commands until outputs are confirmed.

## Reference(s):

- [Getting Started](reference/getting-started.md)
- [Command Line Interface Guide](reference/cli-guide.md)
- [Text-to-Speech Guide](reference/tts-guide.md)
- [Voice Creation Guide](reference/voice-guide.md)
- [Audio Processing Guide](reference/audio-guide.md)
- [Text Processing Principle](reference/text-processing.md)
- [MiniMax Voice Catalog](reference/voice-catalog.md)
- [MiniMax Voice API Complete Reference](reference/api_documentation.md)
- [Troubleshooting](reference/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands; workflows may create segments.json and audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local audio outputs and temporary segment files when the generated commands are run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
