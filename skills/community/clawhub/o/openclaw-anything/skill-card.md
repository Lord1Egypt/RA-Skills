## Description: <br>
OpenClaw CLI wrapper for installing, configuring, and managing gateway, channels, models, agents, nodes, browser, memory, security, and automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doanbactam](https://clawhub.ai/user/doanbactam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to navigate OpenClaw CLI commands, configure gateway and channel behavior, manage models and agents, and run deployment or maintenance workflows with local reference guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper is not a strict safety boundary, and several OpenClaw command groups can change configuration, account state, messaging state, security settings, or approvals. <br>
Mitigation: Use the skill only with a trusted local OpenClaw CLI, grant agents narrow access, prefer read-only checks first, and require explicit review for mutating gateway, channel, model, agent, message, security, and approvals commands. <br>
Risk: High-risk operations can run shell commands, browser automation, node actions, device sensor access, cron changes, plugin or hook installation, secrets application, sandbox recreation, webhooks, or DNS setup. <br>
Mitigation: Keep OPENCLAW_WRAPPER_ALLOW_RISKY unset by default, enable it only for a single reviewed action, verify node identity before approval, and keep gateways on loopback unless remote access is intentional. <br>
Risk: Bulk shell-environment import and plaintext API keys can expose secrets to OpenClaw workflows. <br>
Mitigation: Avoid OPENCLAW_LOAD_SHELL_ENV and plaintext keys unless needed, use dry-run and audit flows for secrets changes, and periodically run OpenClaw security and secrets audits. <br>


## Reference(s): <br>
- [OpenClaw Skill Page](https://clawhub.ai/doanbactam/openclaw-anything) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw CLI Reference](references/cli-full.md) <br>
- [OpenClaw Security Policy](references/security-policy.md) <br>
- [OpenClaw Configuration Reference](references/config-schema.md) <br>
- [OpenClaw Deployment](references/deployment.md) <br>
- [OpenClaw Prerequisites](references/prerequisites.md) <br>
- [OpenClaw Nodes and Platforms](references/nodes-platforms.md) <br>
- [OpenClaw Advanced Tools](references/advanced-tools.md) <br>
- [OpenClaw Documentation Hubs](references/hubs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local openclaw CLI for command execution; high-risk wrapper routes require OPENCLAW_WRAPPER_ALLOW_RISKY=1.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
