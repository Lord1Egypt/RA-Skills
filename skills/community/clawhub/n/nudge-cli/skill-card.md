## Description: <br>
How to use the nudge CLI for commands, flags, setup, onboarding, task management, secrets, status checks, and punishment configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neilsanghrajka](https://clawhub.ai/user/neilsanghrajka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the Nudge CLI for accountability workflows, including setup, task creation, task completion or failure, secret selection, punishment configuration, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide collection of embarrassing secrets and disclosure to contacts as punishment. <br>
Mitigation: Use harmless test content instead of damaging secrets, verify each recipient and token scope, and confirm stored secrets can be deleted before relying on the workflow. <br>
Risk: Punishment actions can automatically send messages when a task fails. <br>
Mitigation: Confirm task cancellation, cleanup, and punishment-disable paths before use, and start with desktop notifications or other low-impact test actions. <br>
Risk: The documented shell installer fetches a remote script. <br>
Mitigation: Inspect the installer before running it and prefer package-manager or Go install paths when those better match the user's environment. <br>


## Reference(s): <br>
- [Nudge CLI Reference](references/cli-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/neilsanghrajka/nudge-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include JSON-output command variants when the user needs machine-readable Nudge CLI output.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
