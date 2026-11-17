## Description:

Convert HTML and Markdown for web clipping, clean notes, and batch content migration, with support for local files, URLs, batch directories, metadata frontmatter, quality reports, and themed HTML output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and content migration users use this skill to convert HTML files, raw HTML, web pages, Markdown files, and batch directories between Markdown and standalone HTML formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML-to-Markdown script can fetch arbitrary URLs, including batches from URL lists.

Mitigation: Use only trusted URLs and trusted URL-list files, and review network targets before running the skill in shared or sensitive environments.

Risk: The Markdown-to-HTML path can generate active HTML from untrusted Markdown.

Mitigation: Sanitize generated HTML before publishing it or use trusted Markdown only.

Risk: Dependency versions are declared with semver ranges and no pinned lockfile is present in the artifact.

Mitigation: Install with a reviewed, pinned dependency lockfile for repeatable execution.

Risk: The skill text includes unrelated automotive reference links.

Mitigation: Remove or justify unrelated links before publication so users can distinguish converter references from unrelated material.

## Reference(s):

- [Conversion Profiles](references/profiles.md)
- [ClawHub Skill Page](https://clawhub.ai/wangziiiiii/skills/html-to-markdown)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON quality reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write converted Markdown or HTML files and optional JSON quality reports; URL input may fetch remote HTML.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
