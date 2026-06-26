## Description: <br>
A comprehensive maintenance guide for installing, configuring, operating, securing, and troubleshooting OpenClaw, a self-hosted multi-channel AI agent gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forgottener](https://clawhub.ai/user/forgottener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to maintain local OpenClaw installations, including channel setup, gateway operations, model provider configuration, security hardening, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides privileged OpenClaw administration and automation guidance. <br>
Mitigation: Use it only when administering OpenClaw, and review installer scripts, shell commands, and configuration changes before execution. <br>
Risk: Gateway exposure can increase control-plane access risk. <br>
Mitigation: Keep the gateway loopback-only or tailnet-only, and require strong authentication for remote access. <br>
Risk: Approve-all or elevated full modes can allow broad system changes. <br>
Mitigation: Avoid those modes except in controlled break-glass cases, and prefer scoped allowlists and explicit approval flows. <br>
Risk: Optional third-party data flows can expose sensitive data. <br>
Mitigation: Disable or explicitly scope Firecrawl, cloud transcription, cloud embeddings, broad memory indexing, heartbeat delivery, and standing orders for sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/forgottener/openclaw-guide-maintenance) <br>
- [OpenClaw maintenance skill source](artifact/SKILL.md) <br>
- [OpenClaw security guide](artifact/security.md) <br>
- [OpenClaw installation guide](artifact/install.md) <br>
- [OpenClaw channel setup guide](artifact/channels.md) <br>
- [OpenClaw configuration reference](artifact/config_reference.md) <br>
- [OpenClaw gateway operations guide](artifact/gateway_ops.md) <br>
- [OpenClaw architecture documentation](https://docs.openclaw.ai/concepts/architecture) <br>
- [OpenClaw agent loop documentation](https://docs.openclaw.ai/concepts/agent-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for an agent; examples should be reviewed before execution.] <br>

## Skill Version(s): <br>
2026.3.24 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
