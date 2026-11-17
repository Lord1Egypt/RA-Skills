## Description:

Deploys a three-agent video production pipeline that coordinates script writing, editing handoff, and multi-platform distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to configure coordinated Pilot Protocol agents for video script generation, editing coordination, asset handoff, publishing notifications, and performance tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned skill installation can pull changed dependencies into a production video pipeline.

Mitigation: Use trusted, pinned dependency versions before installation.

Risk: Free-form deployment prefixes and shell templates can lead to unsafe local configuration commands.

Mitigation: Validate the deployment prefix as a hostname-safe value and review generated commands before execution.

Risk: Peer handshakes and external publishing destinations may be accepted with insufficient verification.

Mitigation: Confirm peer identities before handshakes and explicitly approve YouTube, TikTok, social, webhook, and Slack destinations and credentials.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-video-production-pipeline-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through role selection, skill installation, hostname setup, manifest creation, and peer handshake steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
