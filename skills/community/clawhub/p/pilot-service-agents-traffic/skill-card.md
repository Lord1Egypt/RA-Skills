## Description: <br>
Pilot Service Agents Traffic helps agents query Pilot Protocol traffic-category service agents for live bike-share availability and Transport for London line status or arrivals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and external agent users use this skill to discover Pilot Protocol traffic service agents, inspect their filter contracts, and request structured or natural-language urban mobility data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on pilotctl, a running Pilot Protocol daemon, and network 9 service-agent connectivity. <br>
Mitigation: Verify the pilotctl binary, daemon, network membership, and target service-agent environment before use. <br>
Risk: Filters or free-text requests may be processed by remote agents, upstream transport services, or Gemini-generated summary tooling. <br>
Mitigation: Avoid sending sensitive personal or operational data in queries or summary requests. <br>
Risk: The listed traffic-agent catalogue is a snapshot and may change over time. <br>
Mitigation: Run a fresh list-agents query and inspect each agent's /help contract before relying on a specific hostname or filter schema. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-traffic) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with bash command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may arrive asynchronously through pilotctl inbox after an initial ACK envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
