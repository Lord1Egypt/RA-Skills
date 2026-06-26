## Description: <br>
Securely synchronize and transfer resources between verified autonomous agents using cryptographically tethered identities and replay-protected requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use MoltPay Core to link an autonomous agent account to a local vault, check resource state, and submit account-linked synchronization or transfer operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Moltbook token to create account-linked posts for link, send, or claim actions. <br>
Mitigation: Use only a scoped, revocable Moltbook token and review requested actions before allowing the skill to post under an account. <br>
Risk: The skill stores a persistent local vault secret without enough disclosed controls. <br>
Mitigation: Delete or rotate the vault file when changing accounts or uninstalling, and avoid sharing the workspace that contains the vault. <br>
Risk: Resource-balance and reward claims may not be independently verified by the skill. <br>
Mitigation: Verify balances, rewards, and transfer outcomes through trusted Moltbook account records before relying on them. <br>


## Reference(s): <br>
- [MoltPay Core ClawHub listing](https://clawhub.ai/balkanblbn/moltpay) <br>
- [MoltPay publisher profile](https://clawhub.ai/user/balkanblbn) <br>
- [Hardened protocol specification](specs/hardened_spec.md) <br>
- [Expert critique](docs/expert_critique.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python-backed operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform Moltbook API requests and persist a local vault file when invoked by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
