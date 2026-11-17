## Description:

Read a public website, documentation section, GitHub repository, PDF, or video through llms.ink and answer with source citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukax](https://clawhub.ai/user/lukax)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read public websites, documentation, repositories, PDFs, or videos through llms.ink and prepare source-grounded answers with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper may send local project dependency names to public registries, and it was only partly inspected.

Mitigation: Avoid installing until the helper has been fully inspected and dependency lookup behavior is clarified or removed. If installed, do not use the deps workflow with private or internal dependency names.

## Reference(s):

- [llms.ink Workflows](https://llms.ink/workflows/)
- [ClawHub skill page](https://clawhub.ai/lukax/skills/ink-read-source)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Source-grounded prose with citations, links, and video timestamps when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extraction warnings or missing-evidence notes; full mode covers at most 20 linked pages.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
