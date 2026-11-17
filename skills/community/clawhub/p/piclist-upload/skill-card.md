## Description:

Uploads local images referenced in Markdown files to a configured PicList image host through the PicList HTTP Server, then replaces the local image paths with hosted URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Developers, writers, and documentation maintainers use this skill to process Markdown files or directories that contain local image references, upload those images through PicList, and update the Markdown to use cloud-hosted image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Successful uploads delete local image files by default, which can cause data loss if the user did not intend deletion.

Mitigation: Run --dry-run first and use --keep-local unless local file deletion is intentional.

Risk: Processing broad directories or untrusted Markdown can upload unintended local images.

Mitigation: Process only trusted Markdown files and narrow target paths before running in-place updates.

Risk: A PicList HTTP Server exposed beyond localhost can increase unintended access risk.

Mitigation: Configure PicList to listen on 127.0.0.1 rather than 0.0.0.0.

## Reference(s):

- [PicList setup guide](references/setup.md)
- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/piclist-upload)
- [Publisher homepage](https://github.com/cat-xierluo/legal-skills)
- [PicList project](https://github.com/Kuingsmile/PicList)
- [PicList configuration documentation](https://piclist.cn/configure)
- [PicList FAQ](https://piclist.cn/faq)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and processing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces updated Markdown content or in-place Markdown file changes; successful uploads delete local image files by default unless --keep-local is used.]

## Skill Version(s):

1.3.0 (source: frontmatter and changelog, released 2026-09-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
