## Description: <br>
Manage Apple Reminders via remindctl CLI (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill on macOS to manage Apple Reminders through the remindctl CLI, including listing, creating, completing, deleting, and filtering reminders. It is appropriate when the user wants tasks to appear in Apple Reminders and sync to iPhone or iPad. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to complete, delete, or delete lists in Apple Reminders, and those changes may persist and sync across devices. <br>
Mitigation: Use explicit user confirmation before delete, complete, or list-deletion actions. <br>
Risk: The skill depends on a local Homebrew-installed CLI that needs Reminders access. <br>
Mitigation: Install only if the Homebrew package is trusted, then grant Reminders permission intentionally. <br>


## Reference(s): <br>
- [remindctl GitHub repository](https://github.com/steipete/remindctl) <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-apple-reminders) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON, TSV/plain, or count-only output produced by remindctl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
