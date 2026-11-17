## Description:

Discover and analyze Instagram users and content through the KeyAPI REST API using live official docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn Instagram research goals into KeyAPI REST workflows for profile, content, comment, hashtag, music, Explore, location, follower, and related-account analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can persist a KeyAPI bearer token in shell startup files.

Mitigation: Prefer a per-session environment variable or secure credential store, and review any shell profile changes before installation.

Risk: Passing bearer tokens on the command line can expose credentials through shell history or process inspection.

Mitigation: Use interactive setup or environment-based authentication instead of command-line token arguments.

Risk: Follower, story, comment, and exported response data may include sensitive or high-volume social data.

Mitigation: Keep collection narrowly scoped, confirm broad report scope before execution, and delete exported response files when no longer needed.

## Reference(s):

- [KeyAPI Documentation Index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI Instagram Documentation](https://docs.keyapi.ai/en/instagram/)
- [KeyAPI Authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [Global Rules](references/global-rules.md)
- [Scenario Cards](references/scenarios.md)
- [Routing Policy](references/routing-policy.md)
- [Instagram Rules](references/instagram-rules.md)
- [Instagram User Module Rules](references/instagram-user-rules.md)
- [Instagram Content Module Rules](references/instagram-content-rules.md)
- [Instagram Discovery Module Rules](references/instagram-discovery-rules.md)
- [Setup And Auth](references/setup-and-auth.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown responses with inline shell commands and optional JSON result previews or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live requests require a KeyAPI bearer token and current endpoint documentation should be resolved before calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
