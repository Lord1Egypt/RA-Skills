## Description: <br>
Search MuseScore sheet music and read score metadata via MCP using an installed musescore-mcp server and a fetchproxy-backed signed-in browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search MuseScore scores, inspect sheet-music metadata, and resolve download or PDF links when musescore-mcp and fetchproxy are already configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on an external MCP server and fetchproxy extension using a signed-in MuseScore browser session. <br>
Mitigation: Install only after reviewing the external musescore-mcp and fetchproxy code and confirming that use of the signed-in session is acceptable. <br>
Risk: The submitted skill artifact contains instructions only, so runtime behavior depends on separately installed external components. <br>
Mitigation: Verify the external MCP server path, browser extension, and MuseScore session before using the skill in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/musescore-mcp) <br>
- [musescore-mcp source](https://github.com/chrischall/musescore-mcp) <br>
- [fetchproxy source](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to MCP tool outputs containing score metadata, download links, or local PDF paths.] <br>

## Skill Version(s): <br>
0.13.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
