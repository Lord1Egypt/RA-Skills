## Description:

Oskill Proxy lets an agent call a local Android HTTP API to start Activities and Services, send Broadcasts, and operate on ContentProviders when direct Android component invocation is not available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soso-eng](https://clawhub.ai/user/soso-eng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate HTTP API calls for controlling Android app components through a locally running OSkillProxy service. It is intended for trusted device automation scenarios where the target component, token, and ContentProvider operation are explicitly chosen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hardcoded bearer token may allow unintended access if reused or exposed.

Mitigation: Generate a token for your own device, rotate any exposed token, and keep requests limited to trusted local agents.

Risk: The proxy can start Android components and perform broad ContentProvider reads, writes, updates, deletes, and calls.

Mitigation: Use explicit package, class, URI, and selection parameters whenever possible, and avoid broad ContentProvider operations unless the data impact is understood.

Risk: Incorrect implicit Intents or provider operations can affect apps or data beyond the intended target.

Mitigation: Review generated requests before execution and prefer narrow, explicit targets with least-necessary flags and extras.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soso-eng/skills/oskill-proxy)
- [Publisher profile](https://clawhub.ai/user/soso-eng)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bearer-token authenticated local HTTP requests for Android component and ContentProvider operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
