## Description:

Temu 全球站（非 US/EU）取消订单 API（买家+卖家合一），经 LinkFox 网关转发 6 个接口：买家售后取消(bg.aftersales.cancel.*)、卖家申诉/缺货取消(temu.order.cancel.*)等，默认 site=global、tokenPurpose=order-shipping。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu sellers, operations teams, and developers use this skill to call LinkFox-assisted Temu Global cancellation workflows for buyer aftersales cancellations and seller appeal or out-of-stock cancellation requests.

### Deployment Geography for Use:

Global, excluding US and EU Temu cancellation workflows

## Known Risks and Mitigations:

Risk: The skill uses real LinkFox and Temu seller credentials and can store Temu access tokens locally.

Mitigation: Use trusted LinkFox endpoints, prefer short-lived and least-privileged Temu tokens, and avoid exposing unmasked token output.

Risk: Gateway override environment variables can redirect requests away from the expected LinkFox endpoint.

Mitigation: Avoid setting gateway override variables unless the endpoint is explicitly trusted and reviewed.

Risk: Billing-related onboarding commands can create payment orders.

Mitigation: Confirm plan and payment method with the user before running billing commands.

Risk: Full API responses are saved locally and may contain order or seller account data.

Mitigation: Review local output locations and handle saved response files as sensitive operational data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-cancel-order-global)
- [API reference](references/api.md)
- [Partner Global catalog](references/partner-global-catalog.md)
- [Access token guide](references/access-token.md)
- [Authorization flow](references/authorization-flow.md)
- [Onboarding guide](references/onboarding.md)
- [Cancel Order API index](references/apis/README.md)
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9)
- [Temu Global OpenAPI router](https://openapi-b-global.temu.com/openapi/router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may print small JSON responses inline; larger responses are summarized after the full response is saved locally.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
