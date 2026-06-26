## Description: <br>
Manage OmniFocus tasks through JavaScript for Automation scripts that add, list, search, complete, update, and summarize tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenzo1](https://clawhub.ai/user/shenzo1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent review and manage OmniFocus tasks on macOS, including inbox triage, searching, status reporting, and user-directed task updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task notes and search results can expose sensitive personal or work information to the agent. <br>
Mitigation: Use the skill only when the agent may read OmniFocus task data, and avoid searching or displaying sensitive notes unless needed. <br>
Risk: Completion and update scripts can change the wrong task when names are ambiguous because they act on matching task names. <br>
Mitigation: List or search matching tasks first, confirm the intended task with the user, and then run completion or update commands. <br>


## Reference(s): <br>
- [OmniFocus ClawHub Release](https://clawhub.ai/shenzo1/omnifocus) <br>
- [OmniFocus Automation Guide](references/automation-guide.md) <br>
- [OmniFocus JXA API Reference](references/jxa-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and parsed JSON task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task list and search outputs may include task names, notes, due dates, flags, projects, and tags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
