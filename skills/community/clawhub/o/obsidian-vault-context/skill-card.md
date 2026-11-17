## Description:

Teach Claude to use an Obsidian vault as a shared workspace with persistent state across sessions, including vault navigation, orchestration file management, output routing, and optional bidirectional collaboration via Obsidian Headless.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tesfandiari1](https://clawhub.ai/user/tesfandiari1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to let an agent read and maintain shared Obsidian vault context, update persistent status and task files, and route reusable work into the vault. It is especially suited to long-running projects where human and agent collaborators need durable Markdown state across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional server sync can create a long-running service with broad access to synced notes and locally stored Obsidian credentials.

Mitigation: Use a dedicated unprivileged account, prefer a user-level or sandboxed service, secure the host, and document a clear uninstall path before enabling continuous sync.

Risk: Installing the optional Obsidian Headless package globally can increase dependency and update risk.

Mitigation: Pin the package version where possible and review the installed package before using it in a persistent sync workflow.

Risk: A synced vault may contain sensitive folders or agent configuration that should not be modified by the agent.

Mitigation: Keep agent code and workflow definitions outside the synced vault, use selective sync for sensitive folders, and treat legal or credential-bearing areas as read-only.

## Reference(s):

- [Orchestration Files Guide](references/orchestration-files.md)
- [Obsidian Headless Sync Setup](references/obsidian-headless-setup.md)
- [Vault Structure Template](references/vault-structure-template.md)
- [Obsidian Headless documentation](https://obsidian.md/help/sync/headless)
- [Obsidian Sync](https://obsidian.md/sync)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with YAML frontmatter, wikilinks, tables, checklists, and optional bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes persistent state to _context/ files and deliverables to work/ or equivalent vault folders.]

## Skill Version(s):

1.0.1 (source: server release; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
