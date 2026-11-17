## Description:

Openclaw Memory Manager helps agents initialize, organize, snapshot, search, and monitor local markdown memory across episodic, semantic, and procedural folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q262045312-ui](https://clawhub.ai/user/q262045312-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage local agent memory, detect compression risk, create snapshots, migrate flat memory files, and retrieve stored context by memory type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The organizer and categorization scripts can modify or move local memory files in ways that may be broader than the user expects.

Mitigation: Make a separate backup before running organize.sh or categorize.sh, then review the resulting memory, legacy, episodic, semantic, and procedural folders.

Risk: Snapshots consolidate private memory content into markdown files.

Mitigation: Treat generated snapshots as sensitive local data and avoid sharing or syncing them without reviewing their contents.

Risk: Automated runs could repeatedly reorganize or snapshot memory content before a user has reviewed the output.

Mitigation: Run organizer actions manually unless the workspace has been backed up and the schedule has been explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/q262045312-ui/skills/openclaw-memory-manager-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text plus markdown files and local filesystem updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on local OpenClaw workspace memory directories and may create, move, copy, or append markdown memory files.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
