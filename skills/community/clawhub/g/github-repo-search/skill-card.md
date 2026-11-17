## Description:

Helps users search and filter public GitHub open-source repositories and returns a structured recommendation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackhua6](https://clawhub.ai/user/jackhua6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical evaluators use this skill to turn a repository-search request into confirmed requirements, GitHub search queries, filtered candidates, and a structured Top N recommendation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad GitHub or open-source search requests may trigger the workflow and produce recommendations based on live public search results.

Mitigation: Require user confirmation of topic, result count, minimum stars, sorting mode, and target repository type before searching.

Risk: Repository recommendations may become stale or difficult to reproduce because GitHub search results, repository metadata, and API quota state can change.

Mitigation: Record the search time, quota status, filtering rules, and repository metadata in the final report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackhua6/skills/github-repo-search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes search requirements, query list, filtering rules, repository ranking, and brief risk notes when relevant.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
