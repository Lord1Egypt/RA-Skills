## Description: <br>
OpenClaw configuration reference for openclaw.json covering gateway settings, channels, agents, sessions, sandboxing, tools, models, environment variables, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yixn](https://clawhub.ai/user/Yixn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to look up OpenClaw configuration fields, choose safer settings, and recover from broken gateway or openclaw.json changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect OpenClaw configuration examples can prevent the gateway from starting or expose it more broadly than intended. <br>
Mitigation: Back up openclaw.json, validate changes, run openclaw doctor, and require strong authentication before exposing gateway access beyond localhost. <br>
Risk: Copied examples may include token or API key placeholders that could be mishandled in real deployments. <br>
Mitigation: Keep credentials in protected environment files or secret stores and avoid hardcoding channel, gateway, or model-provider tokens in shared config. <br>
Risk: Tool execution, elevated access, open DM policies, or permissive sandbox settings can grant unintended system access. <br>
Mitigation: Prefer deny or ask modes for code execution and elevated access, restrict trusted users, and confirm Docker is available before enabling sandbox modes that require it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yixn/openclaw-config-reference) <br>
- [ClawHosters homepage](https://clawhosters.com) <br>
- [Gateway configuration reference](references/gateway.md) <br>
- [Agents configuration reference](references/agents.md) <br>
- [Channels configuration reference](references/channels.md) <br>
- [Session, sandbox, cron, and hooks reference](references/session.md) <br>
- [Tools, browser, and skills reference](references/tools.md) <br>
- [Models and environment reference](references/models-env.md) <br>
- [Troubleshooting and recovery guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples should be reviewed before applying to a live OpenClaw deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
