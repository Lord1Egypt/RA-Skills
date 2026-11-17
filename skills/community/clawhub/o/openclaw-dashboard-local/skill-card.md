## Description:

OpenClaw Dashboard helps an agent install, run, configure, and present a local visual operations dashboard for supervising one OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaszh7](https://clawhub.ai/user/lucaszh7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and operate a local dashboard for one OpenClaw agent, with live status visibility, chat access, efficiency trends, configuration guidance, and optional recovery helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled launchd installer creates persistent background services with auto-start and KeepAlive behavior and points to runtime programs that are not present in the evidence bundle.

Mitigation: Run the dashboard in foreground/manual mode unless persistent services are intentionally required; do not run install_launchd.sh until all referenced runtime files are present, reviewed, and trusted.

Risk: The stop script may terminate another local process if it is listening on port 18991.

Mitigation: Check the process using port 18991 before stopping the monitor, or change the configured port when another service already uses it.

Risk: Recovery and auto-heal controls can create false confidence if success is assumed without confirming state.

Mitigation: Confirm recovery actions through logs or visible dashboard state before reporting that a nudge, heal, or restart succeeded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucaszh7/skills/openclaw-dashboard-local)
- [Publisher profile](https://clawhub.ai/user/lucaszh7)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Example configuration](artifact/config.example.json)
- [Artifact manifest](artifact/manifest.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local foreground/background launch steps, macOS launchd guidance, dashboard configuration, release copy, and safety notes.]

## Skill Version(s):

1.0.2 (source: evidence.json release.version; artifact manifest and release notes report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
