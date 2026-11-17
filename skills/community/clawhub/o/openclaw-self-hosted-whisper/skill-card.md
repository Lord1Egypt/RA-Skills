## Description:

Transcribes audio files through a self-hosted Whisper ASR service running inside Kubernetes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavjer](https://clawhub.ai/user/xavjer)

### License/Terms of Use:

MIT

## Use Case:

Developers and platform operators use this skill to send audio files to an internal Kubernetes-hosted Whisper ASR API and save transcripts, subtitles, translations, JSON, or timestamped outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files may contain sensitive content and are uploaded over unauthenticated HTTP to the configured Whisper ASR service.

Mitigation: Use only in trusted internal environments, avoid sensitive recordings unless this risk is accepted, and add authentication and TLS before broader deployment.

Risk: The --prompt option can mishandle untrusted prompt text while building the URL-encoded request.

Mitigation: Do not pass untrusted text to --prompt until prompt encoding is fixed to avoid building executable Python source from user input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xavjer/skills/openclaw-self-hosted-whisper)
- [Whisper ASR webservice](https://github.com/ahmetoner/whisper-asr-webservice)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text, JSON, SRT, VTT, or TSV files, with Markdown guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and network access to the configured internal Whisper ASR HTTP endpoint.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
