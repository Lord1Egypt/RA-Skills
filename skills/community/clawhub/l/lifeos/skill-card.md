## Description:

LifeOS helps agents read, search, append to, and update a LifeOS or Obsidian PARA vault through the @life-os/cli command-line tool without opening Obsidian or Aino.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanru](https://clawhub.ai/user/quanru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent inspect tasks and notes, capture entries, maintain periodic and PARA theme notes, and update LifeOS AI Wiki pages in a local LifeOS/Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned remote npm CLI that can read and modify a local LifeOS/Obsidian vault.

Mitigation: Use the skill only with a trusted @life-os/cli publisher, pin a known CLI version where practical, and keep vault backups or version control before allowing write operations.

Risk: Create, append, task-toggle, skill-install, and overwrite workflows can change or replace vault content.

Mitigation: Review resolved paths and command arguments before execution, avoid overwrite and skill install unless explicitly intended, and prefer search or read commands before writes.

## Reference(s):

- [LifeOS](https://lifeos.md/)
- [Command reference](references/commands.md)
- [LifeOS AI Wiki maintenance rules](references/ai-wiki.md)
- [LifeOS AI Wiki compatibility note](references/llm-wiki.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and LifeOS vault content updates through the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands may emit JSON when invoked with --json; write operations can create, append to, overwrite, or toggle Markdown note content in the selected vault.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
