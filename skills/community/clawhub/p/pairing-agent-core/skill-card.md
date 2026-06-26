## Description: <br>
Billions decentralized identity for agents that creates and manages DIDs, links agent identities to human owners, and verifies authentication proofs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilhant-34](https://clawhub.ai/user/ilhant-34) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill to create local Billions Network identities, link an agent DID to a human owner, and prove or verify DID ownership with signed challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived identity keys and credential data are stored locally, with plaintext defaults unless encryption is configured first. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, protect $HOME/.openclaw/billions from backups and other local users, and approve each identity creation, signing, or human-linking action explicitly. <br>
Risk: Identity linking and challenge signing can bind an agent DID to a human owner or prove control of a DID. <br>
Mitigation: Check existing identities first, stop on any script failure, and avoid manual cryptographic workarounds or direct edits to $HOME/.openclaw/billions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilhant-34/pairing-agent-core) <br>
- [Billions Network](https://billions.network/) <br>
- [Billions Wallet](https://wallet.billions.network) <br>
- [Billions identity dashboard](https://identity-dashboard.billions.network) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or string command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DID strings, signed challenge results, verification URLs, and identity metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
