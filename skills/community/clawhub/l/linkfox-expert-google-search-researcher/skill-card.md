## Description:

谷歌搜索专家面向跨境电商调研，通过 Google AI Mode 获取带引用的 AI Overview，用于海外消费者偏好、产品趋势、市场问题、技术趋势和追问式网页调研。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, product researchers, and brand teams use this agent to ask single-round Google AI Mode research questions, review cited Markdown summaries, and save longer market or product-trend findings as HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can expose LinkFox API keys through command output or logs.

Mitigation: Treat API keys as secrets, avoid sharing logs that may contain keys, and rotate any key that may have been exposed.

Risk: Custom LINKFOX_* gateway variables can redirect requests away from trusted LinkFox endpoints.

Mitigation: Use trusted LinkFox endpoints and avoid gateway overrides unless they have been reviewed.

Risk: SMS-code onboarding and payment flows can create account or billing actions.

Mitigation: Run SMS, order, or payment commands only after explicit user initiation and verify the plan, method, and amount before proceeding.

Risk: The file upload helper publishes local files to public URLs.

Mitigation: Upload only files confirmed safe for public access and avoid private, sensitive, or regulated data.

Risk: Live AI Overview research can vary by query wording, locale, and Google availability.

Mitigation: Preserve source citations, disclose recency when relevant, and report empty results instead of fabricating missing AI Overview content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-google-search-researcher)
- [Google AI search API reference](artifact/skills/linkfox-ai-mode-google-search/references/api.md)
- [Google AI search onboarding guidance](artifact/skills/linkfox-ai-mode-google-search/references/onboarding.md)
- [AI text generation API reference](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)
- [Analysis report layout reference](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with citations, JSON tool responses, and HTML report file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live Google AI Overview results can vary; large responses may be saved to local files; public uploads require explicit sensitivity review.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
