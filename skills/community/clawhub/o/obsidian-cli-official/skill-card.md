## Description:

Official Obsidian CLI (v1.12+) providing a complete command-line interface for Obsidian notes, tasks, search, tags, properties, links, and related vault operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexanderkinging](https://clawhub.ai/user/alexanderkinging)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let agents operate Obsidian vaults through the official CLI for note creation, search, task management, metadata, links, publishing, plugin and theme management, and workspace automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can operate broadly on a user's Obsidian vault and configuration.

Mitigation: Use explicit vault and file or path limits, and require confirmation before writes, deletes, restores, publishing, plugin or theme changes, eval, or DevTools commands.

Risk: CLI wrappers or Homebrew taps can affect the command surface used by an agent.

Mitigation: Prefer trusted and pinned installation sources for any CLI wrapper or Homebrew tap.

## Reference(s):

- [Official Obsidian CLI documentation](https://help.obsidian.md/cli)
- [ClawHub skill page](https://clawhub.ai/alexanderkinging/skills/obsidian-cli-official)
- [Obsidian download](https://obsidian.md/download)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reference material with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Obsidian 1.12+ running locally with CLI enabled; some commands require an optional Obsidian Publish subscription.]

## Skill Version(s):

4.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
