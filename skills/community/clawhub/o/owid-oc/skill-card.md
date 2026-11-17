## Description:

Searches, retrieves, and summarizes content from Our World in Data using the `owid-catalog` Python module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachmann-alexander](https://clawhub.ai/user/rachmann-alexander)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search OWID charts, fetch chart data and metadata, and return concise summaries with attribution links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party `owid-catalog` Python package and its transitive dependencies.

Mitigation: Install it only in a trusted environment, preferably an isolated virtual environment, after accepting that dependency chain.

Risk: OWID lookups are performed in English, which can affect multilingual workflows.

Mitigation: Retrieve the OWID content in English, then translate only the final answer while preserving factual meaning and source attribution.

Risk: The skill relies on the public OWID API and may encounter rate limits or unavailable chart data.

Mitigation: Handle lookup and fetch errors explicitly, refine ambiguous searches, and include the OWID URL so users can verify the source.

## Reference(s):

- [owid-catalog on PyPI](https://pypi.org/project/owid-catalog/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON or concise Markdown summary with source URL attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches should be performed in English; non-English responses should translate the final answer while preserving the retrieved facts.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
