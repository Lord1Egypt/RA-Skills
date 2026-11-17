## Description:

Idea Manager is a structured command-line skill for managing ideas, proposals, todos, and wishlist items in IDEAS.md with validated read, write, edit, delete, archive, report, and JSON workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kens-agents](https://clawhub.ai/user/kens-agents)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep personal or project ideas, proposals, todos, and wishlist items in a consistent IDEAS.md format. It supports listing, searching, adding, editing, deleting, archiving, reporting, and JSON-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete and archive operations can permanently remove entries from IDEAS.md or reindex remaining entries.

Mitigation: Review the command and target entries before execution, keep backups for important idea lists, and use archive --force only when non-interactive execution is intentional.

Risk: The --file option can point the manager at an alternate path that will be treated as an ideas file and rewritten.

Mitigation: Confirm that --file targets only an intended IDEAS.md-compatible file before running write, edit, delete, or archive operations.

Risk: Archive files under memory/ may preserve idea metadata and, with --archive-details, full entry details.

Mitigation: Use the default metadata-only archive unless full details are needed, and review archive contents when ideas may contain sensitive project information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kens-agents/skills/idea-manager)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown reports, JSON arrays or objects, human-readable status text, and file updates to IDEAS.md or memory archive files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing commands can create, rewrite, delete, archive, and reindex idea entries; --file can target an alternate ideas file.]

## Skill Version(s):

1.1.1 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
