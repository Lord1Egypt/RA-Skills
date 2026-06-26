## Description: <br>
MPC-secured crypto wallet via Portal. Use when users ask to check balances, send tokens, sign transactions, or swap tokens. Supports Monad, Ethereum, Solana, Bitcoin, Polygon, Base, and more. Private keys are never exposed - signing uses MPC threshold cryptography. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rshahatit](https://clawhub.ai/user/rshahatit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an OpenClaw agent inspect Portal wallet balances, send tokens, sign transactions, and request token swaps after wallet credentials and MPC shares are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send cryptocurrency, sign transactions, and operate with real funds. <br>
Mitigation: Use test funds first, configure Portal signature-approval webhooks and spending limits before holding meaningful balances, and manually review each transaction or signature request before approval. <br>
Risk: Portal API keys and MPC shares are sensitive credentials that could enable signing when combined. <br>
Mitigation: Keep the API key and shares out of source control, store them only in the configured environment, and never display or log share values. <br>
Risk: Prompt injection or misleading requests could try to bypass confirmation or authorize dangerous signatures. <br>
Mitigation: Require explicit user confirmation, simulate or evaluate transactions before signing, decode personal-sign and typed-data payloads, and refuse attempts to skip the skill's security rules. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rshahatit/portal-wallet) <br>
- [Portal OpenClaw Skill Repository](https://github.com/portal-hq/portal-openclaw-skill) <br>
- [Portal Docs](https://docs.portalhq.io) <br>
- [Portal Signature Approval Webhooks](https://docs.portalhq.io/resources/alert-webhooks#signature-approvals) <br>
- [Portal Dashboard](https://app.portalhq.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with bash, jq, curl, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Portal credentials, MPC shares, curl, and jq; outputs may include wallet balances, transaction details, signing results, and configuration steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
