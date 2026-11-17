## Description:

Scan a directory of Markdown files, extract titles/headings/frontmatter, build a searchable index JSON, and output a concise summary report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and knowledge-base operators use this skill to inventory folders of Markdown notes, docs, or wikis and generate searchable JSON plus an optional Markdown catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated index files can expose filenames, titles, headings, line counts, and frontmatter signals from private Markdown collections.

Mitigation: Treat index.json and catalog.md as sensitive when the source documents are private.

Risk: The example shell pipeline has minor safety caveats when processing untrusted filenames or headings.

Mitigation: Review and harden JSON escaping before using the sample command on untrusted document collections.

Risk: The upload example can send indexed metadata to a remote service.

Mitigation: Inspect and replace any upload URL before using the curl example.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/markdown-indexer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with bash, jq, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local index.json output and optional catalog.md output; requires jq.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
