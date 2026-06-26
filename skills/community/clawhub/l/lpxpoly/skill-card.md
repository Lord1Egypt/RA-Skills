## Description: <br>
Lpxpoly helps agents analyze Polymarket prediction markets by comparing AI probability estimates with market prices and using Bitcoin Lightning payments per analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yebdmo2](https://clawhub.ai/user/yebdmo2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find potential prediction-market edges, analyze specific Polymarket events, browse top markets, and check Lightning balance before paid analysis calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill asks the agent to run an undeclared remote npm MCP package with a spend-capable Lightning token. <br>
Mitigation: Inspect or request the source or tarball for lpxpoly-mcp before installing, test with a low-balance or scoped spend token, and require explicit confirmation before paid analysis calls. <br>
Risk: Paid analysis calls can spend Lightning balance during market scans or individual market analysis. <br>
Mitigation: Check balance before multi-analysis sessions, warn when balance is low, and confirm the expected cost before calling paid tools. <br>
Risk: AI-generated market probabilities and position recommendations can be wrong or misleading for financial decisions. <br>
Mitigation: Present outputs as informational analysis rather than financial advice, include uncertainty and key risks, and require user review before any trading decision. <br>


## Reference(s): <br>
- [Lpxpoly Homepage](https://lpxpoly.com) <br>
- [LightningProx](https://lightningprox.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/yebdmo2/lpxpoly) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured market analysis, balance information, recommendations, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LIGHTNINGPROX_SPEND_TOKEN for paid analysis calls; market scans and individual analyses are described as costing about 50 sats each.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
