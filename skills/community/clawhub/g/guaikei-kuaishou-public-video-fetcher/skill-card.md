## Description:

Retrieves public Kuaishou video search results, creator posts, and video comments through the Guaikei API for trend research, competitor analysis, topic selection, and KOL screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, market analysts, and developers use this skill to collect public Kuaishou search, creator-post, and comment data as structured results for topic research, competitor monitoring, KOL screening, sentiment review, and downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou keywords, profile or video URLs, and the GUAIKEI_API_TOKEN are sent to the third-party Guaikei API service.

Mitigation: Use the skill only when third-party API sharing is acceptable, provide the minimum necessary inputs, and rotate or revoke the token if exposure is suspected.

Risk: Retrieved results are saved locally and may include public comments, usernames, profile or video URLs, and other public interaction data.

Mitigation: Review, protect, or delete the local logs directory when retained results should not remain on disk.

Risk: The skill is limited to public Kuaishou data and does not support private, hidden, or login-only content.

Mitigation: Do not use it for non-public data requests; clarify scope or decline when the requested data requires account access or private content retrieval.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-public-video-fetcher)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands, Guidance]

**Output Format:** [JSON with status, error_code, request, skill_metadata, and results fields; progress and error messages may be emitted separately as text logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and can save retrieved result data to a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact metadata, package.json, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
