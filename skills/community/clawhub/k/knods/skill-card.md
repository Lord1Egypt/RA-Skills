## Description:

Build and modify Knods visual AI workflows using either the OpenClaw Gateway polling protocol or the Knods headless flows API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alesys](https://clawhub.ai/user/alesys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw agent with Knods, either by handling Iris-style canvas chat payloads or by programmatically discovering, running, polling, cancelling, and retrieving results from Knods flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent user service that polls Knods and forwards remote chat content into a local OpenClaw agent.

Mitigation: Use a dedicated least-privileged OpenClaw agent profile and disable or stop the systemd user service when the bridge is not needed.

Risk: Gateway tokens may be embedded in URLs and exposed through service logs.

Mitigation: Prefer separate locked-down environment files for Knods secrets, avoid placing tokens in logged URLs where possible, and rotate gateway tokens if logs may have exposed them.

Risk: The bridge can connect local automation to a remote Knods host.

Mitigation: Use HTTPS and trusted Knods hosts, and review the configured base URLs and API keys before enabling the service.

## Reference(s):

- [Knods release page](https://clawhub.ai/alesys/skills/knods)
- [Project homepage](https://github.com/alesys/openclaw-skill-knods)
- [OpenClaw Gateway Protocol (Knods)](references/protocol.md)
- [Knods Headless Flow Execution API](references/headless-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON action blocks and shell commands; command-line clients emit JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit compact [KNODS_ACTION] JSON blocks when a Knods canvas mutation is intended; otherwise returns normal assistant text.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
