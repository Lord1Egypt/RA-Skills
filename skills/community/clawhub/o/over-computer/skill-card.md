## Description: <br>
Trade on prediction markets through over.computer by browsing markets, approving funds, placing buy and sell orders, and checking Myriad positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dabors](https://clawhub.ai/user/dabors) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators use this skill to let an agent interact with over.computer and Myriad prediction-market workflows, including market lookup, wallet-linked registration, order placement, and position review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent wallet-linked prediction-market trading authority. <br>
Mitigation: Install only when that authority is intended, configure strict limits on over.computer, and revoke or rotate OVER_API_KEY when the integration is no longer needed. <br>
Risk: Orders may execute without an explicit per-trade confirmation requirement in the skill instructions. <br>
Mitigation: Require operator confirmation before every order and use unique idempotency keys to reduce duplicate execution risk. <br>
Risk: Remote operator configuration can include trading instructions that affect agent behavior. <br>
Mitigation: Review the active remote prompt and server-side limits before trading, and stop when API guardrails reject an action. <br>


## Reference(s): <br>
- [Over Computer](https://over.computer) <br>
- [ClawHub skill page](https://clawhub.ai/dabors/over-computer) <br>
- [Publisher profile](https://clawhub.ai/user/dabors) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash code blocks and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OVER_API_KEY for authenticated Myriad and agent endpoints.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
