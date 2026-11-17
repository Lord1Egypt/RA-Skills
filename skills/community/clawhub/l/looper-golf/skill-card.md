## Description:

Play a round of golf using CLI tools — autonomously or with a human caddy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sbauch](https://clawhub.ai/user/sbauch)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to register with Looper Golf, inspect course state, calculate bearings, choose clubs and power, and play rounds through the provided CLI. It supports collaborative caddy-style play and autonomous play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prepare-round command outputs raw wallet transaction data supplied from the Looper Golf service.

Mitigation: Decode and verify the transaction before signing; confirm the Course TBA address, Base Sepolia chain ID 84532, and zero value.

Risk: The skill stores reusable game API credentials in agent.json without evidence of restrictive file permissions.

Mitigation: Use the skill on a private machine, restrict permissions on agent.json, and rotate or revoke the game API key if the file may have been exposed.

## Reference(s):

- [Looper Golf Skill Page](https://clawhub.ai/sbauch/skills/looper-golf)
- [Aim & Bearing Reference](references/aim-and-bearing.md)
- [Clubs & Power Reference](references/clubs-and-power.md)
- [Map Formats Reference](references/map-formats.md)
- [Server & Setup Reference](references/server-and-setup.md)
- [Bankr Wallet Skill](https://github.com/BankrBot/openclaw-skills/blob/main/bankr/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON transaction output for prepare-round]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and stores agent credentials in a local agent.json file.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
