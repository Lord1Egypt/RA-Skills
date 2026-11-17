## Description:

OpenClaw Studio helps an agent install, run, configure, and present a local visual operations dashboard for supervising one OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaszh7](https://clawhub.ai/user/lucaszh7)

### License/Terms of Use:

MIT

## Use Case:

External developers and operators use this skill to run a local dashboard for one OpenClaw agent, monitor status and efficiency trends, access chat controls, and apply optional recovery helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a macOS persistence installer that can start monitor, auto-heal, and watchdog LaunchAgents at login.

Mitigation: Prefer the foreground run command for routine use; run install_launchd.sh only after explicit user approval, verify runtime files first, and remove installed LaunchAgents with uninstall_launchd.sh or launchctl when no longer needed.

Risk: Recovery helpers may create a false impression that an agent action succeeded.

Mitigation: Confirm recovery outcomes through logs or visible dashboard state before reporting success.

## Reference(s):

- [OpenClaw Studio ClawHub page](https://clawhub.ai/lucaszh7/skills/openclaw-studio)
- [Declared repository](https://github.com/LucasZH7/openclaw-studio)
- [README](README.md)
- [Market listing](MARKET_LISTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and configuration file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup, operation, presentation, and safety guidance for a single-agent dashboard.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
