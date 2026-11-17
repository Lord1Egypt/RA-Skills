## Description:

Use the oo CLI to submit Doubao Speech transcription and text-to-speech tasks and retrieve their results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use an OOMOL-connected account to submit audio transcription or speech generation tasks and retrieve their status and results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI can persistently add skills to other agent tools, and the skill does not explain that behavior.

Mitigation: Review CLI installation and cross-agent skill changes; set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill syncing if unwanted.

Risk: Speech payloads pass through OOMOL to Doubao Speech.

Mitigation: Approve submissions with this data path in mind.

Risk: Remote installer contents and hosted connector behavior remain unverified.

Mitigation: Review the installer and connector behavior before use, and prefer a verified CLI release.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://raw.githubusercontent.com/oomol-lab/oo-cli/main/docs/commands.md)
- [Doubao Speech product page](https://www.volcengine.com/product/doubao-voice)
- [Doubao Speech API documentation](https://www.volcengine.com/docs/6561/overview)

## Skill Output:

**Output Type(s):** [JSON, Text, Audio]

**Output Format:** [JSON connector responses containing task status and speech task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected speech action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
