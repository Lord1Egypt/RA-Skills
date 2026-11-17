## Description:

Local voice-reply pipeline that turns text into Opus/Ogg audio for Feishu or Discord using the Juno default voice or registered custom voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenured-master-chef-607](https://clawhub.ai/user/tenured-master-chef-607)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate local cloned or custom-voice audio replies from text and deliver them to Feishu or Discord. It is intended for trusted local voice workflows that can manage ffmpeg, Python TTS dependencies, voice samples, caches, and generated media files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local TTS API is unauthenticated and resource-heavy.

Mitigation: Keep the server bound to 127.0.0.1, do not expose it through a proxy or LAN interface, and add authentication, input limits, and pinned dependencies before production or shared-machine use.

Risk: Voice samples, text-derived audio, sidecar metadata, and phrase caches can persist on disk.

Mitigation: Avoid sensitive text or private voice samples unless local retention is acceptable, and manually manage or clear the voice, output, sidecar, and phrase-cache directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenured-master-chef-607/skills/local-voice-reply)
- [VOICE_SERVER_V3.md](artifact/server/VOICE_SERVER_V3.md)

## Skill Output:

**Output Type(s):** [Audio files, JSON metadata, Shell commands, Configuration guidance]

**Output Format:** [Opus audio in an Ogg container with optional JSON sidecar metadata and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is written to a local output directory; voice samples, registries, embeddings, phrase caches, and sidecar metadata may persist locally until manually cleaned.]

## Skill Version(s):

3.3.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
