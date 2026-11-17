## Description:

Publishes Markdown content to Notion, GitHub Wiki, Medium, or local HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to publish or preview Markdown content across GitHub Wiki, Notion, Medium, and local HTML outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package is incomplete and directs users toward an external publishing script for a credentialed workflow.

Mitigation: Verify the actual publish implementation from a trusted source, avoid the external clone path unless trusted, and run dry-run mode before publishing.

Risk: Publishing workflows can expose tokens, private Markdown content, or embedded image data to GitHub, Notion, Medium, or image hosting.

Mitigation: Use least-privilege platform tokens and review Markdown files and embedded images for secrets or private data before publishing.

## Reference(s):

- [Markdown Sync Pro on ClawHub](https://clawhub.ai/antonia-sz/skills/markdown-sync-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and platform configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish content to external platforms or export local HTML, depending on selected command options.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
