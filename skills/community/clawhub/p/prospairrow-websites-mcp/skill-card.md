## Description: <br>
Connects an AI agent to Prospairrow through a local websites-mcp JSON-RPC server to extract and enrich prospects, score companies, discover competitors, and generate content marketing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[discry](https://clawhub.ai/user/discry) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, and developer teams use this skill to let an agent run Prospairrow prospecting workflows through MCP, including lead extraction, enrichment, scoring, competitor discovery, and content generation. It is intended for users who can supply a Prospairrow API key and operate a local Node-based runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Prospairrow API credentials and prospect data. <br>
Mitigation: Install and run it only in trusted local environments, pass API keys through request headers or protected environment variables, and keep keys out of shell history and committed configuration. <br>
Risk: Some tasks labeled read-only may make account-affecting or quota-affecting Prospairrow POST calls. <br>
Mitigation: Prefer the default read-only runtime mode, review requested tasks before execution, and enable write mode only when mutations are intentionally required. <br>
Risk: Optional diagnostics, invocation logging, and saved browser sessions can store sensitive operational data on disk. <br>
Mitigation: Leave invocation logging and config-file API-key fallback disabled unless needed, enable diagnostics only on trusted machines, and use the storage-state write disable flag when saved browser sessions are not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/discry/prospairrow-websites-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/discry) <br>
- [README](artifact/README.md) <br>
- [API schema](artifact/API_SCHEMA.md) <br>
- [Install guide](artifact/docs/INSTALL.md) <br>
- [Configuration guide](artifact/docs/CONFIGURATION.md) <br>
- [Operations guide](artifact/docs/OPERATIONS.md) <br>
- [Troubleshooting guide](artifact/docs/TROUBLESHOOTING.md) <br>
- [Prospairrow application](https://app.prospairrow.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON-RPC request examples, and JSON task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local websites-mcp listener, Node runtime dependencies, and a Prospairrow API key.] <br>

## Skill Version(s): <br>
1.2.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
