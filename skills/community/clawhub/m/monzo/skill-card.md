## Description: <br>
Access Monzo bank account - check balance, view transactions, manage pots, send feed notifications. For personal finance queries and banking automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RHesketh](https://clawhub.ai/user/RHesketh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Monzo account for balance checks, transaction review, savings pot management, receipts, feed notifications, and webhook management. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Monzo API access can expose account data and allow account changes through an agent. <br>
Mitigation: Install only on a machine you control, review connected apps in Monzo, and revoke access immediately if suspicious activity appears. <br>
Risk: Pot movement, receipt deletion, transaction annotation, feed notification, and webhook changes can alter banking data without built-in confirmation. <br>
Mitigation: Require explicit user confirmation before any operation that moves money, sends notifications, deletes receipts, annotates transactions, or changes webhooks. <br>
Risk: MONZO_KEYRING_PASSWORD and encrypted credentials are sensitive on shared or compromised systems. <br>
Mitigation: Keep the password out of shared config where possible, restrict file permissions, and use a password manager or secrets manager. <br>


## Reference(s): <br>
- [ClawHub Monzo skill](https://clawhub.ai/RHesketh/monzo) <br>
- [Publisher profile](https://clawhub.ai/user/RHesketh) <br>
- [Monzo Developer Portal](https://developers.monzo.com/) <br>
- [Monzo](https://monzo.com) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; scripts emit human-readable text or JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MONZO_KEYRING_PASSWORD and the curl, jq, openssl, and bc command-line tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
