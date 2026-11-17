## Description:

Memory Guard monitors and verifies agent workspace files to detect unauthorized changes, injection attacks, personality drift, and cross-agent contamination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Memory Guard to initialize hash tracking for workspace memory files, verify later changes, audit file history, stamp provenance metadata, and run one-shot monitoring checks before trusting agent memory state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verifier contains an unsafe code-injection path that could execute attacker-controlled Python if the workspace registry is tampered with.

Mitigation: Review the skill before installing, avoid automatic execution on untrusted or shared workspaces, and fix Python invocations so paths and file names are passed as data arguments rather than embedded into source code.

Risk: The skill writes local hash registries, audit logs, and provenance stamps in the workspace, which can affect files used by agents.

Mitigation: Run initialization and acceptance commands only after human review of the target workspace and keep generated guard files under normal workspace access controls.

## Reference(s):

- [Memory Guard ClawHub skill page](https://clawhub.ai/cassh100k/skills/memory-guard)
- [Publisher profile](https://clawhub.ai/user/cassh100k)
- [Project homepage](https://nixus.pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text verification or audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local hash registries, provenance stamps, and audit logs when its shell command is run.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
