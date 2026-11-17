## Description:

Retrieves published local news, meeting transcripts, sources, and upcoming civic events from a Communities News newsroom to support research and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alaskanews](https://clawhub.ai/user/alaskanews)

### License/Terms of Use:

MIT-0

## Use Case:

Community journalists, bloggers, and civic writers use this skill to locate prior coverage, check public meeting records and deadlines, and gather cited source material before writing their own stories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed newsroom API key could allow others to read accessible content or consume its rate limit.

Mitigation: Use a read-only key where possible, keep local credential files trusted, and revoke a leaked key.

Risk: Article URLs supplied to the tool are fetched from the network.

Mitigation: Use article URLs from trusted newsroom sources and review the destination before fetching.

Risk: Saving a research brief to an existing path replaces that file.

Mitigation: Choose and check the output path before requesting a saved brief.

Risk: Reusing newsroom reporting without checking its terms or attribution may misrepresent permitted use.

Mitigation: Review the newsroom terms shown in the output and attribute reporting with a link to the source.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alaskanews/skills/local-news-api)
- [Communities News](https://communities.news)
- [Alaska News API specification](https://alaskanews.com/api/v1/openapi.json)
- [Output and attribution guidance](references/output.md)
- [Access verification](references/verification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown by default; JSON on request; optional local Markdown research brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, newsroom usage terms, and suggested next steps; a brief is saved only when an output path is requested.]

## Skill Version(s):

1.6.2 (source: SKILL.md metadata and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
