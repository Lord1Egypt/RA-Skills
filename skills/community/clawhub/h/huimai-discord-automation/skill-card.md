## Description: <br>
Automates routine Discord community operations such as replies, permission management, channel cleanup, moderation, activity reporting, and logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Discord community administrators and project or gaming community operators use this skill to configure welcome messages, automate common moderation workflows, clean up channels, assign roles, and summarize server activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bot permissions can enable high-impact moderation and cleanup actions such as deleting messages, kicking users, changing roles, or changing channels. <br>
Mitigation: Use a dedicated low-privilege bot token, grant only required permissions, and test in a non-critical server before enabling real moderation permissions. <br>
Risk: Professional mode can skip confirmations for batch or destructive actions. <br>
Mitigation: Start in log-only or confirmation-required mode and avoid professional mode for deletes, kicks, role changes, and channel changes unless the workflow has been reviewed. <br>
Risk: Keyword-based moderation can create false positives that affect legitimate users or messages. <br>
Mitigation: Tune keyword rules gradually, review log-only results first, and require confirmation before enforcement until the rule set is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/huimai-discord-automation) <br>
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration steps, and Discord automation action plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute Discord moderation, cleanup, role, and channel operations depending on the agent environment and granted bot permissions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact changelog, released 2026-05-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
