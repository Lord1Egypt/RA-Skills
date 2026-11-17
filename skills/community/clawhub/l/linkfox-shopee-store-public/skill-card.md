## Description:

Helps agents call Shopee Open Platform Public module endpoints through LinkFox scripts for partner shops, merchants, OAuth token exchange, token refresh, resend-code token retrieval, and Shopee IP ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to guide agent calls to Shopee Public APIs through LinkFox, including partner shop and merchant listing, OAuth token operations, resend-code token retrieval, and Shopee IP allowlist lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can forward Shopee OAuth and partner API data through LinkFox services.

Mitigation: Use it only in a trusted environment, avoid pasting production tokens into examples, and confirm requests are intended before sending OAuth bodies or access tokens.

Risk: Endpoint override environment variables can redirect LinkFox service calls.

Mitigation: Avoid endpoint overrides unless the destination is controlled and trusted.

Risk: Onboarding helpers can create or retrieve a LinkFox API key through SMS login.

Mitigation: Prefer self-service API key retrieval, treat SMS codes and API keys as secrets, and store the resulting key only in a protected environment variable.

Risk: Billing helpers can initiate LinkFox plan orders and payment QR output.

Mitigation: Require explicit user confirmation for plan, payment method, and cost before running billing order commands.

Risk: Generated linkfox output files may contain tokens, API responses, or other sensitive account data.

Mitigation: Protect or clean generated linkfox session files and use summarized output or targeted JSON extraction when full responses are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-public)
- [Shopee Public API index](https://open.shopee.com/documents/v2/v2.public.get_shops_by_partner?module=104&type=1)
- [API reference](references/api.md)
- [Onboarding and billing guidance](references/onboarding.md)
- [get_access_token reference](references/apis/get-access-token.md)
- [refresh_access_token reference](references/apis/refresh-access-token.md)
- [get_shops_by_partner reference](references/apis/get-shops-by-partner.md)
- [get_merchants_by_partner reference](references/apis/get-merchants-by-partner.md)
- [get_token_by_resend_code reference](references/apis/get-token-by-resend-code.md)
- [get_shopee_ip_ranges reference](references/apis/get-shopee-ip-ranges.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct scripts to save full API responses as JSON files under a linkfox session directory while printing full JSON or summaries to stdout.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
