## Description: <br>
OpenClaw Xiaohongshu MCP helps agents use a local Xiaohongshu MCP service to search notes, read note details and comments, post comments or replies, and publish image or video content with reusable shell scripts and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomilizhipeng](https://clawhub.ai/user/xiaomilizhipeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and agent users can use this skill to automate Xiaohongshu workflows through a local MCP service, including search, note inspection, commenting, replies, and publishing. It is intended for users who can review generated payloads and operate the linked account responsibly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or comment through a real Xiaohongshu account. <br>
Mitigation: Use a test or least-privilege account where possible, inspect publish and comment payloads before execution, and test new posts with private visibility before making them public. <br>
Risk: The local service persists login state and browser profile data on disk. <br>
Mitigation: Protect the cookie and profile directories, stop the container when work is complete, and delete persisted state when access should be revoked. <br>
Risk: The Docker Compose file references an unpinned third-party image. <br>
Mitigation: Install only after reviewing and trusting the image source, and pin or audit the image before use in controlled environments. <br>


## Reference(s): <br>
- [Setup and persistence notes](references/setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiaomilizhipeng/openclaw-xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON payload examples, and configuration file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local MCP calls that return JSON or text responses from Xiaohongshu workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
