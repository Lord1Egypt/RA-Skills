## Description: <br>
Analyze images and search the web using MiniMax MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daowuu](https://clawhub.ai/user/daowuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call MiniMax MCP tools for image understanding and web search from local scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, search prompts, and Telegram-saved media may include confidential content that is processed by MiniMax or stored locally. <br>
Mitigation: Use only inputs approved for provider processing and delete locally saved Telegram images when they are no longer needed. <br>
Risk: The MiniMax API key can be exposed if it is stored broadly in shell startup files or shared logs. <br>
Mitigation: Store the API key in a restricted environment or secret manager and avoid printing or committing it. <br>
Risk: The skill executes a MiniMax MCP package through uvx, so runtime behavior depends on the package source. <br>
Mitigation: Install and run it only when MiniMax and the uvx package source are trusted for the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daowuu/minimax-vision-search) <br>
- [Project Homepage](https://github.com/daowuu/minimax-vision-search) <br>
- [MiniMax MCP Guide](https://platform.minimaxi.com/docs/token-plan/mcp-guide) <br>
- [Setup Guide](references/setup.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text or JSON returned by MiniMax MCP tools, with setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uvx and MINIMAX_API_KEY; MINIMAX_API_HOST can override the default MiniMax API host.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
