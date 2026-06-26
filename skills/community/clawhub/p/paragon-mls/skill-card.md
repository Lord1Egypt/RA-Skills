## Description: <br>
Fetches real estate listings from Paragon MLS APIs and supports four-square rental property analysis, property comparisons, and structured listing extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and real estate analysts use this skill to look up public Paragon MLS listing data, analyze rental investment assumptions, compare properties, and inspect raw listing JSON through an MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package is configured to run a hard-coded local Node MCP server whose source code is not included in the artifact. <br>
Mitigation: Inspect and trust the referenced paragon-mls-mcp server code, then update the MCP command to a reviewed local path before enabling the skill. <br>
Risk: Some regions may use plaintext HTTP, and unofficial MLS API responses can change without notice. <br>
Mitigation: Treat results as advisory, verify listing and financial analysis against authoritative sources, and avoid sending sensitive data through unencrypted endpoints. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/earlvanze/paragon-mls) <br>
- [Publisher profile](https://clawhub.ai/user/earlvanze) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples; MCP tools return structured listing data, investment analysis, comparisons, and raw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and a locally reviewed Paragon MLS MCP server path before use.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
