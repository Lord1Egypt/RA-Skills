## Description:

Retrieves public Kuaishou video search results, creator posts, and video comments through command-line workflows so an agent can return structured data for content research, competitor monitoring, KOL screening, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, marketers, analysts, and agent developers use this skill to collect public Kuaishou search results, creator post lists, and video comments as structured JSON for topic research, trend monitoring, competitor review, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says users may be prompted to print or expose a real GUAIKEI_API_TOKEN during troubleshooting.

Mitigation: Verify only that GUAIKEI_API_TOKEN is set and valid; do not print, paste, screenshot, log, or share the token value.

Risk: Fetched Kuaishou results are automatically retained in the skill's local logs/ directory.

Mitigation: Review retention needs before use and delete logs/ files when saved search results, creator data, or comments should not remain on disk.

Risk: The security evidence marks the release as suspicious because advertised retrieval behavior is paired with credential-handling and local-retention concerns.

Mitigation: Review the skill before installation or execution, especially in environments that use real API credentials or handle sensitive analysis outputs.

Risk: The skill sends requests and the GUAIKEI_API_TOKEN to the third-party Guaikei API service.

Mitigation: Use only authorized public Kuaishou data and confirm that the API provider, token terms, and data-transfer posture are acceptable for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/kuaishou-detail)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON command output with status, error_code, request, skill_metadata, and results fields; agent-facing responses may summarize results in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GUAIKEI_API_TOKEN environment variable and writes fetched results to the local logs/ directory.]

## Skill Version(s):

1.0.0 (source: evidence release, frontmatter, package.json, and changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
