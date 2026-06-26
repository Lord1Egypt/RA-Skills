## Description: <br>
Provides OpenClaw self-hosted AI agent framework guidance for installation, configuration, channel setup, memory tuning, Docker deployment, troubleshooting, and security hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arn0ld87](https://clawhub.ai/user/arn0ld87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure, administer, troubleshoot, secure, and deploy OpenClaw self-hosted AI agent installations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may lead users or agents to run unverified remote code. <br>
Mitigation: Review commands before running them and prefer package-manager or signed-release installation paths over curl-to-shell snippets. <br>
Risk: Configuration examples may cause secrets or tokens to be stored unsafely. <br>
Mitigation: Use SecretRef or equivalent secret-management patterns and avoid placing real tokens in config examples. <br>
Risk: Memory, embeddings, webhooks, and logging integrations may persist or export sensitive data. <br>
Mitigation: Treat those integrations as sensitive data flows and restrict broad triggers, channels, and logging where possible. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Docker installation](https://docs.openclaw.ai/install/docker) <br>
- [OpenClaw agent workspace](https://docs.openclaw.ai/concepts/agent-workspace) <br>
- [OpenClaw memory](https://docs.openclaw.ai/concepts/memory) <br>
- [OpenClaw multi-agent](https://docs.openclaw.ai/concepts/multi-agent) <br>
- [OpenClaw secrets](https://docs.openclaw.ai/gateway/secrets) <br>
- [OpenClaw configuration](https://docs.openclaw.ai/gateway/configuration) <br>
- [OpenClaw security](https://docs.openclaw.ai/security) <br>
- [Quick reference](references/quick-reference.md) <br>
- [Security hardening](references/security-hardening.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Configuration reference](references/config-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON/JSON5 configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may include operational commands and configuration examples that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
