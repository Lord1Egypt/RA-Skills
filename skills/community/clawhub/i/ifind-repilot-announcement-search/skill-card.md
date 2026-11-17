## Description:

通过自然语言问句语义化搜索A股、基金、港美股公告信息，返回年报、半年报、季报、临时公告、招股说明书等相关公告片段。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenzisay](https://clawhub.ai/user/wenzisay)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and agents use this skill to search company announcements and financial-report disclosures by natural-language query, optionally constrained by a date range. Results are intended to be reorganized into concise summaries that preserve announcement titles, related securities, source links, and important excerpt details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured auth token may be sent to an arbitrary endpoint if the base URL is changed.

Mitigation: Use --set-url only for a destination you fully trust, verify the config keeps base_url on the official repilot.51ifind.com service, and rotate the token if it may have been exposed.

Risk: The skill depends on a local token and remote API availability, so searches can fail with authentication, permission, quota, network, or API errors.

Mitigation: Check token configuration before use, avoid retrying on 401, 403, or 429 responses, and report the returned failure or empty-result state instead of inventing announcement details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenzisay/skills/ifind-repilot-announcement-search)
- [Publisher profile](https://clawhub.ai/user/wenzisay)
- [iFinD RePilot platform](https://repilot.51ifind.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [JSON announcement results summarized as text or Markdown, with shell commands for setup and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured auth token; query results may include announcement titles, summaries, URLs, publication dates, scores, and related stock information.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
