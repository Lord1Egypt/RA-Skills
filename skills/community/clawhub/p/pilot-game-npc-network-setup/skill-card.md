## Description: <br>
Deploys a four-agent Pilot Protocol NPC village where villager, merchant, guard, and narrative-director agents communicate autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game developers and agent operators use this skill to configure a four-agent NPC network for emergent village behavior, dynamic economy events, threat reporting, and story orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup depends on external pilot-* skills and the pilotctl binary. <br>
Mitigation: Review the external skills and pilotctl source before installation. <br>
Risk: NPC agents communicate over port 1002. <br>
Mitigation: Restrict port 1002 to the intended network and endpoints you control. <br>
Risk: The setup can persist local state in ~/.pilot/setups/game-npc-network.json. <br>
Mitigation: Remove ~/.pilot/setups/game-npc-network.json when persistent setup state is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-game-npc-network-setup) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation of related pilot-* skills, hostnames, trust handshakes, event topics, and local setup state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
