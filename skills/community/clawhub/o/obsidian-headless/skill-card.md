## Description:

Manages an Obsidian notes vault from headless or SSH environments with commands for creating, viewing, deleting, searching, listing, and appending daily notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imakid](https://clawhub.ai/user/imakid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and note-taking users use this skill to manage Markdown notes in an Obsidian vault on headless servers, SSH sessions, containers, or other environments without the Obsidian desktop GUI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, create, append, and delete Markdown files in the configured Obsidian vault.

Mitigation: Use a dedicated or backed-up vault until the operator has reviewed the shell scripts and confirmed the target vault path.

Risk: Search command handling is flagged by security evidence as vulnerable to rg/grep option injection with untrusted natural-language input.

Mitigation: Avoid untrusted search terms and review or patch search argument handling before installing in shared or automated environments.

Risk: Installation and configuration can persist shell profile/PATH changes and store a world-readable vault path.

Mitigation: Review installer changes before use, prefer the OBSIDIAN_VAULT environment variable for temporary configuration, and restrict config file permissions if the vault path is sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imakid/skills/obsidian-headless)
- [Obsidian](https://obsidian.md/)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Artifact-declared repository](https://github.com/imakid/obsidian-headless)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown notes and terminal text from shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes, reads, searches, lists, and deletes Markdown files inside the configured Obsidian vault.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
