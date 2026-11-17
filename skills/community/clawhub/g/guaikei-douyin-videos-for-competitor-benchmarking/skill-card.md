## Description:

This skill helps agents retrieve public Douyin keyword search results, creator posts, video comments, and trending topics for content research, competitor benchmarking, sentiment analysis, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content researchers, and developers use this skill to collect and structure public Douyin data for short-video topic research, competitor account monitoring, comment analysis, and real-time trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, profile or video URLs, and a GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Use a limited or revocable token, treat it as sensitive, and avoid confidential research unless the data-sharing behavior is acceptable.

Risk: Generated logs can retain research queries and collected Douyin data locally.

Mitigation: Review retention needs before use and delete generated logs when they are no longer required.

Risk: Broad triggering can run the skill during generic competitor or content-research requests even when Douyin was not explicitly requested.

Mitigation: Confirm the intended platform before execution when the user request is ambiguous or sensitive.

Risk: Server security evidence reports credential handling, broad auto-triggering, local data retention, and runtime messages as less safe than the documentation claims.

Mitigation: Review the security summary and runtime behavior before installation, and install only if those risks are acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-videos-for-competitor-benchmarking)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei token and support site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [JSON on stdout, diagnostic text on stderr, and JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and Node.js >= 16.14.0; task logs are written under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
