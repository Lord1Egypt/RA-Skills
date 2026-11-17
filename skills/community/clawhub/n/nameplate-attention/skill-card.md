## Description:

Nameplate Attention gives an agent a local on-screen attention alert with a topmost message card and pulsating screen borders via Nameplate when it is blocked on a human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to request human attention on a Mac before interactive approvals, password-manager prompts, or other blocked workflows that need a clear reason.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attention alerts can briefly interrupt the user's screen.

Mitigation: Use the skill only when blocked on the human and include the clear activation reason required by the skill.

Risk: The commands depend on the local Nameplate app and CLI being installed and trusted.

Mitigation: Confirm Nameplate.app is trusted locally before use and invoke the documented helper path or PATH symlink.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steipete/skills/nameplate-attention)
- [Publisher profile](https://clawhub.ai/user/steipete)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Nameplate app and a clear reason for each attention request.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
