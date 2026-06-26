## Description: <br>
Automate LinkedIn content creation, posting, engagement tracking, and audience growth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpbshhx](https://clawhub.ai/user/mpbshhx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft, post, schedule, and analyze LinkedIn activity through an agent with browser access to a logged-in LinkedIn account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act publicly through a logged-in LinkedIn account without strong per-action approval controls. <br>
Mitigation: Review every post, comment, like target, analytics request, and cron schedule before execution. <br>
Risk: Browser automation may use the user's professional LinkedIn identity and session. <br>
Mitigation: Use a dedicated browser profile when possible and install only when comfortable granting the agent access to that account. <br>
Risk: Packaged metadata differs from the server-resolved release metadata. <br>
Mitigation: Rely on server release metadata for this card and clarify the packaged metadata mismatch with the publisher before high-trust deployment. <br>


## Reference(s): <br>
- [LinkedIn Content Strategy Guide](references/content-strategy.md) <br>
- [LinkedIn Engagement & Growth Tactics](references/engagement.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mpbshhx/linkedin-automator) <br>
- [LinkedIn Feed](https://www.linkedin.com/feed/) <br>
- [LinkedIn Creator Analytics](https://www.linkedin.com/analytics/creator/) <br>
- [LinkedIn News](https://www.linkedin.com/news/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell-script workflow instructions for browser-based LinkedIn actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser access with an active LinkedIn session; scheduling examples assume OpenClaw cron support.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
