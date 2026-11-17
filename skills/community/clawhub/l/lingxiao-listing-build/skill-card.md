## Description:

Builds TikTok Shop and Etsy listing drafts from product data, validates platform-specific fields, and returns Etsy title, tag, description, and image-slot checks through the Lingxiao MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeli20221102-ux](https://clawhub.ai/user/mikeli20221102-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace sellers, ecommerce operators, and listing specialists use this skill to assemble TikTok Shop or Etsy listing drafts, check field limits before import, and decide which errors must be fixed before platform submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product listing details are sent to the remote Lingxiao MCP service.

Mitigation: Review product data for confidential or sensitive information before using the MCP endpoint.

Risk: Paid copy generation can consume account quota or incur a charge.

Mitigation: Use paid generation only with an intended account and explicit confirmation.

Risk: Marketplace rules and field limits can change after validation.

Mitigation: Treat the validation report as a pre-check and confirm final acceptance in the TikTok Shop or Etsy platform interface.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeli20221102-ux/skills/lingxiao-listing-build)
- [Lingxiao MCP endpoint](https://www.lingxiaochuhai.com/mcp)
- [Lingxiao membership page](https://www.lingxiaochuhai.com/app/membership?from=mcp-trial)
- [Lingxiao link builder](https://www.lingxiaochuhai.com/tools/link-builder)
- [Lingxiao auto listing tool](https://www.lingxiaochuhai.com/tools/auto-listing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON MCP configuration and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft listing fields, validation reports, and warnings through a remote MCP service; paid copy generation requires explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
