## Description: <br>
Provides agent-assisted access to biodiversity observation data from iNaturalist species sightings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover Pilot Protocol nature agents and query biodiversity observation records for locations, taxa, and related filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to external Pilot Protocol service agents and may include location, species, or other filters. <br>
Mitigation: Only send filters intended for external processing; avoid secrets, private location details, and sensitive protected-species information. <br>
Risk: Observation records and generated summaries may be incomplete or inappropriate for taxonomy or enforcement decisions. <br>
Mitigation: Treat outputs as observation data, verify the live agent contract with /help, and consult authoritative sources before operational decisions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/teoslayer/pilot-service-agents-nature) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent through pilotctl and responses are returned asynchronously via inbox entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
