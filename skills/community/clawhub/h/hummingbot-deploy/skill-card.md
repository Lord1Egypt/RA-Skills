## Description:

Deploy Hummingbot trading infrastructure including the Hummingbot API server, optional MCP server, and optional Condor Telegram bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengtality](https://clawhub.ai/user/fengtality)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, configure, verify, and troubleshoot Hummingbot trading infrastructure across local and containerized environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable remote shell code during installation.

Mitigation: Use only pinned and reviewed scripts and container images before installing.

Risk: The skill uses weak plaintext default credentials for trading-related services.

Mitigation: Replace all default credentials with strong unique values before deployment.

Risk: The Hummingbot API could be exposed beyond trusted hosts.

Mitigation: Restrict API access to trusted hosts and networks.

Risk: The container setup path includes a sudo shim.

Mitigation: Avoid creating the sudo shim and use an environment with the required privileges configured explicitly.

Risk: Agent MCP configuration may store Hummingbot API credentials.

Mitigation: Verify where the agent stores MCP credentials and protect or rotate them as needed.

## Reference(s):

- [Hummingbot API Repository](https://github.com/hummingbot/hummingbot-api)
- [Hummingbot MCP Repository](https://github.com/hummingbot/mcp)
- [Condor Repository](https://github.com/hummingbot/condor)
- [Hummingbot API Docs](https://hummingbot.org/hummingbot-api/)
- [Hummingbot MCP Docs](https://hummingbot.org/mcp/)
- [ClawHub Skill Page](https://clawhub.ai/fengtality/skills/hummingbot-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, configuration, verification, upgrade, and troubleshooting guidance for an agent to present or execute with user approval.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
