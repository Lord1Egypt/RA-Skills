## Description: <br>
Temu US e-commerce promotion API skill that routes Partner US Promotion campaign, enrollment, query, coupon, and flash-sale related Temu bg/temu interfaces through the LinkFox gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Temu sellers, operators, and developers use this skill to query US promotion activities, inspect candidate and enrolled goods, enroll goods in promotions, poll operation results, and update promotion goods through LinkFox-mediated Temu APIs. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LinkFox and Temu seller credentials, including sensitive tokens that may authorize account-level actions. <br>
Mitigation: Use it only when the publisher and LinkFox are trusted with those credentials, prefer narrowly scoped Temu tokens, and avoid exposing secrets in shell history or shared logs. <br>
Risk: The generic proxy and file-download helpers may permit broader Temu API activity than the promotion workflow alone. <br>
Mitigation: Review requests before execution, limit use to the intended promotion APIs, and avoid saving access tokens unless necessary. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-temu-promotion-us) <br>
- [LinkFox publisher profile](https://clawhub.ai/user/linkfox-ai) <br>
- [API reference](references/api.md) <br>
- [Temu access token authorization](references/access-token.md) <br>
- [Partner US catalog](references/partner-us-catalog.md) <br>
- [Promotion API index](references/apis/README.md) <br>
- [Temu Partner US API documentation](https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LinkFox API key and either a Temu accessToken or a saved storeKey for authenticated calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
