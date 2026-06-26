## Description: <br>
Purchase data, airtime, and digital products for Nigerian phone numbers using wallet balance with network and plan validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h1rdr3v2](https://clawhub.ai/user/h1rdr3v2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to buy data, airtime, and digital products for Nigerian phone numbers, check balances, manage contacts, and update notification preferences through the CreditWithBleon API. The skill guides an agent through authentication, product discovery, confirmation, purchase, and order status workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session tokens are persisted locally and can be printed by helper commands. <br>
Mitigation: Use only on trusted machines, avoid sharing logs or transcripts containing command output, and clear the saved session token after use. <br>
Risk: The skill can initiate wallet-funded purchases and account changes. <br>
Mitigation: Require explicit confirmation of recipient, plan, amount, wallet balance, and any account mutation before submitting requests. <br>


## Reference(s): <br>
- [ClawHub Pay Bills listing](https://clawhub.ai/h1rdr3v2/pay-bills) <br>
- [CreditWithBleon API base URL](https://lodu.bleon.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may produce authentication, purchase, account-management, and status-check instructions for an agent; purchases and account mutations require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
