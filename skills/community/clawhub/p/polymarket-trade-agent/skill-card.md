## Description: <br>
A Polymarket trading agent that researches markets, analyzes opportunities, checks balances and positions, and can place live buy or sell orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HansWuHan](https://clawhub.ai/user/HansWuHan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket markets, check balances and positions, and place buy or sell orders from an agent-driven CLI. It is for users who understand Polymarket, Polygon, USDC, and private-key custody risk. <br>

### Deployment Geography for Use: <br>
Global, subject to the user's local trading and Polymarket access restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live real-money Polymarket orders without built-in confirmation prompts or hard spending limits. <br>
Mitigation: Use a dedicated low-balance wallet, verify every order outside the agent, start with small positions, and add explicit confirmation plus spending limits before routine use. <br>
Risk: The skill uses a raw wallet private key to derive credentials for trading. <br>
Mitigation: Avoid exposing or logging the private key, keep it out of shared shells and transcripts, and prefer a version that redacts key material. <br>
Risk: Dependency versions are not pinned, so installs may drift across environments. <br>
Mitigation: Pin and review dependency versions before deployment, then update deliberately after testing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HansWuHan/polymarket-trade-agent) <br>
- [Polymarket](https://polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, tables, panels, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can call Polymarket APIs and submit live orders when configured with wallet credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact _meta.json reports 1.0.0 and pyproject.toml reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
