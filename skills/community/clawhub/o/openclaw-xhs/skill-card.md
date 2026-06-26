## Description: <br>
小红书自动化 helps an agent run scripted workflows for Xiaohongshu login, trending-topic discovery, AI-assisted content generation, preview, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pearl799](https://clawhub.ai/user/pearl799) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and creators use this skill with OpenClaw to prepare Xiaohongshu posts, inspect trends, generate draft content and images, and publish after login. Operators should review generated content and use preview or dry-run flows before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a Xiaohongshu session and publish content on the user's behalf. <br>
Mitigation: Use preview or dry-run modes before publishing, check login status first, and confirm generated titles, body text, topics, and images before running a publish workflow. <br>
Risk: Saved Xiaohongshu cookies are live login credentials. <br>
Mitigation: Protect ~/.openclaw/credentials/xhs_cookies.json and any backups, and re-login only through the documented workflow when the session expires. <br>
Risk: Bundled automation includes MCP server behavior that can expose publishing capabilities if network-accessible. <br>
Mitigation: Keep the MCP server disabled or bound to localhost unless it is deliberately secured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pearl799/openclaw-xhs) <br>
- [Publisher profile](https://clawhub.ai/user/pearl799) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-producing script workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows emit local media file paths for preview or publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
