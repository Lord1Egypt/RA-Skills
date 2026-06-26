## Description: <br>
Play a round of golf using CLI tools - autonomously or with a human caddy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sbauch](https://clawhub.ai/user/sbauch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to register a golf agent, resume Looper rounds, inspect hole state, calculate bearings, choose shots, and play with either autonomous or human-caddy decision flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI contacts the Looper API and stores a local game agent credential. <br>
Mitigation: Install only if you trust the Looper service, and keep agent.json private and out of shared folders or source control. <br>
Risk: The prepare-round command can produce raw EVM transaction data for wallet submission. <br>
Mitigation: Before submitting, verify the destination address, chainId 84532, and value 0. <br>


## Reference(s): <br>
- [Aim & Bearing Reference](references/aim-and-bearing.md) <br>
- [Clubs & Power Reference](references/clubs-and-power.md) <br>
- [Map Formats Reference](references/map-formats.md) <br>
- [Server & Setup Reference](references/server-and-setup.md) <br>
- [Looper API](https://api.playlooper.xyz) <br>
- [Bankr Wallet Skill](https://github.com/BankrBot/openclaw-skills/blob/main/bankr/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and occasional JSON transaction data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and writes local agent state to agent.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
