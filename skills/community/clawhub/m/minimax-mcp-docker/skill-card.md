## Description: <br>
MiniMax MCP Docker版（适配极空间） helps an agent use MiniMax-backed image understanding, OCR, and web search through an external MCP package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who want an agent to process images with MiniMax OCR/image understanding or perform web search can use this skill after installing the referenced MCP package and configuring a MiniMax API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user images and search queries to an external MiniMax service for processing. <br>
Mitigation: Avoid sending sensitive images or private search terms unless the user is comfortable with MiniMax processing that content. <br>
Risk: The skill requires a MiniMax API key and includes behavior for storing that key locally. <br>
Mitigation: Use a dedicated MiniMax key with limited exposure and configure it directly in the local credentials file instead of pasting it into chat. <br>
Risk: The skill depends on an external npm package to execute MiniMax MCP commands. <br>
Mitigation: Verify the external package before installation and review the skill before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/minimax-mcp-docker) <br>
- [MiniMax API platform](https://platform.minimaxi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with command examples and returned MCP results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an external MCP package and MiniMax API; image understanding can take 30-60 seconds.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
