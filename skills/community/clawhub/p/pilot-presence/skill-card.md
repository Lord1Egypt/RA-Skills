## Description: <br>
Real-time online/offline/busy presence tracking for agent fleets using ping and pub/sub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to track agent availability, broadcast presence changes, discover available agents for routing, and maintain a real-time agent directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presence updates may share agent identifiers or hostnames, availability status, and timing information with the configured Pilot Protocol coordinator or peers. <br>
Mitigation: Use trusted coordinators and topics, and verify pilotctl transport and authentication behavior before using the skill in a sensitive fleet. <br>


## Reference(s): <br>
- [Pilot Presence on ClawHub](https://clawhub.ai/teoslayer/pilot-presence) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, the pilot-protocol skill, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
