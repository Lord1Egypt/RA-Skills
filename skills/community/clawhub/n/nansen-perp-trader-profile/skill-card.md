## Description: <br>
Deep dive on a Hyperliquid perp trader, including identity, open positions, recent trades, and overall PnL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts and developers use this skill to inspect a Hyperliquid perpetuals trader address, summarize identity labels, open positions, recent trades, margin usage, PnL, and leaderboard standing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad Nansen CLI access, which may allow commands outside the documented trader-profile lookups. <br>
Mitigation: Review proposed nansen commands before execution and keep usage limited to the documented research profiler and leaderboard commands. <br>
Risk: A configured Nansen CLI may have access to wallets, Privy credentials, payment setup, or trading capabilities. <br>
Mitigation: Use credentials appropriate for research workflows and prefer narrower command permissions before deploying this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-perp-trader-profile) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; commands profile one trader address across labels, positions, trades, and leaderboard data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
