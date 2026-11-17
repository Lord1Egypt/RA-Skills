## Description:

Discover and write typed relationships between Obsidian vault notes. Uses plain Markdown and YAML - no plugins required. Works with any AI agent that has file access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dial481](https://clawhub.ai/user/dial481)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Obsidian vault notes, identify high-value typed relationships, and write approved Markdown/YAML links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read sensitive content in an Obsidian vault while searching for note relationships.

Mitigation: Install and run the skill only against vaults or folders the user is comfortable allowing an agent to read.

Risk: Autonomous relationship writing can add incorrect or unwanted links to important notes.

Mitigation: Keep the default review-before-write workflow for important vaults, and use autonomous mode only on scoped folders or after backing up/versioning the vault.

## Reference(s):

- [Wikilink Types](https://github.com/penfieldlabs/obsidian-wikilink-types)
- [Penfield](https://penfield.app)
- [Penfield OpenClaw Plugin](https://github.com/penfieldlabs/openclaw-penfield)
- [Related ClawHub Obsidian Skill](https://clawhub.ai/steipete/obsidian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML frontmatter and wikilink examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [By default, the skill reports findings for review before modifying vault notes.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
