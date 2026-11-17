## Description:

卖家之家(跨境电商)服务产品搜索与发布

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and service providers use this skill to search MJZJ mall service products, filter results by labels, provider, price, or language, upload product images, and submit new product applications for backend review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated upload and product-application flows can act on the MJZJ seller account associated with MJZJ_API_KEY.

Mitigation: Confirm the API key belongs to the intended seller account before uploading files or submitting a product application.

Risk: Incorrect product details, labels, images, prices, or sale windows could be submitted for backend review.

Mitigation: Review the product title, intro, label choices, files, prices, and sale times before calling the product-application endpoint.

Risk: Snowflake-style IDs can lose precision if handled as numbers.

Mitigation: Treat id fields, providerId, labelIds entries, and nextPosition as strings end to end.

## Reference(s):

- [MJZJ Mall homepage](https://mall.mjzj.com)
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-mall)
- [MJZJ API key page](https://mjzj.com/user/agentapikey)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MJZJ_API_KEY for upload and product-submission flows; public product-query flows can run without a token.]

## Skill Version(s):

1.0.1 (source: server release evidence and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
