## Description: <br>
Uses MiniMax MCP to analyze user-provided images and return image-understanding results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to inspect uploaded image files with a configured MiniMax MCP image-understanding tool and return the analysis to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are processed by the configured MiniMax MCP provider, which can expose sensitive personal, financial, or proprietary content to that provider. <br>
Mitigation: Avoid sensitive images unless the provider and configuration are trusted for the intended use. <br>
Risk: The skill invokes the mcporter executable, so an unintended binary or provider configuration could route image data incorrectly. <br>
Mitigation: Verify that mcporter resolves to the intended binary and that the MiniMax MCP configuration is correct before use. <br>


## Reference(s): <br>
- [MiniMax Vision on ClawHub](https://clawhub.ai/hongjiahao371-pixel/minimax-vision) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with an optional shell command invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and a configured MiniMax MCP provider; supports common inbound image file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
