## Description:

Searches Kuaishou public data, lists creator posts, and fetches video comments as structured JSON for competitor research, creator monitoring, KOL screening, content ideation, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketing teams, content operators, and analysts use this skill to retrieve Kuaishou keyword search results, creator public posts, and video comments for trend research, competitive monitoring, KOL screening, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Kuaishou keywords, profile or video URLs, query parameters, and GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use it only when that third-party data exchange is acceptable, and scope tokens and research inputs to the intended task.

Risk: Fetched public-data results are saved locally under logs and may contain sensitive research terms or outputs.

Mitigation: Review and delete local log files when the queried topics, creators, URLs, or retrieved results are sensitive.

Risk: The skill is limited to Kuaishou public data and may return empty or error statuses.

Mitigation: Treat only status success with populated results as usable data, and do not infer private, hidden, deleted, or unavailable content from failed calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/kuai-shou-competitor-research)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Structured JSON results with optional concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful runs include status, request metadata, skill metadata, and results.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
