## Description:

Aggregates multiple search sources with fallback routing and cross-source verification to improve search reliability and compare findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruogu1992](https://clawhub.ai/user/ruogu1992)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route search, research, and fact-checking requests across multiple sources, compare results, and surface confidence or disagreement in the response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad search-like prompts may activate the skill and route the query to multiple search providers.

Mitigation: Avoid private or sensitive queries unless multi-provider exposure is acceptable, and scope prompts clearly when multi-source search is not desired.

Risk: Search providers may return conflicting or incomplete results.

Mitigation: Review the skill's confidence labels, source comparison, and disagreement notes before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruogu1992/skills/multi-search-fallback)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown search report with confidence level, key findings, source comparison, and grouped raw results when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source-level agreement, disagreement, or supplemental-result labels.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
