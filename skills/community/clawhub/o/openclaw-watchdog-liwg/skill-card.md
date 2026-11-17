## Description:

OpenClaw Gateway watchdog that monitors Gateway process health, WebSocket errors, Feishu, WeCom, WeChat channel status, and network connectivity, then restarts Gateway within configured limits when failures are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxwseeyouaska](https://clawhub.ai/user/lxwseeyouaska)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw Gateway availability and channel health, configure periodic checks, and recover from selected process, WebSocket, session, or network failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog can make persistent host proxy changes when it detects network problems.

Mitigation: Run it only on hosts where automatic proxy changes are acceptable, and remove or disable host-wide proxy edits before enabling the systemd watchdog when that behavior is not desired.

Risk: The watchdog can automatically restart OpenClaw Gateway and broadly terminate matching Gateway processes.

Mitigation: Avoid running it with sudo privileges, review the restart limits before deployment, and use it only where automated Gateway restarts are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Bash and systemd configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment-variable configuration and operational guidance for running a watchdog loop.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
