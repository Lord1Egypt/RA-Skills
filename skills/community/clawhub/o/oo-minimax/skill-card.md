## Description:

Use MiniMax through a connected OOMOL account to inspect models and video tasks and create text, audio, and video outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill through a connected OOMOL account to access MiniMax models and manage text, audio, and video generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unchecked remote code.

Mitigation: Install a verified oo CLI release yourself before using the skill.

Risk: The setup helper documents additional agent-skill installation.

Mitigation: Consider disabling managed-skill synchronization using the publisher's command-reference guidance.

Risk: Requests and media pass through OOMOL, and generation may incur charges.

Mitigation: Review the content sent through OOMOL and expected billing before creating media.

Risk: Write actions change MiniMax state, and video deletion is destructive.

Mitigation: Review the exact payload and effect before write actions, and confirm the deletion target.

## Reference(s):

- [MiniMax API documentation](https://platform.minimax.io/docs/api-reference/api-overview)
- [MiniMax](https://www.minimax.io)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [MiniMax skill release](https://clawhub.ai/oomol/skills/oo-minimax)

## Skill Output:

**Output Type(s):** [JSON, text, audio, video]

**Output Format:** [JSON connector responses; text, audio, or video content depending on the action.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some video actions are asynchronous and return task identifiers or file references. Available actions include state-changing and destructive operations.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
