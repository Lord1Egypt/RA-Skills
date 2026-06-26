## Description: <br>
Primary-source scientific and research APIs for earthquakes, molecules, space weather, particle physics, volcanoes, and related research datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research teams use this skill to discover and query Pilot Protocol science service agents for scientific observations, chemistry data, open research datasets, and natural-event streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to remote Pilot Protocol service agents through a local pilotctl and daemon setup. <br>
Mitigation: Use only with a trusted Pilot Protocol installation and avoid sending secrets or sensitive data in queries. <br>
Risk: The documented science category overlaps with literature and citation-oriented agents that the artifact says belong under an academic skill. <br>
Mitigation: Verify the selected agent with list-agents and /help before relying on category-specific behavior. <br>
Risk: The artifact and server evidence disagree on the release license. <br>
Mitigation: Confirm the authoritative license before publication or downstream redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-science) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, text] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote service-agent responses may arrive asynchronously through pilotctl inbox and can include normalized JSON envelopes or prose summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
