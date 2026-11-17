## Description:

Memory Manager provides local memory management for agents, including compression detection, snapshots, typed memory organization, semantic search, and usage statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marmikcfc](https://clawhub.ai/user/marmikcfc)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to organize local agent memory into episodic, semantic, and procedural files, monitor compression risk, create recovery snapshots, and search prior context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell scripts can move, copy, or rewrite local memory files under the configured OpenClaw workspace.

Mitigation: Back up the memory directory before use and confirm OPENCLAW_WORKSPACE points to the intended workspace before running organize.sh, categorize.sh, or snapshot.sh.

Risk: Weak path controls make untrusted file paths or category names risky when using categorize.sh.

Mitigation: Use only trusted local source files and simple expected names when categorizing memory content.

Risk: Snapshots may contain sensitive memory content copied from episodic, semantic, and procedural files.

Mitigation: Treat snapshot Markdown files as sensitive, review them before sharing, and keep them out of public repositories or automated uploads.

Risk: Automatic heartbeat execution can repeatedly run file-changing memory operations before the skill is reviewed.

Mitigation: Review the scripts and run them manually first; add them to an automated heartbeat only after confirming the behavior is acceptable.

## Reference(s):

- [ClawHub Memory Manager listing](https://clawhub.ai/marmikcfc/skills/memory-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text and Markdown files with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local memory directories, state files, and snapshot Markdown files under the configured OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
