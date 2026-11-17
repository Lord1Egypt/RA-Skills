## Description:

Routes natural-language Douyin research requests to Node.js CLI tools for public keyword search, author post collection, video comment lookup, and hot trend retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn Douyin content research requests into structured lookups for marketing research, competitor monitoring, comment analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security evidence flags unsafe API token handling, including authentication in query strings.

Mitigation: Use a low-privilege, revocable GUAIKEI_API_TOKEN, rotate it after testing, and update the implementation to avoid sending authentication in query strings.

Risk: Search terms, Douyin URLs, and result requests are sent to www.guaikei.com, and result JSON files are saved locally by default.

Mitigation: Avoid sensitive inputs, treat returned data and logs as local artifacts requiring retention controls, and clear or isolate the logs directory when needed.

Risk: The security summary reports runtime authentication errors that contradict the stated neutral-error policy.

Mitigation: Review stderr before exposing output to end users and remove runtime contact or promotional messages from authentication error paths.

## Reference(s):

- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI request schema](assets/post_cli_req.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI request schema](assets/comment_cli_req.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)
- [Guaikei service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout with stderr logs and local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; commands query Douyin public data through www.guaikei.com; documented limit is up to 10000 records per request.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
