## Description:

Builds the gauntlet knowledge base from AST extraction and AI enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build or refresh a codebase knowledge base, enriching extracted entries and linking related information across modules. It saves the result as `.gauntlet/knowledge.json` and reports category counts and coverage gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some references to a local knowledge file did not match bundled files, so review of its expected behavior is incomplete.

Mitigation: Check whether the referenced local files are expected in the target project, then review the generated knowledge base before relying on it.

## Reference(s):

- [Gauntlet plugin homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown]

**Output Format:** [JSON knowledge base and a text summary report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes `.gauntlet/knowledge.json`; the report includes category counts, coverage gaps, and difficulty distribution.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
