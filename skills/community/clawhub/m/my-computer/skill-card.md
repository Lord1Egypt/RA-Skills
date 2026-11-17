## Description:

Desktop automation agent that uses CLI commands, application automation, and scripting to work directly with the user's local machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikewang817](https://clawhub.ai/user/mikewang817)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and engineers use this skill to automate local desktop work such as file organization, batch processing, duplicate detection, application scripting, scheduled tasks, system diagnostics, and local development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local automation authority can affect user files, applications, system settings, and scheduled tasks.

Mitigation: Use the skill only with explicit directories and reviewed commands, and require clear confirmation before destructive, system-level, recurring, or outbound-message operations.

Risk: Batch file scripts can move, rename, copy, organize, or undo operations across many files.

Mitigation: Run dry-run previews first, inspect operation manifests, preserve backups for important data, and verify post-operation summaries before continuing.

Risk: Undo operations can delete copied files or move files based on manifest contents.

Mitigation: Run undo operations only with trusted, inspected manifests created for the intended operation, and use dry-run mode before applying changes.

Risk: Recurring-task and outbound-message recipes can persist or send data unexpectedly if configured incorrectly.

Mitigation: Create and test the target script manually first, review the exact schedule, recipients, attachments, and removal steps, and avoid enabling recurring jobs unless those details are explicit.

## Reference(s):

- [Application Automation Recipes](artifact/references/app-automation.md)
- [Platform-Specific Guide](artifact/references/platform-guide.md)
- [Publisher Profile](https://clawhub.ai/user/mikewang817)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, scripts, plans, reports, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run previews, operation manifests, disk reports, duplicate reports, and post-operation summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
