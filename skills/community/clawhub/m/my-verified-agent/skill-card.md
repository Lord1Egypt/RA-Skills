## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karan9074](https://clawhub.ai/user/karan9074) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions Network DIDs, link an agent identity to a human owner, sign challenges, and verify identity proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived identity keys can be stored locally in plaintext if encryption is not configured. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and protect $HOME/.openclaw/billions. <br>
Risk: Signing or linking requests can authorize sensitive identity actions. <br>
Mitigation: Require explicit user intent before signing challenges or linking a human identity to an agent DID. <br>
Risk: Imported wallet keys may expose valuable credentials to local skill storage. <br>
Mitigation: Avoid importing valuable wallet private keys with --key; prefer generating a dedicated agent identity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/karan9074/my-verified-agent) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, or verify DID identity data and signed challenges through Node.js scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
