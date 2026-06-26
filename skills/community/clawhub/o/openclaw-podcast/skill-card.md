## Description: <br>
Transform an OpenClaw workspace into personalized AI-powered podcast briefings about work, priorities, metrics, and strategy using Superlore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdamJurgens](https://clawhub.ai/user/AdamJurgens) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to turn local workspace memory, job, and status files into private audio briefing episodes through Superlore. It supports manual episode generation, dry-run review, custom briefing styles, and scheduled recurring briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sanitized workspace summaries and derived project/profile context are transmitted to Superlore. <br>
Mitigation: Run dry-run review before generation, keep sensitive information out of workspace memory files where possible, and install only if external transmission to Superlore is acceptable. <br>
Risk: The setup wizard can persist the Superlore API key in a shell profile. <br>
Mitigation: Decline shell-profile persistence unless plaintext storage is acceptable, or store the key using a local secret-management workflow instead. <br>
Risk: Recurring briefings may repeatedly send newly derived workspace context on a schedule. <br>
Mitigation: Inspect generated OpenClaw cron commands before enabling them and periodically review or remove scheduled jobs. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/AdamJurgens/openclaw-podcast) <br>
- [Publisher Profile](https://clawhub.ai/user/AdamJurgens) <br>
- [Superlore](https://superlore.ai) <br>
- [Superlore API Reference](references/api.md) <br>
- [Briefing Styles Reference](references/styles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console text with shell commands and generated episode links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce dry-run previews, OpenClaw cron commands, custom style configuration guidance, and private Superlore episode links.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
