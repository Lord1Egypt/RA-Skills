## Description: <br>
Secure multi-account management for NEAR Protocol with encrypted credential storage, account switching, and balance aggregation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, organizations, traders, DeFi users, and advanced NEAR users use this skill to manage multiple NEAR Protocol accounts, switch active accounts, aggregate balances, transfer NEAR, and export or import account metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys for NEAR accounts may be stored by the skill, and the security summary identifies weak wallet-key safeguards. <br>
Mitigation: Use a strong unique NEAR_SKILL_KEY before adding accounts, review the local storage behavior, and avoid storing valuable private keys until the fallback key issue is addressed. <br>
Risk: The skill can initiate NEAR mainnet transfers. <br>
Mitigation: Require explicit human confirmation for transfers and verify the sender, recipient, and amount before invoking transfer actions. <br>
Risk: Unrelated marketplace helper scripts include an exposed authenticated token according to the security guidance. <br>
Mitigation: Remove or ignore those scripts before installation, and have the publisher revoke the exposed token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaiss/near-multi-account-manager) <br>
- [Publisher profile](https://clawhub.ai/user/shaiss) <br>
- [NEAR mainnet explorer](https://explorer.mainnet.near.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [Structured JavaScript object responses with status fields, account summaries, balance data, transfer results, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local encrypted account storage and submit NEAR mainnet transactions when transfer entrypoints are invoked.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
