## Description: <br>
Get public data from The Ohio State University Content APIs (content.osu.edu) across campus services including bus, buildings, dining, events, academic calendar, libraries, recreation sports, parking, directory, student organizations, athletics, food trucks, and BuckID merchants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sichengchen](https://clawhub.ai/user/sichengchen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, campus data users, and MCP-compatible agents use this skill to fetch and inspect public Ohio State University campus data as JSON or through named MCP tools. It is useful for building OSU data features, answering campus information requests, and retrieving current service data such as parking, events, dining, buildings, buses, and classes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Directory tools can return public information about people affiliated with the university. <br>
Mitigation: Use directory queries only for appropriate campus-information needs and avoid redistributing unnecessary personal details. <br>
Risk: The skill retrieves live public data from content.osu.edu, so availability and response contents can change. <br>
Mitigation: Include the retrieval timestamp when summarizing time-sensitive results and retain raw JSON when exact values matter. <br>
Risk: Direct URL mode can fetch arbitrary http(s) URLs when the helper script is used outside the named service/path mode. <br>
Mitigation: Prefer named MCP tools or the helper script's service/path mode for OSU-only workflows. <br>


## Reference(s): <br>
- [OSU Contents API Reference](references/OSU_API.md) <br>
- [OSU Content API endpoints](references/endpoints.md) <br>
- [OSU MCP Server README](mcp-server/README.md) <br>
- [Ohio State API on ClawHub](https://clawhub.ai/sichengchen/ohio-state-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from public OSU APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include retrieval timestamps and raw JSON summaries; requires outbound internet access to content.osu.edu for live data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
