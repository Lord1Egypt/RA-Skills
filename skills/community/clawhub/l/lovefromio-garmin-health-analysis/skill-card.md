## Description: <br>
Queries Garmin Connect health, activity, sleep, recovery, route, and body metrics, then helps agents return analysis, JSON data, downloadable activity files, and interactive HTML dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to connect Garmin Connect account data to a ClawHub or Clawdbot agent for health trend analysis, activity lookup, recovery interpretation, route/file inspection, and dashboard generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a populated config.json and the skill requires Garmin credentials. <br>
Mitigation: Delete the included config.json before use and provide only your own credentials through a trusted secret path such as the configured environment or Clawdbot skill settings. <br>
Risk: Command-line passwords and saved Garmin session tokens can expose account access. <br>
Mitigation: Avoid command-line password arguments where possible, protect the local token file, and periodically remove or rotate saved Garmin tokens. <br>
Risk: Skill outputs may contain sensitive health, identity, and GPS route data. <br>
Mitigation: Review generated analysis, JSON, downloaded files, and dashboards before sharing them or storing them in broader agent logs. <br>
Risk: Generated browser charts may introduce third-party CDN or browser exposure. <br>
Mitigation: Avoid chart generation, or review and adapt the chart assets locally, when that exposure is not acceptable. <br>
Risk: Python dependencies are installed into the runtime environment. <br>
Mitigation: Use a virtual environment and review dependency versions before installation. <br>


## Reference(s): <br>
- [Garmin Connect API Reference (Unofficial)](references/api.md) <br>
- [Health Data Analysis Guide - Garmin Edition](references/health_analysis.md) <br>
- [Extended Garmin Capabilities](references/extended_capabilities.md) <br>
- [MCP Server for Standard Claude Desktop](references/mcp_setup.md) <br>
- [python-garminconnect library](https://github.com/cyberjunky/python-garminconnect) <br>
- [Garmin Connect](https://connect.garmin.com) <br>
- [ClawHub skill page](https://clawhub.ai/lovefromio/lovefromio-garmin-health-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command output, and generated HTML dashboards or downloaded activity files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Garmin credentials and locally stored session tokens; generated outputs may contain sensitive health, identity, and GPS route data.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata; artifact frontmatter and _meta.json remain 1.2.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
