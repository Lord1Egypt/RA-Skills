## Description: <br>
Trade 10-second crypto prediction markets on PredictMe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidpolotm](https://clawhub.ai/user/davidpolotm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and AI-agent operators use this skill to register a PredictMe agent, manage API credentials and owner preferences, inspect BTC/ETH/SOL prediction-market odds, and place TEST or BONUS balance bets with risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release identity is Mi Analista, while the artifact content presents a PredictMe trading skill. <br>
Mitigation: Verify that the Mi Analista package is intentionally the PredictMe skill before installing or enabling it. <br>
Risk: The skill can register an agent, store an API key, and place rapid prediction-market bets. <br>
Mitigation: Set requireApproval=true before trading, use small stop-loss and bet limits, and protect or delete the local credentials file when no longer needed. <br>
Risk: TEST/BONUS betting and recommendations to move to real USDC carry gambling-like financial risk. <br>
Mitigation: Keep activity in TEST/BONUS balances unless the owner explicitly chooses otherwise, and require clear human review before any transition to real-money trading. <br>
Risk: Registration may share an email address and optional wallet address with PredictMe. <br>
Mitigation: Use only contact and wallet information the owner is comfortable sharing with the PredictMe service. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davidpolotm/mi-analista) <br>
- [PredictMe agent API specification](https://app.predictme.me/agents.json) <br>
- [PredictMe agent trading guide](https://app.predictme.me/skill.md) <br>
- [PredictMe agent discovery card](https://app.predictme.me/agent-card.json) <br>
- [PredictMe LLM reference](https://app.predictme.me/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, Python-style code snippets, and REST API request descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce registration, polling, credential-storage, betting, and performance-reporting instructions for PredictMe agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports PredictMe skill 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
