## Description:

Turns conversations, project materials, meeting notes, troubleshooting records, web articles, and local documents into structured Obsidian knowledge-base notes with Properties, key takeaways, summaries, references, and internal note links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojiangyong](https://clawhub.ai/user/luojiangyong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert conversations, project materials, URLs, WeChat articles, and local documents into durable Obsidian Markdown notes that preserve source context, reusable insights, and vault relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated notes can persist conversation details, source links, and user-approved sensitive text into an Obsidian vault.

Mitigation: Review generated notes before write-back, especially when the source material contains confidential project or meeting content.

Risk: Notes may accidentally store live API keys, cookies, bearer tokens, private invite links, or tokenized URLs.

Mitigation: Avoid saving these values in notes, particularly when the vault syncs or is shared.

Risk: Vault read/write access can expose or modify personal knowledge-base content.

Mitigation: Grant vault access only when needed and read back generated notes to verify the expected content was written.

## Reference(s):

- [Obsidian Notes ClawHub Skill Page](https://clawhub.ai/luojiangyong/skills/obsidian-notes-skill)
- [Obsidian Note Template](references/note-template.md)
- [Obsidian Note Types](references/note-types.md)
- [Obsidian Source Types](references/source-types.md)
- [Obsidian Note Style Guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Obsidian Markdown notes with YAML Properties, callouts, structured sections, Key references, and internal wiki links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write to an Obsidian vault through MCP or Local REST API when available; otherwise provides Markdown for manual insertion.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
