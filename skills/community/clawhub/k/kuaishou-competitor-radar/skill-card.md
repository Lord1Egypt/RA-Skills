## Description:

Compare brands' content performance, engagement metrics, and discussion trends on Kuaishou using public video, creator, and comment data, with evidence and actionable opportunities for benchmarking and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Brand, marketing, and research teams use the skill to search public Kuaishou videos, review creator posts and comments, and compare content performance or discussion trends. It returns structured evidence that an agent can use to summarize competitor differences and identify content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send the supplied keywords or Kuaishou links to the third-party GuaiKei service.

Mitigation: Use public, non-sensitive keywords and links, and confirm that sending them to the service is acceptable for the task.

Risk: The supplied security assessment reports medium confidence, partial inspection of 12 of 32 components, and degraded tool-misuse analysis.

Mitigation: Review the scripts that were not fully assessed and obtain a complete security scan before installation where needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-competitor-radar)
- [GuaiKei service and API access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis]

**Output Format:** [Structured JSON containing public video, creator, or comment data; an agent may summarize it as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-data queries require a GUAIKEI_API_TOKEN and send the submitted keyword or link to the GuaiKei service. Results and request limits depend on the token plan.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
