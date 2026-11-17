## Description:

Guide for OpenClaw setup, config, commands, routing, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer OpenClaw setup, configuration, command, routing, session, gateway health, and troubleshooting questions. It guides agents to inspect local OpenClaw docs and the relevant config subtree before suggesting minimal changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents toward persistent OpenClaw workspace memory, which may contain private or unrelated information.

Mitigation: Only allow the agent to read MEMORY.md when the request explicitly concerns memory behavior and the user approves that access.

Risk: Troubleshooting guidance could lead to incorrect configuration changes if stale sessions or broad config areas are consulted.

Mitigation: Inspect the relevant config subtree and live evidence for the specific failure layer before proposing a minimal change.

## Reference(s):

- [Skill Design Notes for OpenClaw](references/skill-design-notes.md)
- [OpenClaw Triage Checklist](references/triage-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline paths, commands, diagnoses, and concise configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May distinguish verified facts from inferences and call out follow-up tests after configuration or runtime changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
