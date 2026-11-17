## Description:

Turns one clear portrait and a short singing audio excerpt into a singing clip, then reviews identity, facial movement, audio presence, and synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn a portrait and a short singing excerpt into a singing-photo clip for greetings, character art, playful posts, or song promotion. The agent reviews the result for identity, facial movement, audio presence, and synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner flags broad shared account access and permissions.

Mitigation: Review the Beatra device authorization scope and use it only in an agent environment you trust.

Risk: Portrait and voice media are sent to an external service for processing.

Mitigation: Confirm you have permission to use and upload the portrait and audio before submitting them.

Risk: The scanner flags recurring installation data reporting.

Mitigation: Review the installation-registration disclosure; it describes coarse package and runtime facts and says prompts, file paths, and tool details are not sent.

Risk: The scanner flags a possible uninstall issue that could disrupt other skills.

Mitigation: Use the bundled uninstall decision flow and retain shared connection state when other Beatra skills remain installed.

## Reference(s):

- [Singing-photo workflow](artifact/references/workflow.md)
- [Music editing and audio](artifact/references/music-editing-and-audio.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/photo-singing-video)
- [Beatra skill homepage](https://beatra.ai/skills/photo-singing-video)

## Skill Output:

**Output Type(s):** [Video, Guidance, Text]

**Output Format:** [Singing-photo video artifact with a concise result summary and review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One portrait and one singing audio excerpt per run; reports observed result quality without promising exact identity preservation or perfect synchronization.]

## Skill Version(s):

0.2.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
