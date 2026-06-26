## Description: <br>
Discover, analyze, and filter Polymarket smart money wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[griffithkk3-del](https://clawhub.ai/user/griffithkk3-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover profitable Polymarket wallets, screen out likely market makers or HFT behavior, and assess whether a wallet is suitable for copy trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to run a separate local Python project outside the reviewed package. <br>
Mitigation: Review and trust the referenced PolyAnalysis project before running its commands. <br>
Risk: Alchemy RPC credentials may be stored in a local .env file. <br>
Mitigation: Protect the RPC key and avoid exposing it in prompts, logs, or shared outputs. <br>
Risk: Local cache data may retain wallet-analysis information after use. <br>
Mitigation: Clear the local cache when stored wallet-analysis data is no longer needed. <br>


## Reference(s): <br>
- [Leaderboard Discovery Strategies](references/leaderboard-strategies.md) <br>
- [MM Score Details](references/mm-score-details.md) <br>
- [Polymarket Data API leaderboard endpoint](https://data-api.polymarket.com/v1/leaderboard) <br>
- [ClawHub skill page](https://clawhub.ai/griffithkk3-del/polymarket-smart-money) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [User-facing wallet analysis should emphasize copy reliability labels, MM/HFT indicators, copy trading score, and concise rationale.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
