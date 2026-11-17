## Description:

Control a remote Obsidian vault through Fast Note Sync. Use when reading, searching, writing, or appending notes in Obsidian from OpenClaw, especially for remote vault workflows that do not have direct filesystem access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[attack-flower](https://clawhub.ai/user/attack-flower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to search, read, write, append, rename, move, and inspect notes in a remote Obsidian vault through a Fast Note Sync deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify remote Obsidian vault notes through Fast Note Sync.

Mitigation: Install only for vaults and Fast Note Sync servers you trust, read uncertain paths before writing, and use a dedicated test path for exploratory or risky changes.

Risk: Credentials, bearer tokens, and note data may be exposed if configuration files or terminal logs are mishandled.

Mitigation: Use HTTPS endpoints you control, avoid storing passwords in the local config file, protect ~/.config/fast-note-sync/config.json, and treat login output as sensitive.

Risk: Write, replace, rename, move, and restore actions can unintentionally change vault content.

Mitigation: Prefer append when possible, avoid blind overwrites, and review the target path and operation before executing modifying commands.

## Reference(s):

- [obsidian-fns usage reference](references/usage.md)
- [ClawHub skill page](https://clawhub.ai/attack-flower/skills/obsidian-fns)
- [Publisher profile](https://clawhub.ai/user/attack-flower)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can return note content, search result metadata, write status, version, and update timestamps.]

## Skill Version(s):

0.3.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
