## Description: <br>
Helps agents screen MoltMarkets prediction markets, estimate probabilities, size positions, place bets, create and resolve markets, and track calibration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spiceoogway](https://clawhub.ai/user/spiceoogway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to analyze MoltMarkets prediction markets and execute account actions such as bets, market creation, resolution checks, and position review. It also guides probability estimation and risk-sized position sizing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live MoltMarkets account authority can create markets, place bets, and resolve markets without strong built-in confirmations or limits. <br>
Mitigation: Require explicit human approval outside the skill, use a least-privilege or test token, and set account-level limits before execution. <br>
Risk: The security guidance calls out create-market-with-odds.sh for argument handling and live-action confirmation concerns. <br>
Mitigation: Avoid create-market-with-odds.sh until its argument handling and live-action confirmation are fixed and reviewed. <br>
Risk: The skill reads a local MoltMarkets API key for account access. <br>
Mitigation: Use a dedicated scoped token where available and keep the key out of prompts, logs, and shared workspaces. <br>


## Reference(s): <br>
- [Forecasting Guide](references/forecasting-guide.md) <br>
- [Kelly Criterion for MoltMarkets](references/kelly-criterion.md) <br>
- [MoltMarkets API](https://api.zcombinator.io/molt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell scripts that call the MoltMarkets API when the user authorizes account actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
