## Description: <br>
DeFi vault intelligence for risk scores, yield comparison, portfolio analysis, and oracle monitoring across Morpho, Yearn, Aave, Beefy, and Spark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkoranges](https://clawhub.ai/user/zkoranges) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to query Philidor's CLI/API for DeFi vault discovery, risk-aware yield comparison, wallet portfolio analysis, protocol data, curator data, and oracle freshness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Philidor's external npm CLI and API for DeFi vault and portfolio lookups. <br>
Mitigation: Install and use it only when the publisher and service are trusted, and verify the CLI package and API endpoint before use. <br>
Risk: DeFi risk scores, yield data, and recommendations may be incomplete, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as informational, check data freshness and incident/oracle signals, and avoid recommending vaults based on APR alone. <br>
Risk: Wallet portfolio analysis can expose linkable public on-chain activity to the service. <br>
Mitigation: Submit wallet addresses only when the user understands and accepts the privacy implications. <br>


## Reference(s): <br>
- [Philidor Website](https://philidor.io) <br>
- [Philidor API Documentation](https://api.philidor.io/v1/docs) <br>
- [Philidor Risk Methodology](https://philidor.io/risk) <br>
- [ClawHub Skill Page](https://clawhub.ai/zkoranges/philidor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and references to JSON, table, or CSV CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent workflows should prefer explicit JSON output for stable parsing.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
