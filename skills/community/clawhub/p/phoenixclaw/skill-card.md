## Description: <br>
PhoenixClaw passively scans OpenClaw session logs and memory files to generate Markdown journals, summaries, timelines, growth maps, and profile updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goforu](https://clawhub.ai/user/goforu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use PhoenixClaw to run passive personal journaling over OpenClaw activity, turning session logs, memory files, and media references into daily or weekly Markdown reflections and long-term personal profile artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly reads OpenClaw session logs, memory files, media references, agent runs, and cron runs. <br>
Mitigation: Install only when that local data access matches the intended private journaling use, and review the configured journal and source paths before enabling automation. <br>
Risk: Recurring cron operation can summarize private activity without each manual invocation. <br>
Mitigation: Enable cron deliberately, confirm the schedule and timezone, and review cron registration and history after setup. <br>
Risk: The security summary notes plugin execution and avoidable shell-command fallbacks. <br>
Mitigation: Review enabled plugins, pin a fixed version, and prefer a version that removes execSync shell fallbacks and clarifies plugin access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goforu/phoenixclaw) <br>
- [Cron setup](references/cron-setup.md) <br>
- [Media handling](references/media-handling.md) <br>
- [Plugin protocol](references/plugin-protocol.md) <br>
- [User configuration](references/user-config.md) <br>
- [Profile evolution](references/profile-evolution.md) <br>
- [Obsidian format](references/obsidian-format.md) <br>
- [Skill recommendations](references/skill-recommendations.md) <br>
- [Visual design](references/visual-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown journal files and setup guidance with inline shell commands and YAML configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local journal, profile, timeline, and growth-map files, and may copy referenced media into user-configured journal assets.] <br>

## Skill Version(s): <br>
0.0.19 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
