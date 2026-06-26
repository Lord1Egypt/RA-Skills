## Description: <br>
Manage an LNbits Lightning wallet by checking balances, creating invoices, decoding invoices, and sending payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[talvasconcelos](https://clawhub.ai/user/talvasconcelos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate an LNbits Lightning wallet from an agent session, including balance checks, invoice creation, invoice decoding, and confirmed payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses LNbits wallet credentials and can send real Lightning payments. <br>
Mitigation: Use a dedicated low-balance wallet, set LNBITS_BASE_URL explicitly, and avoid exposing admin keys in chat or shared logs. <br>
Risk: Payment safeguards depend on the agent following the skill instructions. <br>
Mitigation: Require a decoded invoice review, check wallet balance first, and obtain clear yes/no confirmation before running any payment command. <br>


## Reference(s): <br>
- [LNbits](https://lnbits.com) <br>
- [ClawHub LNbits Wallet release](https://clawhub.ai/talvasconcelos/lnbits) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, LNBITS_API_KEY, and LNBITS_BASE_URL; payment flows require decoded invoice review and explicit yes/no confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
