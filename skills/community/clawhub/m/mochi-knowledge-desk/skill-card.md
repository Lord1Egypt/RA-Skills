## Description:

Incrementally index local documents, search Chinese and English text, and return source snippets with file hashes. Use for Local Knowledge Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users can use the skill in an agent workspace to incrementally index selected local documents, search Chinese and English content, verify source freshness, and export an index manifest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexed document text remains in the local database after source files disappear.

Mitigation: Select only folders you want indexed, remove unwanted index entries, and separately delete exported reports when needed.

## Reference(s):

- [Action contract](references/input.md)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-knowledge-desk)
- [Publisher homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML reports, Files]

**Output Format:** [Search snippets and citations, JSON results, and local JSON or HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs and persistent index data remain in the active workspace; search uses lexical ranking.]

## Skill Version(s):

1.0.1 (source: frontmatter metadata, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
