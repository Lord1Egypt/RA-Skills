## Description: <br>
Obsidian Assistant helps Obsidian users learn and maintain vault structure, habits, templates, Dataview queries, QuickAdd macros, and vault health workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltryee](https://clawhub.ai/user/ltryee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Obsidian users use this skill to get personalized knowledge-management guidance, generate reusable note templates and automation snippets, and diagnose vault organization issues based on their own setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores vault-related preferences and workflow details for personalization, which may include private note titles, paths, plugin lists, or directory structure. <br>
Mitigation: Redact sensitive paths, note titles, screenshots, command output, and directory listings before sharing; periodically inspect or clear references/habit-patterns.md. <br>
Risk: Generated Dataview queries, templates, QuickAdd macros, and workflow changes could be inaccurate for a user's vault or plugin setup. <br>
Mitigation: Review generated snippets and templates before applying them to an Obsidian vault, and test changes on a copy or small subset first. <br>


## Reference(s): <br>
- [Obsidian Concepts](references/obsidian-concepts.md) <br>
- [Habit Patterns](references/habit-patterns.md) <br>
- [Obsidian Assistant on ClawHub](https://clawhub.ai/ltryee/obsidian-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and optional JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to Markdown templates and the habit profile when users confirm personalization details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
