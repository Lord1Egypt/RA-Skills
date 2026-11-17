## Description:

Configure a powerful macOS machine to host multiple dedicated OpenClaw agent users with Fast User Switching, a shared Homebrew toolchain, per-user OpenClaw homes, per-user SSH trust, and auditable rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to plan and configure a macOS host for multiple dedicated OpenClaw agent users, including shared Homebrew tooling, per-user state, shell verification, and rollout receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-creation scripts handle passwords and dry-run or transcript output may expose account credentials.

Mitigation: Review and fix password handling before running account-creation scripts on a real Mac; treat generated transcripts as sensitive.

Risk: Generated privileged admin commands may be unsafe if inputs are not validated or safely quoted.

Mitigation: Validate user-provided account names and command parameters, prefer reviewed command rendering, and require explicit administrator confirmation before privileged execution.

Risk: The skill changes macOS user accounts, shell startup files, SSH directories, and shared toolchain access.

Mitigation: Run dry-runs first, keep one macOS user per agent, avoid unnecessary admin grants, keep SSH keys and OpenClaw state private per user, and preserve shared Homebrew during rollback.

## Reference(s):

- [Fast User Switching](references/fast-user-switching.md)
- [Shared Homebrew](references/shared-homebrew.md)
- [ClawHub Skill Page](https://clawhub.ai/matthewxmurphy/skills/mac-multi-user-agents)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Text]

**Output Format:** [Markdown guidance with shell commands, configuration checks, and JSONL receipt output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run command rendering, host inspection output, per-user shell verification output, and optional JSONL rollout receipts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
