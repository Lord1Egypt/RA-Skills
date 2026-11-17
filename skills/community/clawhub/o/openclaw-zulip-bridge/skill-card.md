## Description:

High-performance Zulip bridge skill that enables messaging, stream monitoring, and administrative actions on Zulip servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niyazmft](https://clawhub.ai/user/niyazmft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to let an agent interact with Zulip workspaces through the OpenClaw Zulip Bridge plugin, including sending messages, monitoring streams, managing streams, handling reactions, and performing gated administrative actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is deprecated and points users to an unpinned third-party code plugin that handles Zulip credentials.

Mitigation: Review the exact @niyazmft/openclaw-zulip plugin version before installing and prefer a pinned or verified release.

Risk: The Zulip integration can send outbound messages and may perform administrative workspace actions when enabled.

Mitigation: Use a dedicated least-privilege Zulip bot account, keep enableAdminActions disabled unless needed, and require explicit approval before stream, user, or sensitive outbound-message changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/niyazmft/skills/zulip-bridge)
- [Publisher Profile](https://clawhub.ai/user/niyazmft)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Zulip plugin and configured Zulip credentials; message responses may be chunked, converted to Markdown, and uploaded as media by the bridge.]

## Skill Version(s):

2026.7.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
