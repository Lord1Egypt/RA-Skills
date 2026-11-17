## Description:

Obsidian Clipper saves web content such as articles, videos, notes, and social posts to an Obsidian vault with automatic classification, naming, extraction, and Markdown generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyeasy](https://clawhub.ai/user/flyeasy)

### License/Terms of Use:

MIT-0

## Use Case:

External Obsidian users and agent operators use this skill to collect links, notes, videos, and articles into a configured Obsidian vault as organized Markdown notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-writing instructions are loosely scoped, so generated paths or categories could place content outside the intended Obsidian vault.

Mitigation: Configure an explicit vault path, use trusted destination categories, and verify that saved files remain inside the intended vault before routine use.

Risk: The artifact ships a personal local configuration with a vault path and collector name.

Mitigation: Replace the bundled configuration with the user's own vault path and collector name before first use.

Risk: Web content extraction can be incomplete on platforms with login walls or unsupported parsing paths.

Mitigation: Review generated summaries and provide copied text or screenshots when automated fetch, search, or browser extraction cannot capture the source.

## Reference(s):

- [Obsidian Clipper ClawHub Skill Page](https://clawhub.ai/flyeasy/skills/obsidian-clipper)
- [Obsidian Clipper GitHub Repository](https://github.com/flyeasy/obsidian-clipper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, concise text responses, shell command blocks, and JSON configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes collected content to a user-configured Obsidian vault path and reports the saved path and key points.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
