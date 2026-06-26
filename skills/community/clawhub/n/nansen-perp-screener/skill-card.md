## Description: <br>
What is the state of the Hyperliquid perp market? Top contracts by volume/OI, trader leaderboard, and SM perp activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Nansen CLI data for Hyperliquid perpetual market volume, open interest, trader leaderboard, and smart-money perp activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Nansen API key and invokes the nansen CLI. <br>
Mitigation: Install only when Nansen market-data access is intended, keep the API key scoped and protected, and approve the read-only Nansen commands expected for this workflow. <br>
Risk: The installed nansen-cli package may change behavior over time. <br>
Mitigation: In stricter environments, review or pin the nansen-cli package version before use. <br>


## Reference(s): <br>
- [Nansen Perp Screener on ClawHub](https://clawhub.ai/nansen-devops/nansen-perp-screener) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples and market-data field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; intended for read-only market-data queries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
