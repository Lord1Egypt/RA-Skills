## Description:

Call GET /api/douyin-xingtu/get-kol-convert-videos-or-products/v1 for Douyin Creator Marketplace (Xingtu) Conversion Resources through JustOneAPI with detailType, kolId, and page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) conversion resources endpoint for a KOL ID, resource detail type, and page. The skill supports commerce analysis and campaign optimization by summarizing endpoint results and then returning raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token can be exposed through process arguments or URL query logs.

Mitigation: Use a narrowly scoped or short-lived token if available, avoid sharing logs or command traces, and rotate the token if exposure is suspected.

Risk: Endpoint responses and backend error payloads may contain data that should not be broadly shared.

Mitigation: Review summaries, raw JSON, and error payloads before sharing them, and redact sensitive identifiers or campaign data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-convert-videos-or-products)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_videos_or_products&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_videos_or_products&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with command examples and raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; required endpoint inputs are detailType, kolId, and page.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
