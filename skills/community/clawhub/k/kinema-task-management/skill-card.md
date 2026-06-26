## Description: <br>
Kinema personal task tracking system where an AI agent maintains local Markdown task files, daily reports, snapshots, and task archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeshunee](https://clawhub.ai/user/leeshunee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent create, update, archive, snapshot, and report on personal tasks stored as Markdown files in an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local Markdown task history, which may contain sensitive task descriptions. <br>
Mitigation: Avoid putting secrets or sensitive information in task titles, descriptions, and changelog entries. <br>
Risk: Daily cron automation can continue sending reports or archiving tasks after setup. <br>
Mitigation: Confirm the report destination during onboarding and remove the kinema-tasks cron jobs when daily reports or automatic archiving are no longer wanted. <br>
Risk: Reports may be delivered to the wrong channel if cron delivery settings are misconfigured. <br>
Mitigation: Verify the OpenClaw channel and recipient before creating scheduled report jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeshunee/kinema-task-management) <br>
- [README.md](artifact/README.md) <br>
- [ONBOARDING.md](artifact/ONBOARDING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown task files, Markdown reports, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local task, archive, report, and snapshot files under the configured task directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
