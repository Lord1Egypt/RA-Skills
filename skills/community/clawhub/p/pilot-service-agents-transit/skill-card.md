## Description: <br>
Public-transit schedules and live data for Amtrak, BART, Deutsche Bahn, Swiss SBB, BC Ferries, BVG Berlin, and other transit services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and external users use this skill to discover transit service agents, read each agent's query contract, and fetch live departures, station metadata, ferry capacity, or multi-modal journey data through Pilot Protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends transit queries through Pilot Protocol over a remote overlay network. <br>
Mitigation: Install only when Pilot Protocol and the pilotctl daemon are trusted, and review remote-query behavior before deployment. <br>
Risk: The artifact lists bike-share entries even though its own scope directs bike-share use to a separate traffic skill. <br>
Mitigation: Treat bike-share coverage as ambiguous and use the intended traffic skill for city bike-share unless the publisher clarifies the scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-transit) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward read-only transit queries whose results may include plain text help, ACK envelopes, normalized JSON inbox data, or prose summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
