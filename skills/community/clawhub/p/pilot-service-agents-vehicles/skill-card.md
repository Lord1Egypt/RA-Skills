## Description: <br>
Provides agent guidance for querying NHTSA vehicle records, including VIN decoding, makes, models, recalls, and consumer complaints through Pilot Protocol service agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and operators use this skill to discover Pilot Protocol vehicle service agents, read each agent's filter contract, and query NHTSA-style vehicle data such as VIN details, recalls, models, and complaints. <br>

### Deployment Geography for Use: <br>
Global; data coverage is focused on United States NHTSA records. <br>

## Known Risks and Mitigations: <br>
Risk: VINs and vehicle queries are sent to remote Pilot Protocol service agents. <br>
Mitigation: Use only trusted agents and networks, and avoid sending sensitive or unnecessary vehicle information. <br>
Risk: The skill depends on the pilotctl binary, a running daemon, and network 9 membership. <br>
Mitigation: Install pilotctl and join the network only from trusted Pilot Protocol sources before running commands. <br>
Risk: The /summary command produces Gemini-generated prose for submitted filters. <br>
Mitigation: Use /data for structured lookup results when possible, and avoid /summary for information that should not be processed by the summary provider. <br>
Risk: Service-agent catalog entries and filter contracts can change over time. <br>
Mitigation: Run a fresh list-agents query and send /help to the target agent before relying on a query schema. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-vehicles) <br>
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return an immediate ACK; the actual agent response is read later with pilotctl --json inbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
