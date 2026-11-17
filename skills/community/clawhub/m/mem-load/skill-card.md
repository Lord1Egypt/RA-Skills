## Description:

Loads recent memory-bank task and session context so an agent can identify relevant implementation docs when $mem-load is invoked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to load recent project memory-bank context, identify the active task and latest session, and decide which implementation documents the agent should read next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory-bank files may contain credentials, personal data, or unrelated confidential notes that would be loaded into the active agent session.

Mitigation: Keep sensitive information out of memory-bank files and use runtimes that keep referenced paths limited to the project memory-bank.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to read local memory-bank files; it does not define network access, persistence, or hidden execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
