## Description: <br>
Poetry MCP - PoetryDB API (free, no auth). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to Pipeworx's PoetryDB MCP gateway for poem search, author lookup, and random poem retrieval without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent to the remote PoetryDB MCP gateway may be processed outside the local agent environment. <br>
Mitigation: Avoid sending private or sensitive text through the MCP server unless the remote service is acceptable for the deployment. <br>
Risk: Using mcp-remote@latest delegates package selection to the latest published version at install time. <br>
Mitigation: Pin the mcp-remote package version when stronger supply-chain control or repeatable installs are required. <br>


## Reference(s): <br>
- [Pipeworx Poetry](https://pipeworx.io/packs/poetry) <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-poetry) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown or text responses, with JSON MCP configuration when setup instructions are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns poetry lookup results through a remote MCP gateway; no API key is required by the submitted skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
