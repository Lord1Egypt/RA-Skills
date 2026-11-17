## Description:

Searches and manages Markdown notes in an Obsidian vault, uses Git to inspect history and commit changes, and guides remote setup and fetch/pull/push synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cfddd](https://clawhub.ai/user/cfddd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and note-taking users use this skill to let an agent work inside an Obsidian Markdown vault, create or update notes, review Git history, and coordinate local and remote vault synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional auto-sync can create a recurring agent task.

Mitigation: Enable the cron helper only after reviewing the scheduled message, interval, vault path, remote target, and disable procedure.

Risk: The Git workflow can rewrite remote history after broad consent.

Mitigation: Treat force-with-lease as a manual recovery action and confirm the exact branch and remote before allowing it.

Risk: The skill can modify and synchronize personal notes in a selected vault.

Mitigation: Confirm the vault path before file or Git operations and keep synchronization scoped to the intended Obsidian repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cfddd/skills/obsidian-git-vault)
- [Git remote setup guide](git-remote-wizard.md)
- [Vault sync SOP](vault-sync-sop.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Git and filesystem operations within the selected vault when the user has confirmed the target path and operation.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
