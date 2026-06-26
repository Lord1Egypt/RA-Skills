## Description: <br>
Autonomous ORE mining on Solana via refinORE. Onboard humans, start/stop sessions, optimize tile strategies, track P&L, manage risk, auto-restart, multi-coin mining (SOL/USDC/stablecoins), DCA/limit orders, staking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JussCubs](https://clawhub.ai/user/JussCubs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure an agent that can manage refinORE ORE mining sessions, monitor balances and rounds, adjust strategies, and report mining performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a funded refinORE account and deploy funds into recurring mining sessions. <br>
Mitigation: Use the official API URL, a small starting balance, explicit per-round and total spend limits, and confirmation before starting or restarting mining. <br>
Risk: API keys can control account actions and may be exposed if pasted into chat or logs. <br>
Mitigation: Provide the key only through REFINORE_API_KEY, use a revocable or scoped key if available, and revoke or rotate it when no longer needed. <br>
Risk: Auto-restart, live strategy edits, and DCA or limit orders can continue changing exposure after the initial setup. <br>
Mitigation: Require confirmation before enabling those actions and document how to stop sessions, cancel orders, and revoke the API key. <br>


## Reference(s): <br>
- [ORE Miner ClawHub Release](https://clawhub.ai/JussCubs/ore-miner) <br>
- [refinORE](https://automine.refinore.com) <br>
- [refinORE API](https://automine.refinore.com/api) <br>
- [refinORE API Endpoints](references/api-endpoints.md) <br>
- [ORE V2 Mining Rules & Mechanics](references/mining-rules.md) <br>
- [ORE Mining Strategies](references/strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline bash commands, JSON request examples, and human-facing operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REFINORE_API_URL and REFINORE_API_KEY, plus bash, curl, and python3 for bundled helper scripts.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
