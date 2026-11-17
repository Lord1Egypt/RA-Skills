## Description:

Supports Douyin public-data reconnaissance for short-video sentiment and reputation monitoring by searching keywords, collecting creator posts and video comments, and tracking hot lists; it does not cover news-media sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and marketing or brand teams use this skill to collect structured public Douyin search, creator-post, comment, and hot-list data for content planning, competitor analysis, and sentiment monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI API tokens may be exposed because the security evidence says tokens are placed in request URLs.

Mitigation: Use least-privilege or disposable tokens where possible, avoid running through shared logging proxies, and rotate any token that may have been retained in server or proxy logs.

Risk: Collected Douyin data is saved locally under the skill's logs directory by default.

Mitigation: Limit collection to data needed for the task, protect or delete generated logs, and avoid storing sensitive investigation context with exported results.

Risk: The security summary reports that runtime behavior may contradict the stated promise not to show promotional contact information.

Mitigation: Review outputs before acting on error or support messages, and do not follow unexpected promotional contact instructions from the tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-recon)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Guaikei token and help site](https://www.guaikei.com)
- [Search request schema](artifact/assets/search_cli_req.schema.json)
- [Search response schema](artifact/assets/search_cli_resp.schema.json)
- [Post request schema](artifact/assets/post_cli_req.schema.json)
- [Post response schema](artifact/assets/post_cli_resp.schema.json)
- [Comment request schema](artifact/assets/comment_cli_req.schema.json)
- [Comment response schema](artifact/assets/comment_cli_resp.schema.json)
- [Hot list response schema](artifact/assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout with logs and status messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-run CLI responses; up to 10,000 records per collection task; logs saved under logs/ by default.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
