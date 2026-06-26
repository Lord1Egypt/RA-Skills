## Description: <br>
Discovers and ranks Polymarket markets by recent activity, new listings, or category using live market data and returns linked market summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnica](https://clawhub.ai/user/cnica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find trending, newly listed, or category-specific Polymarket markets with linked market names, prices, volume, trader counts, and timing context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market discovery output could be mistaken for financial advice. <br>
Mitigation: Treat results as informational market discovery only and make independent trading decisions using current source data. <br>
Risk: The skill depends on referenced local Polymarket data-layer code and local command execution. <br>
Mitigation: Install and run it only in an environment where the referenced local code is trusted and reviewed. <br>
Risk: Broad trigger phrases such as generic trade-discovery questions may invoke Polymarket-specific queries. <br>
Mitigation: Confirm user intent when a request is broad or when the surrounding context does not clearly ask for Polymarket market discovery. <br>
Risk: Recent-volume and new-market metrics are limited by the available recent trade-data window. <br>
Mitigation: State the active lookback window, avoid all-time claims, and mark unavailable metrics rather than estimating them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnica/polymarket-predictradar-market-discovery-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with linked markets and tabular or ranked market data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live data lookups and should not fabricate market names, prices, volume, trader counts, or timing metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
