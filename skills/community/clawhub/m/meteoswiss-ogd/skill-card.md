## Description: <br>
Access MeteoSwiss Open Government Data for Swiss current weather, forecasts, pollen, and station discovery via direct HTTP when no MCP server is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eins78](https://clawhub.ai/user/eins78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill through an agent to answer Swiss weather questions, retrieve MeteoSwiss current conditions, forecasts, and pollen data, and discover valid stations or forecast points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause the agent to make outbound HTTP requests to public MeteoSwiss data endpoints. <br>
Mitigation: Install only when outbound public weather-data access is acceptable, and review proposed network commands before execution. <br>
Risk: The optional MCP-server alternative adds a persistent third-party remote service to the agent configuration. <br>
Mitigation: Use the direct HTTP workflow for normal use; add the MCP server only intentionally and confirm how to remove it later. <br>


## Reference(s): <br>
- [MeteoSwiss Open Data Documentation](https://opendatadocs.meteoswiss.ch/) <br>
- [MeteoSwiss STAC API](https://data.geo.admin.ch/api/stac/v1) <br>
- [MeteoSwiss Current Weather CSV](https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv) <br>
- [Skill Reference](REFERENCE.md) <br>
- [Metadata Repository Link](https://github.com/eins78/meteoswiss-llm-tools) <br>
- [ClawHub Skill Page](https://clawhub.ai/eins78/meteoswiss-ogd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and key=value script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use curl, awk, iconv, and jq; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0-rc.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
