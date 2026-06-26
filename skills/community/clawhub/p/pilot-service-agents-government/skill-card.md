## Description: <br>
Provides government and civic data access across the Federal Register, FBI wanted persons, elections information, and national open-data portals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and query Pilot Protocol service agents for government, civic, regulatory, weather, spending, and public-data sources. It helps agents construct pilotctl commands, inspect each remote agent's filter contract, and retrieve structured or summarized public data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filters, free-text queries, and summary requests are sent to remote Pilot Protocol service agents. <br>
Mitigation: Avoid sending secrets or sensitive personal information, and review query payloads before execution. <br>
Risk: The skill depends on an externally installed pilotctl binary and a trusted Pilot Protocol daemon. <br>
Mitigation: Install and use this skill only when the Pilot Protocol environment and pilotctl binary are already trusted. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-government) <br>
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and reachable service agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
