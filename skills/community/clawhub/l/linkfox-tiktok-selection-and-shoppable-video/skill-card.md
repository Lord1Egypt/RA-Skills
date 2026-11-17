## Description:

One-stop TikTok product-selection and shoppable-video toolkit that helps agents use EchoTik, FastMoss, and TikTok official video APIs for product research, trend analysis, promotional-video analysis, creator authorization, and shoppable-video publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and commerce teams use this skill to research TikTok Shop products and trends, analyze promotional videos and creator performance, and guide authorized shoppable-video publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives broad credential-bearing API access with weak endpoint and credential-storage controls.

Mitigation: Install only when LinkFox and the runtime are trusted, keep credentials in a scoped secret store, and do not override LINKFOX_TOOL_GATEWAY or related API URL variables to untrusted hosts.

Risk: Video posting and related commerce actions can affect external TikTok accounts.

Mitigation: Treat OAuth authorization, uploads, pre-checks, publishing, and status checks as user-approved actions before running the relevant scripts.

Risk: Full API responses and cached results may contain account, product, token, or commerce data.

Mitigation: Review generated response files before sharing them and avoid placing full API keys or sensitive tokens in chat, shell history, or shell startup files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-selection-and-shoppable-video)
- [EchoTik TikTok new product ranking](references/linkfox-echotik-list-new-product-rank.md)
- [EchoTik TikTok product search](references/linkfox-echotik-list-product.md)
- [EchoTik TikTok batch product detail](references/linkfox-echotik-batch-product-detail.md)
- [EchoTik TikTok product video](references/linkfox-echotik-product-video.md)
- [EchoTik TikTok video download URL](references/linkfox-echotik-get-video-download-url.md)
- [FastMoss TikTok top-selling product rank](references/linkfox-fastmoss-product-rank-top-selling.md)
- [FastMoss TikTok product search](references/linkfox-fastmoss-product-search.md)
- [TikTok video authorization and token management](references/linkfox-tiktok-video-auth.md)
- [TikTok shoppable video API](references/linkfox-tiktok-video.md)
- [TikTok sellable product query](references/linkfox-tiktok-video-products.md)
- [Shoppable video large file upload](references/large-file-upload.md)
- [TikTok Partner Center shoppable video large file upload](https://partner.tiktokshop.com/docv2/page/shoppable-video-large-file-upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request and response examples; scripts write JSON response files and may print summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LinkFox API credentials; external API calls may consume credits and can publish shoppable videos when explicitly invoked.]

## Skill Version(s):

1.2.3 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
