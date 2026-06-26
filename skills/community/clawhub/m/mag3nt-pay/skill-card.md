## Description: <br>
Pay for APIs and services, receive payments, and manage agent wallets using Mag3nt USDC virtual cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mag3nt](https://clawhub.ai/user/mag3nt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to let agents check Mag3nt card balances, settle x402, MPP, and Pay Link API payments, and issue or verify AP2 payment mandates with Mag3nt credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real Mag3nt/USDC spending authority. <br>
Mitigation: Use low-limit or test cards first, set strict card and mandate caps, and require confirmation for meaningful purchases. <br>
Risk: The skill depends on sensitive Mag3nt API key and card token credentials. <br>
Mitigation: Keep MAG3NT_API_KEY and MAG3NT_CARD_TOKEN in the local environment only and out of shared files, prompts, logs, and transcripts. <br>
Risk: Payment flows may forward original request bodies or headers during payment and retry. <br>
Mitigation: Review any flow that forwards request bodies or headers before payment or retry, especially when the original request contains user data or secrets. <br>
Risk: Payments can fail or spend unexpectedly if balance, status, method, or network assumptions are wrong. <br>
Mitigation: Check card balance and status before payment, verify the merchant's amount and supported payment methods, and log transaction IDs and on-chain hashes as charge evidence. <br>


## Reference(s): <br>
- [Mag3nt Pay on ClawHub](https://clawhub.ai/mag3nt/mag3nt-pay) <br>
- [Setup](references/setup.md) <br>
- [Balance](references/balance.md) <br>
- [Pay Link Settlement](references/paylink-pay.md) <br>
- [Universal Pay](references/x402-pay.md) <br>
- [MPP Pay](references/mpp-pay.md) <br>
- [AP2 Pay](references/ap2-pay.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript examples, API request examples, and JSON response shapes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead the agent to execute Mag3nt API requests when configured with valid user credentials.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
