## Description: <br>
Automates TikTok slideshow marketing workflows for apps and products, including competitor research, image generation, text overlays, social posting, analytics tracking, and iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Batsirai](https://clawhub.ai/user/Batsirai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, app marketers, and product teams use this skill to set up agent-assisted TikTok slideshow campaigns, generate content assets, post through Postiz, and use analytics or conversion data to refine hooks and calls to action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags social posting automation, recurring analytics collection, plaintext secrets, and broad setup authority. <br>
Mitigation: Review before installing, keep secrets in environment variables or a secrets manager, and require explicit approval before installs, posting, scheduled jobs, or analytics access. <br>
Risk: The security review warns that account-warmup or anti-detection guidance may violate platform rules. <br>
Mitigation: Avoid account-warmup and anti-detection workflows, and confirm that any posting process complies with TikTok, Postiz, and other platform terms. <br>
Risk: RevenueCat and analytics integrations can expose subscriber, conversion, and campaign performance data. <br>
Mitigation: Grant only the minimum required API access, avoid committing configuration files with secrets, and review generated reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Batsirai/larryskill) <br>
- [Analytics & Feedback Loop](references/analytics-loop.md) <br>
- [App Category Templates](references/app-categories.md) <br>
- [Competitor Research Guide](references/competitor-research.md) <br>
- [RevenueCat Integration](references/revenuecat-integration.md) <br>
- [Slide Structure & Hook Writing](references/slide-structure.md) <br>
- [Postiz](https://postiz.pro/oliverhenry) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration, JavaScript scripts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local campaign files, reports, and scheduled automation configuration when the user approves the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
