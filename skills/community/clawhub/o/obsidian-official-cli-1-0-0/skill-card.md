## Description:

Work with Obsidian vaults using the official Obsidian CLI (v1.12+). Open, search, create, move, and manage notes from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justin-202603](https://clawhub.ai/user/justin-202603)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent operate Obsidian vaults through the official CLI for note management, file operations, search, tasks, properties, links, plugins, themes, sync, and workspace operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad live vault access can alter, delete, overwrite, restore, export, or expose private Obsidian notes and workspace data.

Mitigation: Use explicit prompts and require confirmation before deletes, overwrites, sync restores, exports, screenshots, plugin or theme installs, and commands targeting private or business vaults.

Risk: Developer and debug commands, including eval-style operations, can run powerful actions against the live Obsidian app.

Mitigation: Restrict debug and eval commands to trusted users and reviewed command text, and avoid running them on sensitive vaults unless the expected effect is clear.

## Reference(s):

- [Obsidian Official CLI Documentation](https://help.obsidian.md/cli)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/justin-202603/skills/obsidian-official-cli-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that read, modify, delete, export, sync, install plugins or themes, capture screenshots, or run debug and eval operations in a live Obsidian vault.]

## Skill Version(s):

1.0.0 (source: server release evidence and CHANGELOG, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
