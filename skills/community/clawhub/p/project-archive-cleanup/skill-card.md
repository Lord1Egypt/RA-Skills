## Description:

Archive-clean finished, long-idle project directories — retain planning documents and result artifacts, strip execution traces (one-off scripts, import intermediates, scrape snapshots, console logs, superseded versions, byte-identical duplicates). Use when asked to clean up project leftovers, reduce process noise, or archive completed work. Always read-only scan first, then a two-phase backup-and-delete with batching for the safe-delete threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace maintainers use this skill to review completed or long-idle project directories and prepare a careful cleanup that preserves planning and result files while removing verified process residue. It is intended for unrestricted projects; active or restricted material is excluded or held for sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Partial scanner coverage leaves some local references unresolved, so relevant behavior may not have been fully assessed.

Mitigation: Review the unresolved local references and inspect the skill content before installation.

Risk: Cleanup could remove active, unique, or restricted project material if candidates are classified incorrectly.

Mitigation: Check activity, verify duplicates by SHA-256, hold restricted material for sign-off, and review the complete dry-run manifest; back up and verify file counts before deletion.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/haiyangchenbj/skills/project-archive-cleanup)
- [Publisher profile](https://clawhub.ai/user/haiyangchenbj)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown reports, Shell commands]

**Output Format:** [Markdown with inventory, keep/remove decisions, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only inventory first; cleanup uses a dry run, backup, explicit approval where required, and a safe-delete limit.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
