## Description: <br>
X-ray any Polymarket wallet for skill level, entry quality, bot detection, and edge analysis using public Polymarket market and trade data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket wallet trading behavior, compare wallet profiles, identify bot-like or anomalous activity, and inform their own research without treating the output as trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports conflicting guidance about authentication and notes authenticated Simmer account access. <br>
Mitigation: Do not provide SIMMER_API_KEY unless the user intentionally wants the skill to access Simmer account portfolio and position data. <br>
Risk: The skill can produce copytrading-oriented recommendations that may be mistaken for financial advice. <br>
Mitigation: Treat results as unsupported analysis for research and learning; require independent judgment before any trading decision. <br>
Risk: Documentation mentions live-trading risk while the reviewed analyzer appears mostly read-only, creating ambiguity about operational behavior. <br>
Mitigation: Review commands and flags before execution, avoid live or automated trading workflows unless the behavior is explicitly understood, and start with dry-run or paper-mode workflows when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-wallet-xray) <br>
- [Simmer API reference](https://docs.simmer.markets/api/overview) <br>
- [Original forensic trading analysis](https://x.com/thejayden/status/2020891572389224878) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com/markets/keyset) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Human-readable console or Markdown summaries, with optional JSON output for scripted use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet profitability metrics, entry-quality ratings, bot-detection signals, risk profile, comparison results, and recommendation text.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
