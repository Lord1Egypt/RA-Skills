## Description:

This skill helps agents retrieve and summarize TikTok Shop ERP video performance analytics for authorized shops, including views, sales, orders, and GMV over a requested date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to select an authorized TikTok Shop and request video performance data for a date range. Agents can use the returned analytics to compare shop videos by views, engagement, sales, orders, and GMV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence reports a suspicious verdict because the skill supports TikTok Shop video analytics while also exposing broader proxy and authorization access.

Mitigation: Install only when the publisher and runtime environment are trusted, and prefer the named get_video_performances script over the generic proxy unless broader authorization and analytics access is intentional.

Risk: Gateway environment variables and production API keys could be exposed to untrusted shells.

Mitigation: Review or restrict gateway-related environment variables before use and avoid exposing production API keys outside trusted agent runtimes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-shop-analytics)
- [TikTok Shop ERP Analytics API Reference](references/api.md)
- [Get Authorized Shops](references/apis/get_authorized_shops.md)
- [Get Video Performances](references/apis/get_video_performances.md)
- [TikTok Shop Get Authorized Shops](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309)
- [TikTok Shop Get Video Performances](https://partner.tiktokshop.com/docv2/page/get-video-performances-202403)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a selected authorized shop openId and a start_date/end_date query window; may return paginated analytics results.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
