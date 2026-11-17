## Description:

Produce a focused literature/knowledge review using only selected Research KB contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Research KB users use this skill to generate source-grounded literature reviews, thematic syntheses, method comparisons, and research-gap analyses from selected personal or team knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an admin Gitea token and can write generated review files to caller-selected repositories by default.

Mitigation: Use a tightly scoped Gitea service token, enforce server-side validation of allowed knowledge-base repositories, and require explicit opt-in before writing review files.

Risk: Dependency and environment setup may drift before deployment.

Mitigation: Pin dependencies and remove unused python-dotenv before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-literature-review)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Single JSON object containing a source-grounded answer, citations, used scopes, read pages, mode, and optional generated review path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a Markdown review file to the first selected knowledge-base repository when writeReview is not false.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
