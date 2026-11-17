## Description:

Build focused queries with exact phrases and source domains before researching a question.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use the skill to prepare focused search queries with exact phrases and optional source domains before conducting research. It helps structure a search plan and local report; live searches and source verification are handled separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated query text remains in local reports and could expose private information if included in a query.

Mitigation: Keep private information out of public searches and review queries before searching; limit access to local reports containing sensitive query text.

Risk: A prepared query plan does not provide search results or verify claims.

Mitigation: Run searches with an available authorized tool and verify current claims against original sources before reporting results.

## Reference(s):

- [Input contract](references/input.md)
- [中文用法](references/zh-CN.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-search-planner)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON query plan with raw and URL-encoded search queries; local JSON report and artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper works offline and does not perform live searches or verify results. It saves query text in local reports.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
