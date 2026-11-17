## Description:

Helps agents find, generate, edit, and reuse media assets for HyperFrames projects, including audio, images, captions, and color treatments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heygen-com](https://clawhub.ai/user/heygen-com)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to source or generate media, prepare voiceovers and captions, adjust footage, and reuse assets across HyperFrames projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider credentials may be loaded from a project environment file and used for external media requests.

Mitigation: Review credentials and provider settings before use, particularly in untrusted repositories; use local-only workflows when external requests are inappropriate.

Risk: Generated or sourced media may be written locally and retained in a cross-project cache.

Mitigation: Review project outputs and the shared ~/.media cache before handling sensitive media or sharing a workspace.

Risk: Coarse opt-out usage telemetry may be sent.

Mitigation: Review telemetry settings and opt out if usage reporting is not permitted.

## Reference(s):

- [media-use release on ClawHub](https://clawhub.ai/heygen-com/skills/media-use)
- [Media resolution and reuse](references/resolve.md)
- [Audio workflows](references/audio.md)
- [Media operations](references/operations.md)
- [Provider setup](references/setup-providers.md)
- [HeyGen CLI documentation](https://developers.heygen.com/cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Plain text and Markdown with commands and local media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local media files, captions, and asset ledger records.]

## Skill Version(s):

1.0.86 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
