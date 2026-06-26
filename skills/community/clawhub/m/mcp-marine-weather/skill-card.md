## Description: <br>
Marine weather forecasts via NOAA api.weather.gov for current conditions, multi-day forecasts, and marine weather warnings without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haveblue997](https://clawhub.ai/user/haveblue997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add NOAA marine weather lookup for sailing, charter planning, offshore activity checks, coastal event assessment, and pre-departure weather briefings. <br>

### Deployment Geography for Use: <br>
United States and U.S. territories <br>

## Known Risks and Mitigations: <br>
Risk: A floating npx install can resolve a different package version over time. <br>
Mitigation: Confirm the exact npm package name and pin a reviewed version before installation. <br>
Risk: Latitude and longitude queries are sent to NOAA weather services for forecast lookup. <br>
Mitigation: Avoid entering sensitive location data unless an external NOAA lookup is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/haveblue997/mcp-marine-weather) <br>
- [NOAA Weather API](https://api.weather.gov) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON returned as MCP text content, with Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast output includes conditions, forecast periods, and filtered marine-relevant warnings for latitude and longitude inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
