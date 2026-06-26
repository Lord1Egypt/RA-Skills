## Description: <br>
Provides commodity market analysis for steel, non-ferrous metals, energy and chemical products, furnace materials, and related supply-demand or price-trend questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyb92](https://clawhub.ai/user/wyb92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to request structured Mysteel commodity-market reports and receive expanded Markdown interpretation of prices, supply, demand, inventory, sentiment, risks, and practical guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local Mysteel API key and sends market-analysis queries to Mysteel. <br>
Mitigation: Install only when Mysteel is trusted for submitted queries, protect references/api_key.md, and avoid submitting confidential business details unless allowed by the applicable Mysteel terms. <br>
Risk: The helper script is invoked with a user-derived query argument. <br>
Mitigation: Use careful argument quoting when running scripts/analyze.py and review generated shell commands before execution. <br>


## Reference(s): <br>
- [API key configuration](references/api_key.md) <br>
- [Mysteel analysis helper script](scripts/analyze.py) <br>
- [Mysteel analysis API endpoint](https://mcp.mysteel.com/mcp/info/chat-robot/rag/answer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown commodity-market analysis report with configuration guidance and shell command usage when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid Mysteel API key in references/api_key.md; API calls may take about 90 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
