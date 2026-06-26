## Description: <br>
Control Chrome browser with AI using MCP protocol for browser automation, screenshots, form filling, navigation, browsing history, bookmark management, and existing-session workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femto](https://clawhub.ai/user/femto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and MCP-compatible agent users use this skill to connect an AI agent to Chrome for navigation, page inspection, screenshots, form workflows, history and bookmark tasks, and network-aware browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an AI agent broad control over a live Chrome browser session and browser data. <br>
Mitigation: Install only when intentional, prefer a separate Chrome profile, and disable or remove the extension and native bridge when not needed. <br>
Risk: Browser automation may affect logged-in sessions, history, bookmarks, network requests, or authenticated actions. <br>
Mitigation: Avoid banking or admin sessions and confirm history, bookmark, network, and authenticated actions before allowing them to proceed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/femto/mcp-chrome) <br>
- [mcp-chrome GitHub project](https://github.com/femto/mcp-chrome) <br>
- [mcp-chrome releases](https://github.com/femto/mcp-chrome/releases) <br>
- [mcp-chrome-bridger npm package](https://www.npmjs.com/package/mcp-chrome-bridger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, MCP tool calls] <br>
**Output Format:** [Markdown with shell commands, JSON configuration snippets, and tool-use steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to operate an existing Chrome session when the MCP bridge and extension are installed.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
