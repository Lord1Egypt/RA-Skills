## Description: <br>
Query real-time prices and data for Indigo Protocol iAssets, ADA, and INDY tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current Indigo Protocol iAsset, ADA, and INDY token prices for portfolio views, protocol dashboards, and market context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Price outputs may be stale, unavailable, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Confirm the MCP tools and underlying data source are trusted and current before relying on outputs for trading, lending, or portfolio decisions. <br>
Risk: Financial workflows may request wallet keys or trading authority outside this read-only skill's scope. <br>
Mitigation: Do not provide wallet keys, signing authority, or trading permissions unless separately required by another reviewed tool. <br>


## Reference(s): <br>
- [Indigo Assets release page](https://clawhub.ai/adacapo21/indigo-assets) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [Asset Concepts](references/concepts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text responses with current price data and concise explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only price lookup guidance; no executable code, credential access, persistence, or account-changing behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
