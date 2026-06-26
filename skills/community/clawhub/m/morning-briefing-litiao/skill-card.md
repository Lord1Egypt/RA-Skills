## Description: <br>
Generates a personalized morning briefing from today's reminders and undone Notion tasks, with optional storage of the resulting report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and productivity-focused users can ask an agent for a morning briefing or daily plan that combines reminders with open Notion tasks. Developers can configure the Notion database through environment settings when adapting the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a Notion API key from ~/.config/notion/api_key and uses it to query a configured Notion database. <br>
Mitigation: Use a narrowly scoped Notion token and confirm the configured database before running the skill. <br>
Risk: The briefing may include private reminders and task data, and the evidence notes possible storage of the resulting briefing. <br>
Mitigation: Review where briefing output will be captured or saved before execution, especially when it may include private task information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/morning-briefing-litiao) <br>
- [USAGE.md](references/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like daily briefing text emitted to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the current date by default and can query a configured Notion tasks database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
