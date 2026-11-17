## Description:

Fixes common Matrix Channel issues, including missing encryption modules, expired tokens, DNS failures, re-login, room exit operations, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boms](https://clawhub.ai/user/boms)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose and repair OpenClaw Matrix channel failures, including missing encryption support, invalid tokens, DNS resolution problems, configuration reset, room leave operations, and channel status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair steps can alter or remove Matrix account state.

Mitigation: Back up or rename state directories before resets, and confirm the affected OpenClaw account before making changes.

Risk: Package installation and rebuild commands can modify a system-wide OpenClaw installation.

Mitigation: Pin and verify package versions, test in a controlled environment when possible, and use appropriate administrative permissions.

Risk: Matrix passwords and access tokens can be exposed through shell commands, logs, or command history.

Mitigation: Avoid putting secrets directly in command lines; prefer secure prompts, protected environment variables, and token cleanup after use.

Risk: Room leave and reset operations can affect unintended Matrix rooms or bot memberships.

Mitigation: List and confirm rooms, homeservers, and bot accounts before running leave or reset operations.

## Reference(s):

- [Matrix Channel Fix on ClawHub](https://clawhub.ai/boms/skills/matrix-fix)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that modify OpenClaw Matrix account state, package installation, and Matrix room membership.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
