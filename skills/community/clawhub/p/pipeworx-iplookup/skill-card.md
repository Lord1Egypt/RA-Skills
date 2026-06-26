## Description: <br>
IP Lookup MCP - ip-api.com (free, no auth for basic usage). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Pipeworx's remote IP lookup MCP service for single or batch IP geolocation lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried IP addresses are sent to Pipeworx's remote MCP gateway and likely ip-api.com. <br>
Mitigation: Avoid submitting sensitive internal, customer, regulated, or incident-response IP lists unless external processing is approved by the organization. <br>
Risk: Remote IP lookup results can be incomplete or unsuitable for high-assurance decisions. <br>
Mitigation: Review lookup results before using them in operational workflows or customer-facing guidance. <br>


## Reference(s): <br>
- [Pipeworx iplookup homepage](https://pipeworx.io/packs/iplookup) <br>
- [ClawHub skill listing](https://clawhub.ai/brucegutman/pipeworx-iplookup) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill exposes remote MCP tools for geolocate_ip and batch_geolocate.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
