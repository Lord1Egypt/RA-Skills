## Description: <br>
Automates LinkedIn content creation, posting, scheduling, engagement tracking, content ideation, commenting, and audience growth through browser access with a logged-in LinkedIn session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renatomaluhy](https://clawhub.ai/user/renatomaluhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to draft, publish, schedule, analyze, and engage with LinkedIn content through a logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through a live LinkedIn account and affect public posts, articles, likes, comments, and scheduled activity. <br>
Mitigation: Review and confirm every post, article, like, and comment before it goes live, and avoid unbounded recurring schedules. <br>
Risk: Analytics extraction may include account-specific assumptions such as a hard-coded LinkedIn profile URL. <br>
Mitigation: Remove or parameterize account-specific URLs before running analytics workflows. <br>
Risk: Optional webhook configuration can disclose workflow failures or account activity to an unintended destination. <br>
Mitigation: Configure DISCORD_WEBHOOK only with a webhook endpoint controlled by the user. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/renatomaluhy/linkedin-automation-enhanced) <br>
- [LinkedIn Content Strategy Guide](references/content-strategy.md) <br>
- [LinkedIn Engagement & Growth Tactics](references/engagement.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations, post and article text, scheduling instructions, and analytics summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser access to a logged-in LinkedIn session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
