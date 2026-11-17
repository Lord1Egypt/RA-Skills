## Description:

Inspect one selected OpenClaw instance and its agent bindings, create verified private snapshots, compare changes and rehearse restoration in a new directory. Use for OpenClaw Maintenance and Migration Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

OpenClaw owner/operators use this skill to inspect one chosen instance, create and verify private snapshots, compare state, and rehearse recovery in a new directory when preparing maintenance or migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives and restored copies contain usable credentials, which could be exposed if stored or shared carelessly.

Mitigation: Confirm the selected instance and keep the archive and maintenance folder private and accessible only to you.

Risk: A restore rehearsal can succeed even when a live migration would fail, and workspaces outside the selected instance root may be omitted.

Mitigation: Back up external workspaces separately and treat a successful rehearsal as file recovery evidence, not proof of live service behavior.

## Reference(s):

- [Job contract](references/input.md)
- [MochiLab](https://mochilab.bz)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-claw-maintenance)

## Skill Output:

**Output Type(s):** [Files, JSON, Configuration guidance]

**Output Format:** [JSON inventory and receipts, ZIP snapshot archives, and a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot archives may contain credentials and should be kept private.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
