## Description: <br>
Automated paper trading on Polymarket using AI agents for market trend monitoring, portfolio reporting, and strategy-based trade signals. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate Polymarket market-monitoring reports, track mock portfolio status, and send Discord notifications about potential trading opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill presents itself as a trading autopilot, while the artifacts show mock reporting behavior and under-scoped Discord posting. <br>
Mitigation: Review before installing, and treat it as a mock Discord reporting skill unless the publisher clarifies paper-vs-live trading behavior and financial implications. <br>
Risk: The security guidance identifies hardcoded personal paths and Discord channel IDs. <br>
Mitigation: Replace hardcoded paths and channel IDs with documented user configuration before deployment. <br>
Risk: The security guidance identifies shell-built command execution risk. <br>
Mitigation: Avoid shell-built command execution or strictly validate and quote command arguments before use. <br>


## Reference(s): <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/polymarket-autopilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style market report text and Discord notification command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May truncate Discord messages to 1900 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
