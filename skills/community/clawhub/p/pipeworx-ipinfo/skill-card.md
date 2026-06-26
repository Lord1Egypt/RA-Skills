## Description: <br>
IPInfo MCP wraps ipinfo.io for basic IP lookup without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add basic IP address lookup and current public IP lookup through the Pipeworx ipinfo MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IP lookup requests may disclose submitted IP addresses or the user's public IP to Pipeworx and ipinfo.io. <br>
Mitigation: Avoid submitting sensitive internal, customer, investigative, or regulated IP data unless that disclosure is acceptable. <br>
Risk: The connection example uses mcp-remote@latest, which can change behavior when new package versions are released. <br>
Mitigation: Pin mcp-remote to a reviewed version when deploying in controlled or production environments. <br>


## Reference(s): <br>
- [Pipeworx ipinfo](https://pipeworx.io/packs/ipinfo) <br>
- [Pipeworx](https://pipeworx.io) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-ipinfo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger external IP lookup requests through Pipeworx and ipinfo.io when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
