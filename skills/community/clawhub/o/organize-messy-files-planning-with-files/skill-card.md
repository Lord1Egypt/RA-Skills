## Description:

Implements Manus-style file-based planning for complex tasks. Creates task_plan.md, findings.md, and progress.md. Use when starting complex multi-step tasks, research projects, or any task requiring >5 tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long, multi-step work organized through persistent planning, findings, and progress files in the project directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-controlled task_plan.md content can be placed into agent context before file edits or shell commands.

Mitigation: Review existing planning files before use, especially in untrusted repositories, and remove or disable the automatic planning-file hook if that behavior is not desired.

Risk: Stale or incorrect planning files can steer later agent decisions during long tasks.

Mitigation: Keep planning files current, mark phase status explicitly, and review the plan before major decisions.

## Reference(s):

- [Planning With Files skill page](https://clawhub.ai/lnj22/skills/organize-messy-files-planning-with-files)
- [Reference: Manus Context Engineering Principles](reference.md)
- [Examples: Planning with Files in Action](examples.md)
- [Task plan template](templates/task_plan.md)
- [Findings template](templates/findings.md)
- [Progress template](templates/progress.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown planning files with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates task_plan.md, findings.md, and progress.md in the active project directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
