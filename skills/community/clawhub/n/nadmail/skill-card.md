## Description: <br>
NadMail gives AI agents wallet-authenticated email identities on Monad, with support for registration, sending, inbox access, credits, and payment-linked emo-buy boosts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to register and operate NadMail email accounts, send and receive mail, and manage payment-linked features for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys and NadMail auth tokens are used by the skill. <br>
Mitigation: Use a dedicated low-value wallet, prefer environment variables for private keys, and protect ~/.nadmail/token.json and private-key.enc with local file permissions. <br>
Risk: Payment-linked email actions can spend MON through micro-buys, emo-buy boosts, and credit purchases. <br>
Mitigation: Review emo-buy costs and daily caps before allowing autonomous sending, and require explicit operator approval for payment-bearing workflows. <br>
Risk: Password entry for encrypted wallet use may be exposed in recorded, shared, or monitored terminals. <br>
Mitigation: Avoid entering wallet passwords in shared or recorded sessions and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [NadMail website](https://nadmail.ai) <br>
- [NadMail API](https://api.nadmail.ai) <br>
- [NadMail API docs](https://api.nadmail.ai/api/docs) <br>
- [ClawHub skill page](https://clawhub.ai/daaab/nadmail) <br>
- [Publisher profile](https://clawhub.ai/user/daaab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents through local Node.js scripts that call NadMail APIs and read or write local NadMail configuration files.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
