## Description: <br>
Scans Polymarket hourly BTC/ETH/SOL/XRP markets for edge opportunities using the Argus strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamieRossouw](https://clawhub.ai/user/JamieRossouw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to scan current Polymarket hourly crypto prediction markets and rank potential edge opportunities for BTC/ETH/SOL/XRP. Treat the output as heuristic gambling and financial analysis rather than trading instructions or guaranteed returns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns betting-edge estimates and Kelly sizing that could be mistaken for guaranteed financial advice. <br>
Mitigation: Treat results as heuristic gambling and financial analysis, verify independently, and avoid risking funds based only on the skill output. <br>
Risk: The skill depends on outbound requests to public Polymarket-related APIs, so market data may be unavailable, delayed, or stale. <br>
Mitigation: Confirm market freshness and odds directly before acting on any suggested opportunity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JamieRossouw/polymarket-scout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with ranked edge opportunities and bet-sizing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analysis based on public Polymarket-related market data; no credentials or trade execution are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
