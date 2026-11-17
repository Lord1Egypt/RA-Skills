## Description:

Manage OmniFocus tasks through macOS JavaScript for Automation scripts for adding, listing, searching, completing, updating, and reporting on tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenzo1](https://clawhub.ai/user/shenzo1)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers who use OmniFocus on macOS can use this skill to let an agent inspect task state and perform requested task-management actions such as adding, searching, completing, or updating tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a live OmniFocus database by adding, completing, or updating tasks.

Mitigation: Ask the agent to show matching tasks before write actions and confirm the exact target when task names are similar.

Risk: Listing and searching tasks can expose sensitive personal or work information from task names and notes.

Mitigation: Limit broad list or search requests when OmniFocus contains sensitive information, and avoid requesting notes unless needed.

## Reference(s):

- [OmniFocus Automation Guide](references/automation-guide.md)
- [OmniFocus JXA API Reference](references/jxa-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON returned by helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with OmniFocus installed and running; read operations can include task names, notes, due dates, flags, projects, and tags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
