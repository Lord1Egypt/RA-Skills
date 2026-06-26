## Description: <br>
Provides country, state, and city data including ISO codes, capitals, phone codes, currencies, and regions through the Pipeworx CountryStateCity MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a CountryStateCity MCP service for country, state, and city lookup tasks. It is useful when an agent needs normalized location data such as ISO codes, capitals, phone codes, currencies, regions, states, provinces, and city lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Country, state, and city lookup queries are sent to the external Pipeworx gateway. <br>
Mitigation: Confirm that the Pipeworx gateway is trusted before installing or routing lookup requests through the service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-country-state-city) <br>
- [Pipeworx CountryStateCity MCP Endpoint](https://gateway.pipeworx.io/country-state-city/mcp) <br>
- [CountryStateCity API](https://api.countrystatecity.in/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only lookup guidance and MCP server configuration for country, state, and city queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
