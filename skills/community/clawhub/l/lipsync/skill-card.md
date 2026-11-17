## Description:

Lip-sync a face to a specific audio track on RunComfy via the runcomfy CLI, routing across ByteDance OmniHuman, Sync Labs sync v2 / Pro, Kling lipsync, and Creatify based on whether the user provides a portrait and audio, source video and audio, or a script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT

## Use Case:

Developers and external creators use this skill to select and invoke RunComfy lip-sync models for dubbing existing videos, creating talking-head videos from portraits, or generating synced speech from a script. It is intended for consent-based face and voice workflows where the operator has rights to the source media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing or running an unpinned third-party CLI.

Mitigation: Pin or review the @runcomfy/cli version before installing or executing it, especially in sensitive environments.

Risk: RunComfy tokens could provide broader access than needed if reused across environments.

Mitigation: Use a narrowly scoped RunComfy token and prefer environment-specific credentials.

Risk: Lip-sync workflows can misuse a person's face or voice without permission.

Mitigation: Process only faces and voices where the operator has consent and appropriate rights.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/lipsync)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync)
- [Sync Labs sync v2 Pro](https://www.runcomfy.com/models/sync/sync/lipsync/v2/pro?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync)
- [Sync Labs sync v2](https://www.runcomfy.com/models/sync/sync/lipsync/v2?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync)
- [Kling lipsync audio-to-video](https://www.runcomfy.com/models/kling/lipsync/audio-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync)
- [Kling lipsync text-to-video](https://www.runcomfy.com/models/kling/lipsync/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync)
- [Creatify lipsync](https://www.runcomfy.com/models/creatify/lipsync?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync)
- [RunComfy lip-sync feature catalog](https://www.runcomfy.com/models/feature/lip-sync?utm_source=clawhub&utm_medium=skill&utm_campaign=lipsync)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON CLI inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces model-route recommendations and runcomfy CLI invocations; generated media is produced by the external RunComfy service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
