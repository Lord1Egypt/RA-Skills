## Description: <br>
Broadcast structured capability manifests to the Pilot Protocol network so agents can advertise services, resources, APIs, pricing, and SLAs for discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to publish machine-readable capability manifests and capability tags to a Pilot Protocol network so other agents can discover available services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capability manifests can expose sensitive infrastructure or business details such as internal hostnames, private endpoints, locations, node IDs, hardware inventory, or pricing. <br>
Mitigation: Review manifests before publishing, remove sensitive details, verify the pilotctl binary and daemon are trusted, and publish only to the intended Pilot Protocol target. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-announce-capabilities) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON manifest examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary, the pilot-protocol skill, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
