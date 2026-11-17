## Description:

Query GLM coding plan usage statistics, including quota, model usage, and MCP tool usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orientluna](https://clawhub.ai/user/orientluna)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to check GLM coding plan quota, model usage, and MCP tool usage from their configured provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cron setup can keep running every hour and write usage output to a local log.

Mitigation: Run the script on demand unless continuous monitoring is intentional; document and verify how to remove the cron entry and manage the generated log.

Risk: The script reads the GLM API key from the local OpenClaw configuration.

Mitigation: Protect the OpenClaw configuration file, avoid exposing logs or command output that could reveal sensitive configuration context, and rotate the API key if exposure is suspected.

## Reference(s):

- [GLM Coding Plan API Endpoints Reference](artifact/references/api-endpoints.md)
- [Installation Guide](artifact/docs/INSTALLATION.md)
- [OpenClaw Documentation](https://openclaw.dev)
- [GLM Coding Plan](https://open.bigmodel.cn)
- [ClawHub Skill Page](https://clawhub.ai/orientluna/skills/openclaw-glm-plan-usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and terminal-formatted usage statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English output; requires curl, jq, OpenClaw provider configuration, and a GLM Coding Plan API key.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
