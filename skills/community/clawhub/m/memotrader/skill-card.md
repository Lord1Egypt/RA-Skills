## Description: <br>
MemoTrader helps an assistant manage a human's MemoTrader inbox, credits, balance, cliques, conversations, and notice price through the Personal Assistant API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimbursch1](https://clawhub.ai/user/jimbursch1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with MemoTrader accounts use this skill to let an assistant triage inbox messages, surface high-value opportunities, monitor notice price and balance, and help manage profile and clique settings while leaving replies and spending decisions to the human. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a MemoTrader PA API key in persistent memory. <br>
Mitigation: Use a revocable PA key and prefer a dedicated secret store over plain memory. <br>
Risk: The skill can dismiss messages or change profile and clique settings. <br>
Mitigation: Require explicit human confirmation before dismissing messages or changing profile or clique settings. <br>
Risk: Proactive heartbeat checks can surface account activity without a direct user request. <br>
Mitigation: Limit alerts to genuinely new high-value messages, significant notice-price drift, or quiet high-value conversations. <br>


## Reference(s): <br>
- [MemoTrader API Reference](references/api.md) <br>
- [MemoTrader Platform Overview](references/platform.md) <br>
- [MemoTrader](https://memotrader.com) <br>
- [MemoTrader Personal Assistant Key Setup](https://memotrader.com/account/assistant/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline API endpoint and PowerShell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON responses from the MemoTrader API and may track last check time and known message IDs in persistent memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
