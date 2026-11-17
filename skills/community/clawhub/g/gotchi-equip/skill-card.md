## Description:

Equip, unequip, and inspect Aavegotchi wearables on Base via Bankr submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT

## Use Case:

External Aavegotchi users and agent operators use this skill to inspect current wearable loadouts and submit equip or unequip transactions for Gotchi NFTs on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Bankr API key to submit transactions.

Mitigation: Use a scoped or rotatable Bankr key and avoid exposing it in logs, prompts, or shared environments.

Risk: Equip and unequip commands can change on-chain wearable state for a Gotchi.

Mitigation: Verify the Gotchi ID, slot names, wearable IDs, and unequip-all intent before running transaction-submitting commands.

Risk: The skill depends on external Goldsky and Bankr services.

Mitigation: Check command output and transaction responses before relying on results or repeating submissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaigotchi/skills/gotchi-equip)
- [Publisher profile](https://clawhub.ai/user/aaigotchi)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Terminal output, shell command usage, and JSON transaction responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, jq, curl, and a Bankr API key; queries a Goldsky subgraph and submits wearable transactions through Bankr.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
