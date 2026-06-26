## Description: <br>
Live sports scores, fixtures, and historical stats for MLB, NFL, NHL, NBA, Formula 1, cricket, and generic TheSportsDB sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover Pilot Protocol sports data agents, inspect each agent's filter contract, and request public score, schedule, standings, and sports metadata snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to remote overlay agents and may include user-supplied filters or prompts. <br>
Mitigation: Avoid sending private, sensitive, or confidential information through filters, prompts, or free-text requests. <br>
Risk: Summary and free-text features may return Gemini-generated prose that can be incomplete or inaccurate. <br>
Mitigation: Use structured data responses for factual checks and review generated summaries before relying on them. <br>
Risk: The skill depends on a trusted Pilot Protocol daemon, pilotctl installation, and reachable overlay agents. <br>
Mitigation: Install only in trusted Pilot Protocol environments and verify the daemon, network membership, and target agent contract before use. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-sports) <br>
- [Pilot Skills index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Pilot Protocol agents to return ACK envelopes followed by inbox responses containing normalized sports data; summary and free-text responses may be Gemini-generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
