## Description:

Safely create, preview, inspect, run, update, remove, import, export, explain, diagnose, and manage the local dashboard for schedules managed by the Locron local-first job scheduler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitekiwi](https://clawhub.ai/user/whitekiwi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect, diagnose, and manage local Locron scheduler jobs, runs, policies, daemon state, service state, and dashboard access. It emphasizes dry-run review, narrow scope, authorization before mutations, and careful handling of secrets and local scheduler state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized Locron mutations can affect durable local jobs, service state, dashboard state, or queued runs.

Mitigation: Use dry-run where supported, inspect the exact target before mutations without dry-run, and require current user authorization for the specific change.

Risk: Imports, exports, environment values, HTTP headers, bodies, and dashboard tokens can expose secrets or schedule side-effecting work.

Mitigation: Avoid plaintext value flags unless explicitly requested and acknowledged, inspect import plans before applying them, and do not place dashboard tokens in URLs, logs, durable notes, or third-party messages.

Risk: Diagnostics can overstate what Locron observed, especially around missed runs, sleep, queueing, and terminal run state.

Mitigation: Distinguish stored facts from inference, preserve warnings, and use the durable Locron commands for run status instead of inferring outcomes from logs or queue acknowledgements.

## Reference(s):

- [Locron safety model](references/safety.md)
- [ClawHub skill page](https://clawhub.ai/whitekiwi/skills/locron)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run outcomes, warnings, final durable state, and unknowns when Locron commands are executed.]

## Skill Version(s):

0.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
