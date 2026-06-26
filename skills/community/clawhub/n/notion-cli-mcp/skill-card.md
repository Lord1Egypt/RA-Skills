## Description: <br>
Provides agent-facing guidance for using notion-cli as a Notion CLI and MCP server with read-only defaults, opt-in write and admin tiers, audit logs, dry-run validation, and Notion data-source support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xarkstar](https://clawhub.ai/user/0xarkstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to connect agents to Notion through notion-cli, starting from read-only access and enabling write or admin workflows only when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion integration token can expose workspace content beyond the intended workflow. <br>
Mitigation: Give the integration token only the least access needed and share it only with the pages or databases required for the task. <br>
Risk: Write or admin tiers can modify Notion content, schemas, or page locations. <br>
Mitigation: Keep the default read-only tier for general agents, enable write or admin mode only for specific workflows, and review the relevant audit logs. <br>
Risk: Installing an unexpected notion-cli binary could introduce supply-chain risk. <br>
Mitigation: Install only from the documented upstream source and verify published binaries or checksums when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xarkstar/notion-cli-mcp) <br>
- [notion-cli repository](https://github.com/0xarkstar/notion-cli) <br>
- [notion-cli-mcp on crates.io](https://crates.io/crates/notion-cli-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward notion-cli MCP commands that return JSON-wrapped Notion responses.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
