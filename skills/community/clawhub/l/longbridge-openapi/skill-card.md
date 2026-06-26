## Description: <br>
Wraps Longbridge Securities workflows for market data, financial analysis, account state, watchlists, price alerts, statements, and recurring DCA plans across US, Hong Kong, A-share, Singapore, and crypto markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genkin-he](https://clawhub.ai/user/genkin-he) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to route stock, market, portfolio, and trading-related requests through Longbridge Securities CLI or MCP surfaces. It supports read-only market analysis and guarded account workflows such as watchlist changes, price alerts, statement exports, and recurring DCA plan management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access brokerage account data and sensitive credentials. <br>
Mitigation: Install only for intended Longbridge account and market workflows, grant the least privilege needed, keep tokens out of shared environments, and avoid exposing private account details in shared outputs. <br>
Risk: Watchlist changes, price alerts, statement exports, and recurring DCA plans can change persistent account state or expose private records. <br>
Mitigation: Review every preview carefully and require explicit confirmation before mutating actions or statement exports. <br>
Risk: Recurring DCA plans can commit real money on a schedule if configured incorrectly. <br>
Mitigation: Read back every DCA parameter before confirmation and do not silently retry failed DCA operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/genkin-he/longbridge-openapi) <br>
- [Longbridge skills homepage](https://github.com/longbridge/skills) <br>
- [Longbridge OpenAPI documentation](https://open.longbridge.com) <br>
- [Longbridge OpenAPI llms.txt](https://open.longbridge.com/llms.txt) <br>
- [Longbridge MCP endpoint](https://openapi.longbridge.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Longbridge-sourced market data, account summaries, warnings, and preview text before sensitive or mutating actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
