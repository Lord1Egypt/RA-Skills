## Description: <br>
Billions decentralized identity for agents that links agents to human identities using Billions ERC-8004 and Attestation Registries, verifies and generates authentication proofs, and uses the iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Meverylucky](https://clawhub.ai/user/Meverylucky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions Network decentralized identities, sign and verify authentication challenges, and link an agent identity to a human owner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages long-lived private keys for decentralized identities. <br>
Mitigation: Install it only for agents that should manage a real identity, set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities, and protect $HOME/.openclaw/billions. <br>
Risk: Passing an existing wallet private key on the command line may expose sensitive material through shell history or process inspection. <br>
Mitigation: Avoid command-line private key input and prefer creating a new identity with protected local key storage. <br>
Risk: A third-party identity skill can affect trust in agent ownership claims. <br>
Mitigation: Verify the publisher profile, package version, and release context before trusting the skill with identity keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Meverylucky/meveryluckyagent) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local identity files under $HOME/.openclaw/billions when its scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
