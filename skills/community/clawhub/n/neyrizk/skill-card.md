## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carolin3-neyzr](https://clawhub.ai/user/carolin3-neyzr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to create and manage Billions Network decentralized identities, link an agent DID to a human owner, sign authentication challenges, and verify DID ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local identity keys and may store private key material without at-rest encryption when BILLIONS_NETWORK_MASTER_KMS_KEY is not set. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities, keep the master key secret, and avoid importing funded or high-value wallet keys. <br>
Risk: Signing a challenge is an authentication action that can link or prove control of an identity. <br>
Mitigation: Review each challenge before signing, check that an intended identity already exists, and stop on script errors instead of attempting manual cryptographic workarounds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carolin3-neyzr/neyrizk) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local DID records, signed challenge results, verification URLs, and identity verification status; some commands persist data under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
