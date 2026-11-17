## Description:

Obsidian CLI Plugins helps agents automate configured Obsidian vault workflows, including vault checks, Git-backed sync, Tasks todos, journal and project records, attachment-backed records, safe vault reads and searches, plugin commands, and OpenClaw sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxshelley](https://clawhub.ai/user/dxshelley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let agents work with real Obsidian vaults through stable Python workflows for status checks, syncing, task management, note records, attachments, project notes, and safe content access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default sync-backed commands can commit and push unrelated or sensitive pending vault changes to the configured Git remote.

Mitigation: Review vault Git status before installation and use; choose local-only or no-sync modes for sensitive notes and keep secrets out of the vault repository.

Risk: Uploaded or staged media can be copied into durable Obsidian records when attachment recording is requested.

Mitigation: Use attachment recording only for intended files, verify readable local paths or staged selectors, and avoid recording private media unless durable storage is desired.

## Reference(s):

- [Obsidian CLI Plugins User Usage Examples](docs/user-usage.md)
- [Obsidian CLI Plugins Agent Usage Examples](docs/agent-usage-examples.md)
- [Obsidian Fast Paths](references/fast-paths.md)
- [Obsidian Runtime, Sync, and Commands](references/runtime-sync.md)
- [Vault Safety and Content Semantics](references/vault-safety.md)
- [Obsidian Record Workflows](references/record-workflows.md)
- [Record Body Configuration](references/record-body.md)
- [Obsidian Task Add Workflows](references/task-add.md)
- [Obsidian Task Query Workflows](references/task-query.md)
- [Obsidian Official CLI Reference](references/official-cli.md)
- [OpenClaw Compatibility](references/openclaw.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled workflows can read and write Obsidian vault files, run Git or Obsidian CLI commands, copy requested attachments into records, and return structured JSON for agent handoff.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
