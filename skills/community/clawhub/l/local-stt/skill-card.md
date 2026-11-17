## Description:

Local STT with selectable backends - Parakeet (best accuracy) or Whisper (fastest, multilingual).

This skill is ready for commercial/non-commercial use.

## Publisher:

[araa47](https://clawhub.ai/user/araa47)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to transcribe local audio files through selectable Parakeet or Whisper speech-to-text backends, with optional Matrix room delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Matrix mode can send generated transcripts to a configured homeserver.

Mitigation: Use --room-id only for audio that is appropriate to share, require an HTTPS MATRIX_HOMESERVER, and use a narrowly scoped Matrix access token.

Risk: The Matrix feature may read credentials from home .env files and write Matrix metadata to /tmp/stt_matrix.log.

Mitigation: Review local .env contents before use, protect Matrix credentials, and remove or restrict access to the temporary Matrix log when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/araa47/skills/local-stt)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text transcription on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Matrix message delivery when --room-id is configured; requires ffmpeg.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
