## Description:

Poetry helps agents generate classical Chinese poems and query a local chinese-poetry dataset by author, title, keyword, dynasty, and related literary criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create classical Chinese poetry, retrieve poems from a local corpus, compare literary themes, and analyze authors, forms, imagery, and styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script downloads the public chinese-poetry dataset from GitHub without pinning or verifying an exact revision.

Mitigation: For reproducible or high-integrity deployments, pin a reviewed dataset commit or verify the downloaded dataset before use.

## Reference(s):

- [chinese-poetry dataset](https://github.com/chinese-poetry/chinese-poetry)
- [Poetry skill on ClawHub](https://clawhub.ai/wscats/skills/poetry)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with poetry, query results, analysis, and occasional shell commands for dataset setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on a separately downloaded local chinese-poetry dataset for retrieval-oriented responses.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
