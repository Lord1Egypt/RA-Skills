## Description: <br>
Performs advanced Google searches with Playwright for OpenClaw technical resources and summarizes results for Telegram channel delivery in Markdown format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonpham1909](https://clawhub.ai/user/sonpham1909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users can use this skill to search for OpenClaw documentation, repositories, and usage guides, then receive a concise Markdown summary through Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs an unreviewed local Python script for web automation. <br>
Mitigation: Inspect or replace the referenced bot.py before installing or executing the skill. <br>
Risk: Search results are forwarded to Telegram, which may expose sensitive query content or summaries. <br>
Mitigation: Confirm the Telegram destination before each send and avoid sensitive queries or account credentials. <br>
Risk: Telegram automation requires credentials that could be misused if overprivileged or exposed. <br>
Mitigation: Use a dedicated low-privilege bot token stored outside the skill artifact. <br>


## Reference(s): <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sonpham1909/google-research-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/sonpham1909) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summary with structured search-result details and optional execution or delivery status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are intended for Telegram delivery and are based on the top 3-5 search results returned by the referenced local Python workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
