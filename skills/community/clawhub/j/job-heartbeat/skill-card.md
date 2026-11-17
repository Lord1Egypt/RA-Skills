## Description:

AO Job Heartbeat monitors recurring tasks through a hosted dead-man's switch, with a check for each task that is pinged after success and alerts when late.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkhxz7k72d-cmd](https://clawhub.ai/user/jkhxz7k72d-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators monitor recurring jobs and backups for missed or failed runs, manage checks, and inspect alert events through a hosted heartbeat service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposed API keys or ping URLs could allow unauthorized access or false heartbeats.

Mitigation: Set the API key outside chat and keep both the key and generated ping URLs private.

Risk: Deleting a check or marking it failed can stop monitoring or trigger an unintended alert.

Mitigation: Get the user's approval before deleting checks or sending test-fail actions.

Risk: Pinging before job success can hide a failed run.

Mitigation: Ping only after the job's success conditions are met.

## Reference(s):

- [AO Job Heartbeat service](https://beat.austinoaksapi.com/)
- [AO Job Heartbeat on ClawHub](https://clawhub.ai/jkhxz7k72d-cmd/skills/job-heartbeat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance and shell snippets; JSON check and event results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snippets are printed for the user to install; checks and alerts depend on the hosted service.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
