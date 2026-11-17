## Description:

OpenClaw PC Control lets an agent operate a Windows PC through local CLI and HTTP interfaces for screenshots, keyboard and mouse actions, clipboard access, file operations, process and window management, browser automation, and shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukenccode](https://clawhub.ai/user/lukenccode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent inspect and control a Windows desktop session through screenshots, input automation, file/process/window operations, browser automation, and shell command execution. It is suited to tightly controlled local or test environments where full logged-in-session control is intentional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication and safety boundaries are weak for the level of Windows PC control exposed.

Mitigation: Install only in an isolated test environment unless the maintainer fixes the default shared API key, network binding, TLS/auth model, security-mode downgrade endpoint, file sandbox, shell validation, and browser security flags.

Risk: If the service is reachable, it can expose or control the logged-in Windows session through screenshots, input automation, file access, process control, browser automation, and shell execution.

Mitigation: Run with a least-privileged account, restrict network reachability, keep the strongest security mode enabled, rotate the API key before use, and review each action before execution.

Risk: Browser automation behavior can weaken normal browser isolation and certificate protections.

Mitigation: Use a dedicated browser profile with no sensitive sessions or stored credentials, and avoid using the browser automation endpoints on untrusted sites.

## Reference(s):

- [PC Control API documentation](references/api-doc.md)
- [ClawHub skill page](https://clawhub.ai/lukenccode/skills/openclaw-pc-control)
- [ClawHub publisher profile](https://clawhub.ai/user/lukenccode)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands, HTTP API examples, and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime endpoints return JSON objects with success, data, and error fields.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
