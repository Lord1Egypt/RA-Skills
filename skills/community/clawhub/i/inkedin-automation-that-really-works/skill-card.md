## Description: <br>
LinkedIn automation for posting with image uploads, commenting with mentions, editing or deleting comments, reposting, reading feeds, analytics, like monitoring, engagement tracking, and content calendar workflows through Playwright with a persistent browser profile. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[red777777](https://clawhub.ai/user/red777777) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to automate personal LinkedIn productivity tasks, analyze engagement, monitor likes, learn writing style, and manage scheduled content with an approval workflow. Public account actions should be reviewed and approved before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a logged-in LinkedIn browser profile. <br>
Mitigation: Use a dedicated browser profile and require explicit review and approval before posting, commenting, reposting, editing, or deleting content. <br>
Risk: The local content-calendar webhook can alter scheduled public posts if exposed or left unauthenticated. <br>
Mitigation: Avoid running the webhook, cron, or systemd workflow until authentication, restricted CORS, and local network exposure controls are in place. <br>
Risk: Third-party activity collection may create policy or privacy risk. <br>
Mitigation: Avoid third-party activity scraping unless there is a clear permitted basis and the intended use complies with applicable platform terms. <br>


## Reference(s): <br>
- [Content Calendar Integration](references/content-calendar.md) <br>
- [LinkedIn Content Strategy](references/content-strategy.md) <br>
- [LinkedIn DOM Patterns Reference](references/dom-patterns.md) <br>
- [LinkedIn Engagement Guide](references/engagement.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can perform read-only analysis or user-approved LinkedIn account actions through a persistent browser session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
