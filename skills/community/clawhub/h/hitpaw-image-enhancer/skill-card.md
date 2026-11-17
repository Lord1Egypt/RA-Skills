## Description:

Enhance images and videos using HitPaw's AI enhancement API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitpawdev](https://clawhub.ai/user/hitpawdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to submit publicly reachable image or video URLs to HitPaw's enhancement API, poll asynchronous jobs, and download enhanced media outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media handling is under-scoped and requires sending media through HitPaw or publicly reachable URLs.

Mitigation: Use only photos or videos that are acceptable to share with HitPaw or expose through a public URL, and avoid confidential, regulated, or sensitive media.

Risk: The video command is broken in the artifact, with unresolved merge conflict markers in src/video-cli.js.

Mitigation: Do not rely on video enhancement until the publisher ships a fixed artifact and the command is rebuilt and tested.

Risk: Remote result downloads are not safely constrained.

Mitigation: Download outputs only to controlled paths, inspect generated media before reuse, and wait for publisher-side constraints on remote downloads.

Risk: The release needs dependency and provenance review before installation.

Mitigation: Review the package before deployment, update vulnerable dependencies, and treat GitHub links in the artifact as documentation links unless server-resolved provenance is added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hitpawdev/skills/hitpaw-image-enhancer)
- [HitPaw Image API Introduction](https://developer.hitpaw.com/image/Introduction)
- [HitPaw Image Models](https://developer.hitpaw.com/image/available-models)
- [HitPaw Video API Introduction](https://developer.hitpaw.com/video/Introduction)
- [HitPaw Video Models](https://developer.hitpaw.com/video/available-models)
- [HitPaw Image API Reference](https://developer.hitpaw.com/image/API-reference)
- [HitPaw Video API Reference](https://developer.hitpaw.com/video/API-reference)
- [HitPaw OSS Pre-sign Upload API](https://developer.hitpaw.com/common/oss-presign-put-api)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [CLI status text with downloaded image or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HITPAW_API_KEY and publicly reachable media URLs; writes enhanced media to user-selected output paths.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter and package.json list 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
