## Description: <br>
Task Planner helps agents manage personal tasks and schedules with natural-language commands, reminders, recurring tasks, Markdown calendar export, and optional voice transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luzewen](https://clawhub.ai/user/luzewen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can ask an agent to add, update, summarize, complete, delete, and export personal tasks and schedules without remembering task IDs. The skill is useful for personal planning workflows that need recurring reminders, calendar-style Markdown exports, and optional audio transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task data, exported calendars, and reminder logs may contain personal schedule details. <br>
Mitigation: Store the generated files in a trusted local environment and review calendar and reminder log contents before sharing them. <br>
Risk: Voice transcription requires an OpenAI API key and sends provided audio for transcription. <br>
Mitigation: Use transcription only when this data flow is acceptable, protect the API key, and avoid submitting sensitive audio. <br>
Risk: Reminder and calendar automation can surface outdated or incorrect schedule information if task data is stale. <br>
Mitigation: Review pending tasks and exported calendars before relying on them for time-sensitive plans. <br>


## Reference(s): <br>
- [Server-resolved source repository](https://github.com/luzewen/openclaw-task-planner) <br>
- [ClawHub skill listing](https://clawhub.ai/luzewen/liuxiaoying-task-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance, shell command snippets, JSON command results, and Markdown calendar files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task data locally in the user's home directory and can export a Markdown calendar document.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
