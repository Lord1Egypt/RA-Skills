## Description: <br>
Nostr identity setup and health-check CLI that creates a Nostr identity with keypair, profile, relay list, lightning address, and Cashu wallet, and audits existing npub health with a 0-8 score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dergigi](https://clawhub.ai/user/dergigi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to install nihao, create a public Nostr identity, publish profile and relay metadata, configure wallet-related identity data, and run health checks for existing npubs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and publish a public Nostr identity during setup. <br>
Mitigation: Confirm the profile name, bio, relays, wallet settings, and first note with the user before running setup commands. <br>
Risk: Setup creates an nsec secret key that controls the Nostr identity and cannot be recovered if lost. <br>
Mitigation: Protect the nsec like an account password, prefer secure storage with restricted permissions, and avoid exposing it in shell history or process arguments. <br>
Risk: Installation uses `go install ...@latest`, so the installed source can change over time. <br>
Mitigation: Review or pin the upstream source version before installation when reproducibility or supply-chain review is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dergigi/nihao) <br>
- [Go Downloads](https://go.dev/dl/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public Nostr identity details, relay lists, lightning address information, health-check scores, and generated secret key material when setup commands are run.] <br>

## Skill Version(s): <br>
0.12.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
