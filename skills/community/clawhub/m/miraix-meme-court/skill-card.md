## Description: <br>
Use this skill when the user wants to run Miraix Meme Court, shortlist Solana meme candidates, apply Rug Court safety and liquidity checks, approve one disciplined meme trade, prepare an unsigned payload when live Bitget execution is available, or check the status of a previously prepared order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run Miraix's public Solana meme-trading flow, compare candidates through Scout and Rug Court checks, and return one approved trade with execution readiness details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run implicitly and uses default wallet and trade parameters. <br>
Mitigation: Confirm the intended wallet address, budget, risk mode, and strategy before relying on the generated trade summary or preparing a payload. <br>
Risk: The skill sends wallet and trade details to Miraix third-party endpoints. <br>
Mitigation: Use it only when comfortable sharing those details with Miraix and review the endpoint responses before taking action. <br>
Risk: Trade outputs may be mistaken for financial advice or completed execution. <br>
Mitigation: Treat outputs as informational, verify any unsigned payload in the wallet, and do not represent a trade as signed, submitted, or filled unless the API response proves it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/richard7463/miraix-meme-court) <br>
- [Miraix Meme Rotation Desk API](https://app.miraix.fun/api/meme-rotation-desk) <br>
- [Miraix Prepare API](https://app.miraix.fun/api/meme-rotation-desk/prepare) <br>
- [Miraix Order Status API](https://app.miraix.fun/api/meme-rotation-desk/order-status) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown with API-derived trade summaries and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should lead with the approved trade, include Rug Court and execution readiness summaries, preserve exact API field values, and identify preview mode or unavailable payload preparation when applicable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
