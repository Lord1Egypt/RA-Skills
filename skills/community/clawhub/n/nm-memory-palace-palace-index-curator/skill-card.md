## Description:

Curate the web-capture index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use the skill to review a web-research capture index, promote or archive pending entries, repair capture metadata, and surface valuable stored research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some referenced files were missing from the inspected release, leaving their behavior unverified.

Mitigation: Review the complete plugin and referenced scripts or hooks before enabling the skill.

Risk: Apply modes can persist promotion, archive, or repair changes to local capture data.

Mitigation: Run the report and dry-run commands first, inspect the proposed changes, and confirm the documented backup is created before applying.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-memory-palace-palace-index-curator)
- [Memory Palace plugin homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [Archive Pattern module](artifact/modules/archive-pattern.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown reports, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reporting and dry-run modes are available; apply modes update the local capture index or capture files, with backups documented for these operations.]

## Skill Version(s):

1.10.3 (source: release evidence and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
