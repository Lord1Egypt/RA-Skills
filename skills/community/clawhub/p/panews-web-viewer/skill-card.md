## Description:

Read public PANews website pages as Markdown for homepage, article-page, and column-page reads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medz](https://clawhub.ai/user/medz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve public PANews homepage, article, and column pages as Markdown with page metadata when they need rendered page content rather than structured search or API results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make direct web requests to PANews when a page-reading task is invoked.

Mitigation: Use it for public single-page reads only, not authenticated accounts, private data, write actions, broad crawling, or structured API search workflows.

## Reference(s):

- [PANews Website](https://www.panewslab.com)
- [PANews Web Viewer on ClawHub](https://clawhub.ai/medz/skills/panews-web-viewer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with YAML frontmatter metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public PANews page content and metadata for supported locale-prefixed homepage, article, or column URLs.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
