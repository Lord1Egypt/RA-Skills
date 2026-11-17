## Description:

Temu US fulfillment skill for Buy-Shipping labels, cooperative warehouse fulfillment, self-fulfilled shipments, logistics tracking, scan forms, shipment creation, and related order-shipping workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu sellers, fulfillment operators, and developers use this skill to run US order-shipping workflows, including buying labels, retrieving shipping documents, creating scan forms, confirming shipments, managing cooperative warehouse fulfillment, and checking tracking data.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill sends Temu merchant tokens and fulfillment data through LinkFox-hosted gateway endpoints.

Mitigation: Use it only when the user trusts LinkFox with that data, and keep gateway or login endpoint override environment variables unset unless they point to known LinkFox HTTPS hosts.

Risk: The skill can perform state-changing fulfillment actions such as buying labels, updating shipments, confirming shipped packages, canceling pickup reservations, or submitting cooperative warehouse fulfillment.

Mitigation: Confirm every state-changing shipping action with the user before running the corresponding script or API call.

Risk: Temu access tokens and API responses may be stored locally and can contain sensitive merchant or fulfillment data.

Mitigation: Protect the local token store and saved response files, and delete or rotate them when they are no longer needed.

Risk: The generic proxy can be pointed at Temu API types beyond the intended fulfillment workflow.

Mitigation: Limit use to the documented Temu US fulfillment, shipping, scan form, cooperative warehouse, and tracking API types for this skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-fulfillment-us)
- [API Reference](references/api.md)
- [Access Token Guide](references/access-token.md)
- [Onboarding Guide](references/onboarding.md)
- [Partner US Catalog](references/partner-us-catalog.md)
- [Fulfillment API Index](references/apis/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus JSON API responses and saved response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full responses under a linkfox session data directory; small responses are printed in full, while larger responses print summaries unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
