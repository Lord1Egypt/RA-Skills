## Description:

Helps agents manage Shopee FirstMile logistics for authorized stores through LinkFox-mediated Shopee Open API operations for unbound orders, first-mile tracking numbers, waybills, channels, transit warehouses, and courier delivery details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee sellers, operators, and developers use this skill to inspect and act on cross-border FirstMile logistics workflows for stores that have already been authorized through the companion LinkFox Shopee store authentication skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Shopee logistics data and LinkFox credentials to LinkFox services.

Mitigation: Install and use it only for stores where that data flow is acceptable, and avoid overriding API host environment variables.

Risk: The skill stores full API responses locally, which may include operational store or shipment details.

Mitigation: Run it in an appropriate workspace and review or remove retained response files according to the user's data handling requirements.

Risk: The onboarding flow can assist with LinkFox login, API key generation, and payment orders.

Mitigation: Require explicit user confirmation before bind, unbind, login, API key, or payment actions, and prefer secure credential storage over shell profile files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-first-mile)
- [Shopee FirstMile API index](https://open.shopee.com/documents/v2/v2.first_mile.get_unbind_order_list?module=96&type=1)
- [FirstMile API field reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses saved to local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may be summarized on stdout when large; full LinkFox and Shopee API responses are retained in local JSON files.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
