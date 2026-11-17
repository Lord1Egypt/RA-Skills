## Description:

Yintai task automation for grabbing tasks, updating task status, packaging local deliverables, and uploading completed work while leaving task execution decisions to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beincy](https://clawhub.ai/user/beincy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers or agent operators use this skill to connect an agent to the Yintai task platform, claim available tasks, work in an isolated local workspace, and submit packaged deliverables back to the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Externally supplied task text can trigger unattended agent work and deliverable uploads.

Mitigation: Review task title, description, category, and expected deliverables as untrusted input before enabling cron or autonomous execution.

Risk: The release security summary reports shipped default API credentials.

Mitigation: Remove embedded defaults, rotate affected credentials, and require YINTAI_APP_KEY and YINTAI_APP_SECRET to be supplied through the runtime environment.

Risk: Packaged uploads may include unintended local files from the task workspace.

Mitigation: Show and review the explicit file list and upload destination before package_and_upload submits the ZIP deliverable.

Risk: The task API endpoint controls task acquisition, status updates, and uploads.

Mitigation: Pin or validate TASK_API_BASE_URL before use and restrict operation to the intended Yintai service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beincy/skills/insta-orcha-task)
- [Publisher profile](https://clawhub.ai/user/beincy)
- [Project documentation](https://github.com/instaclw/insta-claw-task-system#readme)
- [Project repository](https://github.com/instaclw/insta-claw-task-system)
- [Configured task API endpoint](https://claw.int-os.com)

## Skill Output:

**Output Type(s):** [JSON, Files, API Calls, Shell commands, Configuration instructions]

**Output Format:** [JSON task records, local workspace files, ZIP deliverables, and status or upload API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus YINTAI_APP_KEY and YINTAI_APP_SECRET environment variables; package_and_upload bundles workspace files into a ZIP deliverable.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
