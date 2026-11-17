## Description:

Extract and break down content from web documents, PDFs, images, and URLs into structured markdown notes stored locally and synced to Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biohackerrrrrr](https://clawhub.ai/user/biohackerrrrrr)

### License/Terms of Use:


## Use Case:

External users and knowledge workers use this skill to convert URLs, PDFs, screenshots, images, and document text into organized Markdown notes with sections, tags, source attribution, and optional Obsidian syncing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist extracted content to local Markdown files and sync it to an Obsidian vault, which may expose sensitive documents if used without consent.

Mitigation: Require explicit confirmation before processing medical, financial, business, or private documents, and review the destination before saving or syncing.

Risk: The artifact references a hardcoded Obsidian vault path that may be inappropriate for another user's environment.

Mitigation: Update or remove the hardcoded vault path before use and configure any sync destination for the local environment.

## Reference(s):

- [Content Templates](references/content-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/biohackerrrrrr/skills/image-breaker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter and a concise Markdown completion report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves notes to workspace directories and may sync them to Obsidian when enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
