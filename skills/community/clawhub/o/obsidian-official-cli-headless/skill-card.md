## Description:

Install and adapt the official Obsidian CLI for headless Linux servers by using a non-root user, Xvfb virtual display, ACL-based vault access, and an obs wrapper command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinrowe](https://clawhub.ai/user/darinrowe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and run the official Obsidian CLI on Debian or Ubuntu-like headless Linux servers where root execution, missing display sessions, or vault permissions would otherwise block native CLI use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root-run setup scripts can make broad system changes on the host.

Mitigation: Review the skill before installing on important hosts and run it only against a carefully chosen vault path.

Risk: Configurable privileged environment variables can affect where the wrapper is written and which user runs the CLI.

Mitigation: Clear privileged environment variables such as WRAPPER_PATH and OBSIDIAN_USER before setup unless intentionally overriding them.

Risk: Verification writes a marker to the daily note in the configured vault.

Mitigation: Run verification only when a write to the daily note is acceptable, or skip verification and inspect commands manually.

Risk: The downloaded Obsidian package is installed during setup.

Mitigation: Prefer a release that validates paths, safely creates the wrapper, and verifies the downloaded package before installation.

## Reference(s):

- [Architecture notes](references/architecture.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/darinrowe/skills/obsidian-official-cli-headless)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and concise setup status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include wrapper path, active vault path, verified commands, and remaining limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
