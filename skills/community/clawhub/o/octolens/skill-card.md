## Description:

Query and analyze brand mentions from the Octolens API across social, developer, and content platforms with filters for source, sentiment, dates, tags, engagement, follower counts, bookmarks, saved views, and keyword tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garrrikkotua](https://clawhub.ai/user/garrrikkotua)

### License/Terms of Use:

MIT

## Use Case:

External developers, marketers, support teams, and product teams use this skill to fetch and analyze Octolens brand mentions, inspect sentiment and engagement, and build filtered mention queries for monitoring, feedback collection, competitor tracking, and campaign analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe setup guidance includes a curl-to-sudo NodeSource installation command.

Mitigation: Provision Node.js through a trusted package manager or verified installer before running the bundled scripts.

Risk: Octolens API keys are shown as command-line arguments, which can expose secrets through shell history or process listings.

Mitigation: Treat API keys as secrets and prefer environment variables, a secret manager, or another protected handoff method.

Risk: Query filters and returned mention data are sent to and processed by Octolens.

Mitigation: Use the skill only with data and monitoring queries approved for processing by Octolens.

Risk: The release under-declares network and code execution needs.

Mitigation: Review permissions before deployment and allow only the Node.js execution and Octolens network access needed for the intended workflow.

## Reference(s):

- [Octolens Skill Page](https://clawhub.ai/garrrikkotua/skills/octolens)
- [Octolens API Base URL](https://app.octolens.com/api/v1)
- [Octolens API Usage Examples](references/EXAMPLES.md)
- [Octolens Filter Reference Guide](references/FILTERS.md)
- [Octolens API Scripts README](scripts/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Octolens API requests, filter JSON, Node.js command invocations, and summarized mention analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
