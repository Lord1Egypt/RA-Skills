## Description: <br>
My Computer is a desktop automation agent that uses CLI commands, application automation, and scripts to organize files, automate local tasks, run diagnostics, build apps, and manage scheduled workflows on a user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikewang817](https://clawhub.ai/user/mikewang817) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and engineers use this skill to automate work on their own computers, including file organization, batch processing, local app automation, diagnostics, maintenance, reporting, and scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local automation can affect user files, including large batch moves, renames, and writes. <br>
Mitigation: Keep tasks narrowly scoped, require previews before batch file changes, and review execution manifests after operations. <br>
Risk: The skill can send data through local applications or connected services. <br>
Mitigation: Explicitly approve recipients, channels, attachments, and upload destinations before anything is emailed or uploaded. <br>
Risk: Scheduled automations may continue running after setup. <br>
Mitigation: Review and manually test each scheduled task before enabling it. <br>
Risk: Undo manifests from untrusted locations could cause unintended file changes. <br>
Mitigation: Run undo operations only against trusted manifests created by this skill during a known operation. <br>


## Reference(s): <br>
- [Application Automation Recipes](references/app-automation.md) <br>
- [Platform-Specific Guide](references/platform-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/mikewang817/my-computer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, plans, manifests, and reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run previews, execution manifests, progress updates, undo instructions, and post-operation summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
