## Description:

MinerU Document Explorer helps agents read and understand PDF files by initializing documents, browsing outlines, reading selected pages, searching content, and extracting tables, figures, formulas, or headings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rise-1210](https://clawhub.ai/user/rise-1210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to answer questions from PDFs, locate topics, extract document evidence, and work with figures or tables without scanning an entire document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or regulated PDFs may be uploaded to the default public staging service.

Mitigation: Review configuration before use; for sensitive documents, set deployment_mode to local, clear server_url, and avoid the public staging endpoint.

Risk: Local caches or logs may contain document-derived data.

Mitigation: Clear local caches and logs after sensitive work and avoid sharing generated page images or crop files.

Risk: Setup or use may involve optional external services and credentials.

Mitigation: Configure optional services deliberately, use scoped credentials, and do not run setup with elevated privileges.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rise-1210/skills/mineru-document-explorer)
- [Installation & Configuration](artifact/references/setup.md)
- [init Command Reference](artifact/references/cmd-init.md)
- [outline Command Reference](artifact/references/cmd-outline.md)
- [pages Command Reference](artifact/references/cmd-pages.md)
- [search-keyword Command Reference](artifact/references/cmd-search-keyword.md)
- [search-semantic Command Reference](artifact/references/cmd-search-semantic.md)
- [elements Command Reference](artifact/references/cmd-elements.md)
- [Workflows & Lessons Learned](artifact/references/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON CLI result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local page images or crop paths for visual verification.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
