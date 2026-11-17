## Description:

品氪 OpenApi 开放平台 Skill helps agents call Pinkr OpenAPI endpoints to synchronize and manage CRM/SCRM data for stores, guides, members, orders, refunds, inventory, products, points, stored value, coupons, sales, marketing, and distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikaijian](https://clawhub.ai/user/ikaijian)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and integration operators use this skill to issue authenticated Pinkr OpenAPI requests for CRM/SCRM data synchronization, lookup, and updates across member, order, inventory, product, coupon, sales, marketing, and distribution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive customer and business records may be returned by API calls and saved locally.

Mitigation: Use the skill only in trusted workspaces, protect or disable local output saving where possible, and regularly clean saved result files.

Risk: The API endpoint can use insecure transport if PK_API_URL is left on an HTTP URL.

Mitigation: Set PK_API_URL to a validated HTTPS endpoint before use.

Risk: The skill can perform write operations using the authority granted to PK_APPKEY.

Mitigation: Use tightly scoped PK_APPKEY permissions and require explicit human review before write, upload, or status-change operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ikaijian/skills/pinkr-openapi-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/ikaijian)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON, with guidance that may include Markdown-style command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper can save formatted text and raw JSON API responses as local output files when run.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
