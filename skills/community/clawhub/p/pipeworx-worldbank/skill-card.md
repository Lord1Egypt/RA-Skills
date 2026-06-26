## Description: <br>
Retrieve public World Bank development data such as GDP, population, CO2 emissions, literacy, and mortality rates by country, indicator, and date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up public World Bank country metadata and development indicator time series through Pipeworx-hosted World Bank tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries pass through a third-party Pipeworx gateway. <br>
Mitigation: Use the skill for public World Bank lookups and avoid including sensitive or unrelated private information in prompts or query parameters. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/brucegutman/pipeworx-worldbank) <br>
- [Pipeworx World Bank MCP endpoint](https://gateway.pipeworx.io/worldbank/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and example shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries public World Bank country and indicator data using country codes, indicator codes, and optional date ranges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
