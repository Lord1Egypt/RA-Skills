## Description: <br>
Comprehensive agentic skills for NEAR Protocol, including gas optimization and on-chain analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mastrophot](https://clawhub.ai/user/mastrophot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to query NEAR Protocol gas data, compare transaction costs, and gather public on-chain analytics for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound requests to NEAR RPC and NearBlocks may expose queried account IDs, contract IDs, or usage patterns to those public API providers. <br>
Mitigation: Use the skill only when those outbound requests are acceptable, and avoid querying account IDs or contracts considered sensitive. <br>
Risk: Dependency or lockfile changes could alter API behavior or introduce new network-facing code. <br>
Mitigation: Keep the lockfile under review and inspect dependency changes before upgrading the skill. <br>
Risk: Analytics and gas estimates depend on availability and freshness of public blockchain APIs. <br>
Mitigation: Treat outputs as operational guidance and cross-check important cost or network-health decisions against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mastrophot/near-agent-skills) <br>
- [NEAR Mainnet RPC](https://rpc.mainnet.near.org) <br>
- [NearBlocks transactions API](https://api.nearblocks.io/v1/txns?limit=5&sort=amount&order=desc) <br>
- [NearBlocks contracts API](https://api.nearblocks.io/v1/contracts?limit=5&sort=txns&order=desc) <br>
- [NearBlocks stats API](https://api.nearblocks.io/v1/stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Plain text responses and JSON-like structured objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make outbound read-only requests to NEAR RPC and NearBlocks public APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
