## Description: <br>
AI-powered stock prediction and market analysis for global markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filwu8](https://clawhub.ai/user/filwu8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to connect agents to G-Prophet endpoints for stock prediction, market data, technical analysis, sentiment data, account usage checks, and async analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with access to GPROPHET_API_KEY can consume paid G-Prophet points. <br>
Mitigation: Store the key outside checked-in config, use limited or test keys where possible, and monitor quotas and usage. <br>
Risk: External SDK or MCP package execution can introduce supply-chain risk. <br>
Mitigation: Verify the gprophet SDK or MCP package source and version before running it in an agent environment. <br>
Risk: Using callback_url can send analysis results to an external endpoint. <br>
Mitigation: Use callback_url only with trusted endpoints and validate where webhook results will be posted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/filwu8/gprophet-api) <br>
- [G-Prophet homepage](https://www.gprophet.com) <br>
- [API key settings](https://www.gprophet.com/settings/api-keys) <br>
- [G-Prophet dashboard](https://www.gprophet.com/dashboard) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides authenticated API, SDK, and MCP usage and describes JSON response shapes returned by the G-Prophet service.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, _meta.json, CHANGELOG released 2026-03-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
