## Description: <br>
Find global B2B prospects with LeadsDaddy via MCP for importer, distributor, wholesaler, buyer, channel partner, and market-entry workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[energypantry](https://clawhub.ai/user/energypantry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, export, and business-development users use this skill to guide an agent through LeadsDaddy MCP workflows for product profiling, lead-discovery task creation, lead review, and selective lead unlocking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can unlock leads, which may spend credits or reveal contact data. <br>
Mitigation: Use a scoped LeadsDaddy token and require explicit user approval before any lead_unlock action. <br>
Risk: Lead-discovery results may include low-fit, noisy, or misleading business matches. <br>
Mitigation: Review task output first, classify leads by fit, and unlock only high-fit or clearly promising leads. <br>
Risk: The skill depends on third-party MCP software and LeadsDaddy service URLs. <br>
Mitigation: Verify the @leadsdaddy/mcp package and configured LeadsDaddy URLs before installation or use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/energypantry/leadsdaddy-b2b-lead-finder) <br>
- [LeadsDaddy homepage](https://www.leads-daddy.com) <br>
- [LeadsDaddy MCP API endpoint](https://edge.leads-daddy.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and lead-review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LeadsDaddy MCP configuration and a scoped LeadsDaddy token before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
