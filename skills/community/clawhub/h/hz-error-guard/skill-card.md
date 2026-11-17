## Description:

Huizai Error Guard monitors, classifies, and intercepts OpenClaw errors in real time with retry, circuit-breaking, and recovery support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lidekahdjdhdhsjjs-lang](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to monitor long-running agent tasks, classify failures, emit task lifecycle events, and coordinate controlled recovery actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emergency recovery behavior can kill every visible execution session without clear ownership checks or user confirmation.

Mitigation: Before shared or production OpenClaw use, change recovery actions to track and kill only sessions created by this skill, require explicit authorization for flush, recover, and restart actions, and document operational impact clearly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lidekahdjdhdhsjjs-lang/skills/hz-error-guard)
- [ClawHub publisher profile](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown guidance with code examples and TypeScript helper modules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task status data, task event payloads, heartbeat actions, and recovery status messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
