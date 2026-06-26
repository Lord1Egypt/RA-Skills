## Description: <br>
Provides a personalized morning briefing with today's Apple Reminders items, undone Notion tasks, and vault storage context for daily planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-riverbi](https://clawhub.ai/user/lucas-riverbi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and agents use this skill to assemble a daily planning summary from local reminders and Notion tasks. It is suited for morning briefing, daily summary, or today's-plan requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access today's reminders and undone Notion tasks, which may include private planning data. <br>
Mitigation: Run it only when this access is intended, review the briefing before sharing it, and avoid generic invocations if you do not want those sources read automatically. <br>
Risk: The Notion integration reads a local API key and queries a tasks database. <br>
Mitigation: Use a Notion token limited to the single tasks database and verify NOTION_TASKS_DB points only to the intended database. <br>
Risk: Briefing content may be persisted to vault storage. <br>
Mitigation: Confirm whether vault writes are enabled in the environment and avoid storing sensitive planning details when persistence is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucas-riverbi/morning-briefing) <br>
- [Usage](references/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown-like plain text briefing with dated sections for reminders and Notion tasks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read Apple Reminders via remindctl, query Notion when NOTION_TASKS_DB is configured, and expose private planning data in the briefing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
