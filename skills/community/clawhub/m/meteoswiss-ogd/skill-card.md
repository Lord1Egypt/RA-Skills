## Description:

Use when the user asks about Swiss weather, MeteoSwiss data, or Swiss weather forecasts and no MCP server is available; covers current weather, forecasts, pollen, and station discovery via direct HTTP with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eins78](https://clawhub.ai/user/eins78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer Swiss weather questions by fetching MeteoSwiss Open Government Data directly over HTTP. It supports current observations, local forecasts, pollen data, station search, and forecast point discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional third-party MCP server can add remote tools to an agent environment and is not verified or clearly scoped in the security evidence.

Mitigation: Use the bundled scripts or direct data.geo.admin.ch URLs for normal weather lookups; add the MCP server only after intentionally trusting that service.

Risk: Weather lookups depend on live public CSV and STAC endpoints and local command-line tools.

Mitigation: Check script errors, validate station or point identifiers from metadata, and ensure curl, awk, iconv, and jq are available before relying on forecast output.

## Reference(s):

- [MeteoSwiss Open Data Skill Page](https://clawhub.ai/eins78/skills/meteoswiss-ogd)
- [Official MeteoSwiss Open Data Documentation](https://opendatadocs.meteoswiss.ch/)
- [MeteoSwiss STAC API](https://data.geo.admin.ch/api/stac/v1)
- [MeteoSwiss LLM Tools Repository Metadata](https://github.com/eins78/meteoswiss-llm-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and key=value script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public MeteoSwiss CSV and STAC endpoints; bundled scripts require curl, awk, iconv, and jq for forecasts.]

## Skill Version(s):

1.0.0-rc.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
