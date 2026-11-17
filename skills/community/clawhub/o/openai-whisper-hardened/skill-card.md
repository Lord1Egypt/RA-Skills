## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate local Whisper CLI commands for speech-to-text transcription and translation without requiring an API key. It emphasizes local handling of audio and transcripts with guardrails for sensitive content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcripts can contain private conversations, medical information, legal proceedings, or other sensitive speech content.

Mitigation: Keep transcription output local, avoid sending transcripts to external services, and review transcript contents before any sharing.

Risk: Audio from system paths or other users' home directories may belong to people who have not consented to transcription.

Mitigation: Confirm authorization, consent, and purpose before transcribing audio from sensitive paths such as /etc, /var/log, or another user's home directory.

Risk: Using the Python Whisper API broadens the execution surface beyond the skill's CLI-focused scope.

Mitigation: Prefer the whisper CLI directly, or invoke the CLI as a subprocess when automation is required.

Risk: Translation can change the user-visible meaning compared with same-language transcription.

Mitigation: Choose translation deliberately and confirm whether the task needs translated subtitles or same-language transcription.

## Reference(s):

- [OpenAI Whisper](https://openai.com/research/whisper)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/openai-whisper-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/openai-whisper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local whisper CLI; models may download locally on first use and transcripts should remain local unless reviewed and approved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
