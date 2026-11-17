## Description:

Fetches public Kuaishou keyword search results, creator posts, and video comments through the Guaikei API for competitor research, content analysis, topic discovery, and brand content investigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content operators, creators, MCNs, brand teams, and analysts use this skill to retrieve structured public Kuaishou data for search analysis, creator monitoring, comment review, and follow-on reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Kuaishou keywords, creator or video identifiers, request parameters, and GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use the skill only when that data transfer is acceptable for the workspace, and scope the API token to the intended use where possible.

Risk: Generated local logs may contain sensitive research context, queried URLs, public comments, author details, and keywords.

Mitigation: Store logs in an approved location, restrict access, and delete or archive them according to the user's data retention requirements.

Risk: The skill retrieves only public Kuaishou data and may return empty or error results for invalid links, deleted content, unavailable content, or API failures.

Mitigation: Check the returned status and error code before analysis, avoid fabricating missing data, and ask for a corrected keyword, video URL, creator profile URL, or user ID when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-search-detail-fetcher)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and writes local result logs that may contain queried keywords, Kuaishou URLs, author details, comments, and request metadata.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, package.json, release evidence, changelog released 2026-08-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
