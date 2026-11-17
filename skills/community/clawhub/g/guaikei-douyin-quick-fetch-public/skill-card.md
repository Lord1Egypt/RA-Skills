## Description:

Collects public Douyin data through keyword search, creator post fetches, video comment retrieval, and real-time hot-list queries, returning structured JSON for content research, competitor analysis, public opinion review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content or marketing teams use this skill to run Node.js CLI commands that query Guaikei for public Douyin search results, creator posts, comments, and hot-list data. It is not intended for publishing or editing videos, downloading watermark-free media, accessing private content, or collecting data from other platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin queries, target URLs, and GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Install and run it only when that data transfer is acceptable; keep the token in the environment, avoid exposing it in shared sessions, and rotate it if it may have been disclosed.

Risk: Fetched public data is saved locally under logs/.

Mitigation: Review local log contents before sharing the workspace, delete logs that are no longer needed, and avoid queries that could collect data outside the intended Douyin research scope.

Risk: The release is intended for public Douyin data research and may be unsuitable for ambiguous or non-Douyin collection requests.

Mitigation: Use it only for lawful public Douyin research, trend tracking, competitor analysis, and comment review; do not use it for private content, other platforms, or unauthorized redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-quick-fetch-public)
- [Guaikei token and help portal](https://www.guaikei.com)
- [Complete options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Search CLI request schema](artifact/assets/search_cli_req.schema.json)
- [Search CLI response schema](artifact/assets/search_cli_resp.schema.json)
- [Post CLI request schema](artifact/assets/post_cli_req.schema.json)
- [Post CLI response schema](artifact/assets/post_cli_resp.schema.json)
- [Comment CLI request schema](artifact/assets/comment_cli_req.schema.json)
- [Comment CLI response schema](artifact/assets/comment_cli_resp.schema.json)
- [Hot CLI response schema](artifact/assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Pure JSON on stdout, operational logs on stderr, and timestamped JSON files saved under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; command limits are documented up to 10000 records per request.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, references/changelog.md, src/config/constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
