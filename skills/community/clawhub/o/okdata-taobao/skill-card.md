## Description:

Retrieves public Taobao and Tmall product, review, and shop data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Taobao and Tmall products, inspect product details and buyer reviews, and list a shop's products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid endpoint calls and additional pages can incur per-call charges.

Mitigation: State the endpoint and maximum cost before the first paid call, and request additional pages only when needed.

Risk: The skill sends Taobao lookup requests to the external okdata service; the security scan had partial coverage and medium confidence.

Mitigation: Use the service only if you trust okdata, and keep the API key in OKDATA_API_KEY or client configuration without printing or logging it.

## Reference(s):

- [Taobao and Tmall API documentation](https://okdata.online/apis/taobao/?src=skill-okdata-taobao)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Text containing Taobao and Tmall product, review, and shop data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; additional pages require separate paid calls.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
