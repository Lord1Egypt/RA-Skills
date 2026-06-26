## Description: <br>
Fetch all active property listings from a Paragon MLS shared listing GUID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real estate and deal-analysis agents use this skill to resolve Paragon MLS share links, GUIDs, or collaboration pages into the active property records behind them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an MCP server from a hard-coded local path outside the reviewed package. <br>
Mitigation: Use it only after inspecting and controlling the local `paragon-mls-mcp` project at that path, then rebuild it from trusted source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earlvanze/paragon-mls-fetch-listings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced MCP tool returns JSON with count and properties[] fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
