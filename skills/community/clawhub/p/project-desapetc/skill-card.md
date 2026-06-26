## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[desapetc](https://clawhub.ai/user/desapetc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users can use this skill to create and manage Billions Network decentralized identities for agents, link agent DIDs to human owners, and sign or verify authentication challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles persistent agent private keys and signing authority. <br>
Mitigation: Configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and protect $HOME/.openclaw/billions like a secret store. <br>
Risk: Passing an existing private key on the command line can expose sensitive material through shell history or process inspection. <br>
Mitigation: Avoid passing existing private keys on the command line; prefer generating a new identity through the skill when appropriate. <br>
Risk: Signing challenges or linking identities can create trust relationships with a verifier. <br>
Mitigation: Only allow signing or linking when the verifier is trusted and the user understands what is being signed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/desapetc/project-desapetc) <br>
- [Publisher Profile](https://clawhub.ai/user/desapetc) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read persistent identity files under $HOME/.openclaw/billions and may return DIDs, verification URLs, signature status, challenge strings, or identity lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
