## Description:

Provides agent-facing guidance and Python command wrappers for managing Temu Global product listings through the LinkFox gateway, covering product queries, updates, stock, sale status, compliance fields, deletion, and signed file download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and commerce operators use this skill to manage Temu Global product records, inventory, listing status, compliance fields, and related product metadata through LinkFox-mediated Temu API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live Temu store data, including stock, sale status, compliance fields, and product deletion.

Mitigation: Require explicit confirmation for destructive or commerce-impacting actions and review request payloads before running the scripts.

Risk: The skill handles LinkFox and Temu credentials and may store Temu access tokens locally.

Mitigation: Treat environment variables, request JSON, saved response files, and ~/.linkfox/temu-access-tokens.json as sensitive; restrict file permissions and avoid sharing logs or outputs containing secrets.

Risk: Gateway or login URL overrides can redirect credentialed requests away from the expected LinkFox service.

Mitigation: Use URL override environment variables only in controlled environments and verify the destination before sending credentials or store data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-manage-product-global)
- [Gateway and authentication API reference](artifact/references/api.md)
- [Partner Global Manage Product catalog](artifact/references/partner-global-catalog.md)
- [Temu access token authorization](artifact/references/access-token.md)
- [Per-interface API documentation index](artifact/references/apis/README.md)
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b)
- [Temu OpenAPI Global router](https://openapi-b-global.temu.com/openapi/router)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON request/response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full responses as JSON files under a linkfox session directory and print either full JSON or a summary depending on response size.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
