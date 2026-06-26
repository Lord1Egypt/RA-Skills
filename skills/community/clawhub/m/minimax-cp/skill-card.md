## Description: <br>
Uses the MiniMax Coding Plan API for web search and image understanding through command-line wrappers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MirrorProMax](https://clawhub.ai/user/MirrorProMax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web for current information and analyze or describe images with MiniMax tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a reusable MiniMax API key. <br>
Mitigation: Require users to provide their own MINIMAX_API_KEY and avoid publishing shared credentials. <br>
Risk: The skill runs an unpinned external minimax-coding-plan-mcp package. <br>
Mitigation: Pin and review the MCP dependency before installation or execution. <br>
Risk: Searches, prompts, image URLs, and possibly image contents are sent to MiniMax. <br>
Mitigation: Avoid sending sensitive data unless the user has reviewed and accepted the MiniMax credential and data-handling arrangement. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MirrorProMax/minimax-cp) <br>
- [Publisher Profile](https://clawhub.ai/user/MirrorProMax) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text returned from command-line scripts, with usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries, prompts, image URLs, and image content may be sent to MiniMax services.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
