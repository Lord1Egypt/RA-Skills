## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louise2364](https://clawhub.ai/user/louise2364) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, external users, and agent operators use this skill to create and manage Billions Network decentralized identities, link an agent identity to a human owner, sign challenges, and verify DID ownership proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys are handled by the skill and may be stored locally. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities so keys are encrypted at rest. <br>
Risk: Signing challenges or creating human-agent linking URLs can assert identity ownership. <br>
Mitigation: Require clear human approval before running commands that sign challenges or create linking URLs. <br>
Risk: Supplying an existing valuable wallet private key with --key increases exposure if the local environment is compromised. <br>
Mitigation: Avoid using valuable wallet private keys with --key; prefer a new purpose-specific identity key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/louise2364/ntala-ai-2047) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local identity data under $HOME/.openclaw/billions when the user runs the documented scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
