## Description:

Format and lint markdown files for consistency and readability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to normalize Markdown documents by fixing headings, links, emphasis style, trailing whitespace, and spacing around headings or code fences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: In-place formatting can unexpectedly change Markdown content.

Mitigation: Use the skill only on intended Markdown files under version control or with a backup, then review the diff after running it.

Risk: Generated, sensitive, or code-heavy Markdown documents may be harder to verify after automated formatting.

Mitigation: Avoid using the formatter on those documents until dry-run support and stronger Markdown parsing are available.

## Reference(s):

- [Markdown Heading Syntax](references/heading-syntax.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files modified in place with brief text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on a target Markdown file path; users should review resulting diffs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
