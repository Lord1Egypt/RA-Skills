## Description:

Provides agent guidance and scripts for Temu EU order-management API calls through the LinkFox gateway, including order list, detail, shipping information, amount queries, combined shipment, customization, and verification upload workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu EU merchants, marketplace operators, and developers use this skill to retrieve order data, shipping data, payment amounts, customization details, and verification-upload guidance for order workflows. It is intended for agents assisting with LinkFox-authenticated Temu EU order operations.

### Deployment Geography for Use:

Europe

## Known Risks and Mitigations:

Risk: The skill handles Temu merchant credentials and customer shipping data.

Mitigation: Use a dedicated workspace, pass credentials only when needed, avoid inline full output for shipping or decrypted-address calls, and restrict file access to users who should see order data.

Risk: Temu access tokens may be stored locally in plaintext.

Mitigation: Prefer short-lived or dedicated store credentials, protect the token store path, remove stale tokens, and avoid sharing workspaces that contain saved token files.

Risk: Endpoint override environment variables can redirect gateway traffic.

Mitigation: Keep LINKFOX_TOOL_GATEWAY, TEMU_API_BASE_URL, and STORE_API_BASE_URL unset or set only to trusted LinkFox endpoints before running scripts.

Risk: Order responses can include sensitive personal information and may be saved to local JSON files.

Mitigation: Review saved response files before sharing logs or artifacts, and delete local order-response data when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-order-eu)
- [API reference](references/api.md)
- [Temu accessToken authorization and retrieval](references/access-token.md)
- [Partner EU order interface catalog](references/partner-eu-catalog.md)
- [Order API document index](references/apis/README.md)
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts write full gateway responses to local JSON files and may print either the full response or a summary depending on response size and inline mode.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
