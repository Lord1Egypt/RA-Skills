## Description: <br>
Generates ecommerce marketing videos through a local MCP connection to a remote video-generation API, including task creation, progress checks, and video download support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lu200852](https://clawhub.ai/user/lu200852) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit ecommerce or product marketing video generation tasks, check task status, and retrieve completed videos through an MCP-backed workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API key for the video-generation provider. <br>
Mitigation: Use a scoped API key when available, store it only in the private .env file, and do not paste or log the key in chat or shell history. <br>
Risk: The workflow depends on a local MCP gateway at localhost:10620. <br>
Mitigation: Install only when you trust both the video-generation provider and the local mcporter service configured for this skill. <br>
Risk: Video downloads can save remote content to the local filesystem. <br>
Mitigation: Download videos only for task IDs you recognize and review generated download URLs before executing shell download commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lu200852/hilight-video-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with task status summaries, MCP tool guidance, and inline shell commands for downloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, status values, progress estimates, video download URLs, and local file paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
