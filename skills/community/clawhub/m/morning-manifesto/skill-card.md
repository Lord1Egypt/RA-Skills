## Description: <br>
Daily morning reflection workflow with task sync to Obsidian, Apple Reminders, and Linear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcBickel](https://clawhub.ai/user/MarcBickel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users who want a daily planning routine use this skill to collect morning reflections, append a structured entry to an Obsidian daily note, sync tasks with Apple Reminders, and summarize urgent Linear issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update notes, reminders, and Linear-related task information. <br>
Mitigation: Install only when those tool actions are expected, and review parsed tasks and destinations before allowing sync actions. <br>
Risk: Ambiguous dates, names, or work items in a morning response could be synced incorrectly. <br>
Mitigation: Confirm detected tasks, due dates, and target systems before creating or updating reminders and summaries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MarcBickel/morning-manifesto) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and plain-text planning summaries with structured note content and task-sync instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read a text or transcribed audio response, update Obsidian notes, sync Apple Reminders, and query Linear when the host agent has those integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
