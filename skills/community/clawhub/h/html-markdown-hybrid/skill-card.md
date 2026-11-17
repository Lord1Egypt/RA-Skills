## Description:

Converts Markdown into styled standalone HTML and converts HTML files, raw HTML, URLs, and directories into clean Markdown with cleanup profiles, metadata, reports, and batch modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[520xiaomumu](https://clawhub.ai/user/520xiaomumu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and content engineers use this skill to choose and run Markdown-to-HTML or HTML-to-Markdown conversion workflows for readable pages, cleaned article or documentation extracts, batch conversions, metadata frontmatter, and quality reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML-to-Markdown workflow can fetch arbitrary URLs, which may expose private services or cloud metadata if run in a permissive network environment.

Mitigation: Run URL conversion in a network-restricted environment, avoid internal or metadata endpoints, and use allowlisted sources for bulk URL jobs.

Risk: Generated HTML from untrusted Markdown or converted content may contain unsafe active content when opened or published.

Mitigation: Only open or publish generated HTML from trusted input, or sanitize the HTML before distribution.

Risk: The release was flagged for review because hostile input and dependency age can affect conversion safety at scale.

Mitigation: Review dependencies before bulk use, scan outputs from untrusted sources, and follow the server guidance for hostile input handling.

## Reference(s):

- [Conversion Profiles](references/profiles.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; scripts can emit HTML files, Markdown files, and JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file, raw-string, directory, and URL-list conversion modes; Node dependencies are required for the Node conversion pipeline.]

## Skill Version(s):

1.1.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
