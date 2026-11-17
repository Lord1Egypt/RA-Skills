## Description:

Task capture, scheduling, and linked knowledge in org-mode files via the `org` CLI. Query, mutate, link, and search the user's org files and org-roam database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dcprevere](https://clawhub.ai/user/dcprevere)

### License/Terms of Use:

MIT-0

## Use Case:

Org-mode users and developers use this skill to let an agent capture TODOs, schedule work, search notes, and maintain linked org-roam knowledge. It is suited for personal or team workflows where the user wants durable task and knowledge state stored in local org files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Note and TODO writes may escape the configured org workspace because of the confirmed path-handling flaw reported by security evidence.

Mitigation: Keep ORG_CLI_DIR pointed at a dedicated workspace and avoid custom file or inboxFile values with path components until the path handling is fixed.

Risk: The skill can modify org files, org-roam files, and the org SQLite database through the agent.

Mitigation: Use previews or explicit confirmation for schedule, state, append, and batch changes, and review item IDs and target paths in write confirmations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dcprevere/skills/org-cli)
- [Project homepage](https://github.com/dcprevere/org-cli)
- [GitHub releases](https://github.com/dcprevere/org-cli/releases)
- [Knowledge management reference](references/knowledge-management.md)
- [Task management reference](references/task-management.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and JSON-aware confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes should surface org-cli action lines with stable item IDs when available.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, OpenClaw plugin manifest, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
