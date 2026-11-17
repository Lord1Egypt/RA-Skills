## Description:

Provides agent-facing guidance and Python scripts for using LinkFox to call Temu Global non-US/EU order-management APIs, including order lists, details, shipping information, amount queries, combined shipments, customization data, and verification uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to retrieve and manage Temu Global order data through LinkFox-authenticated scripts and API guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox and Temu order credentials and can access customer shipping data.

Mitigation: Pass credentials only when needed, keep access tokens private, and restrict use to order-management tasks that require this data.

Risk: The generic proxy can submit broad Temu API requests beyond a narrow single-operation flow.

Mitigation: Use the documented order scripts for routine tasks and avoid using the generic proxy for unrelated APIs.

Risk: Saved token stores and saved API response files may contain sensitive order or shipping information.

Mitigation: Keep the token store and response directories private, review local file permissions, and delete saved responses when they are no longer needed.

Risk: Billing or QR-payment actions may be triggered during onboarding or quota recovery.

Mitigation: Verify plan, payment method, and amount with the user before proceeding with any billing action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-order-global)
- [Temu Global order API reference](artifact/references/api.md)
- [Partner Global order catalog](artifact/references/partner-global-catalog.md)
- [Temu accessToken authorization](artifact/references/access-token.md)
- [Per-interface API documentation](artifact/references/apis/README.md)
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with inline shell commands; scripts print JSON or summaries and save full JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a local linkfox session data directory; large responses print summaries unless --inline is used.]

## Skill Version(s):

1.0.6 (source: server release metadata; target metadata matches)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
