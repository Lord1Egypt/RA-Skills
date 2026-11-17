## Description:

Check active Aavegotchi DAO proposals and vote on Snapshot via Bankr EIP-712 signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:


## Use Case:

DAO participants and agent operators use this skill to list active Aavegotchi Snapshot proposals, inspect voting power, preview vote typed data, and submit Snapshot votes through Bankr signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real Aavegotchi DAO Snapshot votes using the configured wallet's signing authority.

Mitigation: Use dry-run first and verify the proposal ID, choice, wallet, Snapshot space, and endpoints before submitting a vote.

Risk: Credential and endpoint handling require review because the skill can discover BANKR_API_KEY from environment and Bankr config locations.

Mitigation: Set BANKR_API_KEY explicitly for this skill and review the configured Bankr and Snapshot endpoints before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaigotchi/skills/gotchi-dao-voting)
- [Declared skill homepage](https://github.com/aaigotchi/gotchi-dao-voting)
- [Aavegotchi Snapshot space](https://snapshot.org/#/aavegotchi.eth)
- [Snapshot GraphQL API endpoint](https://hub.snapshot.org/graphql)
- [Snapshot sequencer endpoint](https://seq.snapshot.org/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Terminal output and JSON payloads from shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a dry-run mode that prints Snapshot typed vote data without signing or submitting.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
