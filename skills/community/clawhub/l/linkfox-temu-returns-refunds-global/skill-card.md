## Description:

Provides LinkFox gateway scripts and references for Temu Global returns, refunds, and after-sales APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operations teams, and developers use this skill to query and handle Temu Global returns, refunds, after-sales records, return logistics, addresses, labels, signatures, and carriers through LinkFox-managed API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires commerce API credentials and may ask users to grant broad or sensitive Temu permissions.

Mitigation: Use a dedicated least-privilege Temu token where possible and grant only the permissions needed for the specific returns or refunds task.

Risk: The skill can store Temu access tokens and full API responses locally, including return addresses, labels, refund identifiers, and order identifiers.

Mitigation: Avoid shared machines, protect the token store and working directory, and remove retained response files when they are no longer needed.

Risk: Generic proxy and file-download scripts can perform actions beyond a narrow returns lookup.

Mitigation: Review the requested API type, parameters, and download URL before execution, especially for label upload, file download, and refund-related workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-returns-refunds-global)
- [API reference](references/api.md)
- [Temu accessToken authorization and retrieval](references/access-token.md)
- [Partner Global returns and refunds catalog](references/partner-global-catalog.md)
- [Returns and refunds API document index](references/apis/README.md)
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)
- [Temu Global OpenAPI router](https://openapi-b-global.temu.com/openapi/router)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash examples, JSON request payloads, and saved JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save complete API responses under ./linkfox/... and summarize large responses unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
