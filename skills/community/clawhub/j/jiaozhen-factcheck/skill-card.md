## Description: <br>
Fact-checking tool for verifying the factual accuracy of input statements or suspicious claims, identifying rumors, and returning a verification conclusion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check claims, news items, events, common-knowledge statements, or suspected rumors through Tencent News' Jiaozhen fact-checking CLI. It can guide environment setup, API-key configuration, and fact-check command selection before returning the CLI's Markdown result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update a local CLI from remote CDN-hosted scripts. <br>
Mitigation: Install only when Tencent News and the CDN-hosted installer are trusted; inspect or verify installer scripts before running them. <br>
Risk: The skill reads and changes API-key state for the Tencent News CLI. <br>
Mitigation: Treat the API key as a secret and avoid pasting it into chats, logs, screenshots, or shared terminals. <br>
Risk: An unexpected CLI path could run if multiple installations exist. <br>
Mitigation: Use the skill's state-check script to confirm which CLI path will execute before running fact-checking commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencentnewsteam/jiaozhen-factcheck) <br>
- [API key setup guide](references/env-setup-guide.md) <br>
- [Installation guide](references/installation-guide.md) <br>
- [Update guide](references/update-guide.md) <br>
- [Tencent News API key page](https://news.qq.com/exchange?scene=appkey) <br>
- [Jiaozhen AI fact-checking site](https://view.inews.qq.com/ai/agent/UTR2025041800262600?no-redirect=1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with CLI output and inline shell or PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill preserves the fact-checking CLI's structured Markdown result, including conclusions, process details, confidence assessment, and source links.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
