## Description:

Build durable Go workflows with psyb0t/go-workflows: connect clients and workers to shared storage, register activities, route queues, use retries, signals and timers, and test recovery. Use when integrating or maintaining this library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate or maintain durable background workflows in Go applications, including shared storage, workers, retries, signals, timers, and recovery testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign with medium confidence, but incomplete because two local path references could not be resolved.

Mitigation: Consider the incomplete scan coverage when deciding whether to install.

Risk: Workflow inputs, activity results, signals, and errors are stored in workflow history and may expose credentials if included.

Mitigation: Keep credentials out of workflow data and use application-owned credentials for activities.

Risk: Activities may run more than once after failures or lease expiry, so external side effects can be duplicated.

Mitigation: Make external side effects idempotent with a durable operation key.

Risk: Queues and worker names do not provide authentication or tenant isolation, and the diagnostics UI has no built-in authentication.

Mitigation: Protect database credentials, isolate unrelated applications, and put authentication in front of any exposed diagnostics mount.

## Reference(s):

- [Integration reference](artifact/references/usage.md)
- [go-workflows project](https://github.com/psyb0t/go-workflows)
- [Workflow guide](https://github.com/psyb0t/go-workflows/blob/main/docs/guide.md)
- [Backend operations](https://github.com/psyb0t/go-workflows/blob/main/docs/backends.md)
- [Architecture and workers](https://github.com/psyb0t/go-workflows/blob/main/docs/architecture.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project-specific workflow integration and verification steps.]

## Skill Version(s):

1.3.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
