## Description:

Run on every heartbeat to summarize completed tasks and log them to your analytics dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[proviras](https://clawhub.ai/user/proviras)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to record agent heartbeat activity, task summaries, outcomes, model identifiers, and skill usage in a Proviras analytics dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends identifiable agent activity, task summaries, model identifiers, and stable user or agent IDs to proviras.com on every heartbeat.

Mitigation: Install only after workspace-owner approval for continuous telemetry, and avoid use around confidential work unless retention, deletion, and data handling terms are already agreed.

Risk: The skill can create persistent parent-child linkage across spawned agents when parent identifiers are propagated.

Mitigation: Control propagation of PROVIRAS_PARENT_ID and PROVIRAS_USER_ID, and do not pass cross-agent identifiers into spawned agents unless that tracking is intended and approved.

Risk: The skill stores a registered agentId locally in references/config.md.

Mitigation: Review generated configuration before sharing or publishing workspaces, and remove local identifiers where they are not meant to travel with the artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/proviras/skills/proviras-logger)
- [Proviras publisher profile](https://clawhub.ai/user/proviras)
- [Proviras service](https://proviras.com)
- [Payload schema](references/payload-schema.md)
- [Agent config](references/config.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Structured JSON payloads sent through shell commands, with a short text status on success]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads heartbeat memory and local agent configuration; posts analytics data to Proviras when invoked.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
