## Description: <br>
Manage macOS Calendar with OpenClaw in IM-first workflows (Telegram/Discord/Feishu/iMessage/Slack), including screenshot-to-schedule extraction, idempotent create/update, move/extend/reschedule, reminders, conflict checks, daily review sync, and duplicate cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryant24hao](https://clawhub.ai/user/bryant24hao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage macOS Calendar from OpenClaw conversations, including creating, updating, moving, reviewing, and cleaning up events. It is aimed at IM-first scheduling workflows where calendar changes should stay synchronized with daily planning and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change real macOS Calendar data. <br>
Mitigation: Grant Calendar access only when needed, keep date ranges narrow, and review proposed changes before applying them. <br>
Risk: Duplicate cleanup can remove calendar events when run with apply flags. <br>
Mitigation: Use dry-run first, review the generated cleanup plan, and apply deletion only after explicit confirmation. <br>
Risk: The installer can add a daily local cron check that continues running until removed. <br>
Mitigation: Review config.json before installation and run the bundled uninstall script when the recurring check is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bryant24hao/macos-calendar-assistant) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, script arguments, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Calendar operation guidance and invokes bundled local scripts that may emit text or JSON results such as CREATED, UPDATED, SKIPPED, event lists, cleanup plans, or environment checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
