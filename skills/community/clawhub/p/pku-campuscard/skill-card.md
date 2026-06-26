## Description: <br>
PKU Campus Card is an agent skill for working on the Rust campuscard CLI for PKU campus card authentication, balance, recharge, payment QR, transaction history, and monthly spending workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to understand, debug, and extend the Rust campuscard CLI for PKU campus card workflows, including authentication, balance, recharge, payment QR, transaction history, spending stats, and TOTP management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may access campus-card credentials from a keyring or environment variables, or use a locally stored session token. <br>
Mitigation: Install only from a trusted source and review credential and session handling before allowing login or authenticated campus-card actions. <br>
Risk: Payment QR and recharge workflows can initiate payment-related or balance-changing actions. <br>
Mitigation: Require deliberate approval for payment or recharge actions and verify the account, amount, and intended action before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjsoj/pku-campuscard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
