## Description: <br>
Coordinates an IceCube-to-Xiaohongshu publishing workflow that drafts diary-style content, adapts it for Xiaohongshu, creates titles and hashtags, and prepares publishing commands through a Xiaohongshu MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ares521521-design](https://clawhub.ai/user/ares521521-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to turn IceCube diary entries into Xiaohongshu-ready posts, including content optimization, titles, hashtags, scheduling guidance, and publishing command preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish through a real Xiaohongshu account using an external MCP service. <br>
Mitigation: Require manual approval for every title, body, image, private-message action, and publish command before execution. <br>
Risk: The artifact downloads and runs an external Xiaohongshu MCP binary and keeps a localhost service active. <br>
Mitigation: Verify the binary and source before installation, monitor the local service, and stop it when publishing work is complete. <br>
Risk: Generated promotional or monetization copy may be inaccurate, noncompliant, or unsuitable for the account audience. <br>
Mitigation: Review content, hashtags, scheduling, and conversion messages against platform rules and account policy before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ares521521-design/icecube-xiaohongshu-flow) <br>
- [Publisher profile](https://clawhub.ai/user/ares521521-design) <br>
- [xiaohongshu-mcp release repository](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and content templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include publishing scripts, content calendars, hashtags, posting records, and MCP service-management commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
