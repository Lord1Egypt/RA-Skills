## Description:

Searches and reads web, news, video, and image results through Brave Search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to search Brave's web, news, video, and image indexes and read the returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run remote installers, while external installer payloads and CLI binaries were not assessed.

Mitigation: Review setup before installing, install a verified CLI release yourself, and separately approve the OOMOL connection.

Risk: Search queries pass through OOMOL.

Mitigation: Avoid submitting queries that contain information you do not want passed through OOMOL.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Brave Search](https://search.brave.com/)
- [Brave Search API documentation](https://api-dashboard.search.brave.com/app/documentation)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON search results and text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are returned for the requested query and action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
