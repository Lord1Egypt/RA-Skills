## Description: <br>
Resilient MCP proxy for Google Stitch with auto-retry, token refresh, and TCP drop recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choihyunsus](https://clawhub.ai/user/choihyunsus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and design engineers use this skill to configure an MCP server that connects agents to Google Stitch for project management, screen generation, screen editing, design variants, and generation-status tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marked the release suspicious because it runs an unpinned npm server with Google credentials and create/edit authority. <br>
Mitigation: Install only if the npm or GitHub publisher is trusted, pin a specific n2-stitch-mcp version, and require confirmation before allowing create or edit actions on important Stitch content. <br>
Risk: Google credentials or API keys may be exposed through shared MCP configuration or agent transcripts. <br>
Mitigation: Use a dedicated least-privilege Google credential or API key and avoid placing secrets in shared configuration or transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/choihyunsus/n2-stitch-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/choihyunsus) <br>
- [NPM package](https://www.npmjs.com/package/n2-stitch-mcp) <br>
- [Project website](https://nton2.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke an unpinned npm MCP server that uses Google credentials and can create or edit Stitch content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
