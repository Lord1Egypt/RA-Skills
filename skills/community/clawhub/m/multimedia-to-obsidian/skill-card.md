## Description:

Imports PPT, PDF, DOCX, and image files into an Obsidian vault by extracting page images, sending them to a selected multimodal model, and saving generated descriptions as Markdown notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidescend](https://clawhub.ai/user/aidescend)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to convert slide decks, PDFs, Word documents, and image collections into Obsidian Markdown notes with AI-generated visual descriptions for training materials, migrated notes, and structured image knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads extracted document images to external AI services for content understanding.

Mitigation: Use it only with documents approved for the selected provider, avoid confidential or regulated material unless authorized, and use limited-scope API keys.

Risk: Unsafe output category values may affect where files are written in the Obsidian vault.

Mitigation: Use a dedicated test vault first and avoid category values containing slashes, absolute paths, or '..' traversal.

Risk: The MiniMax API host is configurable and could send content to an untrusted endpoint.

Mitigation: Keep MINIMAX_API_HOST set only to a trusted HTTPS provider before running the skill.

Risk: Cleanup behavior and document conversion commands should be reviewed before use.

Mitigation: Run the skill in an isolated environment with backups of the target vault.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aidescend/skills/multimedia-to-obsidian)
- [Publisher profile](https://clawhub.ai/user/aidescend)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and command-line instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Markdown files into the selected Obsidian vault/category and requires API credentials for the selected multimodal provider.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
