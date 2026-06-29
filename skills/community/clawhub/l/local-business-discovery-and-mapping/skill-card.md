## Description: <br>
Local Business Discovery and Mapping helps agents search for nearby places, run text-based place searches, and convert between addresses and coordinates through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover local businesses and services, find places by category or text query, and geocode or reverse-geocode locations for travel, dining, healthcare, retail, routing, and market research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location searches can expose sensitive home, workplace, medical, or other personal-location context. <br>
Mitigation: Ask for explicit user intent before sending sensitive locations and keep lookup inputs limited to the minimum needed for the task. <br>
Risk: AgentPMT account, wallet, payment, or API credentials could be exposed if included in prompts or logs. <br>
Mitigation: Use the setup skills for credential handling and keep account secrets, wallet private keys, mnemonics, signatures, and payment headers out of prompts and logs. <br>


## Reference(s): <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/local-business-discovery-and-mapping) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/local-business-discovery-and-mapping) <br>
- [Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API Calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response handling examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces action guidance for geocode, nearby_search, reverse_geocode, and text_search calls; tool responses are JSON from AgentPMT and Google Maps-backed lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
