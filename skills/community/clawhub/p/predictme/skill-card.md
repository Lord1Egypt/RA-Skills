## Description: <br>
Trade 10-second crypto prediction markets on PredictMe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howardpen9](https://clawhub.ai/user/howardpen9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to register with PredictMe, manage TEST/BONUS trading credentials, inspect BTC/ETH/SOL odds, place TEST/BONUS bets, and review betting performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to register with PredictMe, store a bearer API key, and place autonomous TEST/BONUS bets. <br>
Mitigation: Require explicit owner approval before betting, especially during initial use, and store the API key in a locked-down file or proper secret store. <br>
Risk: Weak credential handling could expose the PredictMe API key or agent identity. <br>
Mitigation: Save credentials outside shared project files where possible, restrict file permissions, and add local credential files to ignore lists. <br>
Risk: The artifact encourages evaluating TEST-balance performance before recommending real USDC activity. <br>
Mitigation: Treat any move to real-funds trading as a separate human decision and do not let the agent autonomously deposit, connect wallets, or trade real balance. <br>
Risk: Prediction-market guidance can lead to overtrading or misleading confidence in short-term crypto price forecasts. <br>
Mitigation: Use conservative bet limits, stop-loss and profit-target controls, performance review, and owner confirmation for high-risk or unusual settings. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/howardpen9/predictme) <br>
- [PredictMe Agent Trading Guide](https://app.predictme.me/skill.md) <br>
- [PredictMe Agent API Spec](https://app.predictme.me/agents.json) <br>
- [PredictMe Agent Discovery](https://app.predictme.me/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline Python and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes strategy guidance, credential and preference file examples, REST API request patterns, and trading-loop examples for TEST/BONUS balances.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
