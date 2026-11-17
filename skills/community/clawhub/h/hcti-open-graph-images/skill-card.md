## Description:

Create and implement HCTI dynamic Open Graph image configurations that render webpages or populate templates from page metadata for persistent social preview URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[htmlcsstoimage](https://clawhub.ai/user/htmlcsstoimage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to configure persistent HCTI Open Graph image URLs, publish the required webpage metadata, and verify screenshot-based or template-based social previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering sends page HTML/CSS, target URLs, template values, and rendering options to the hosted HCTI service.

Mitigation: Confirm the user is comfortable sharing those inputs with HCTI before creating or updating configurations.

Risk: Rendering consumes HCTI image credits and may incur service costs under the user's plan.

Mitigation: Review account costs and image-credit usage before rendering.

Risk: Proxy, storage-destination, update, and delete actions can change the user's HCTI account configuration.

Mitigation: Perform those actions only when the user explicitly intends the account change.

Risk: Website integration can fail when metadata is absent from the initial HTML head or when public image URLs use the management id instead of domain_id.

Mitigation: Publish server-rendered metadata, use domain_id in public image URLs, and open the HCTI image URL directly to verify the result.

## Reference(s):

- [HCTI homepage](https://htmlcsstoimage.com)
- [HCTI MCP documentation](https://docs.htmlcsstoimage.com/integrations/mcp/)
- [OpenClaw MCP setup](https://docs.openclaw.ai/cli/mcp/registry)
- [Webpage integration for dynamic Open Graph images](references/webpage-integration.md)
- [Dynamic Open Graph image setup](https://docs.htmlcsstoimage.com/getting-started/og-images/)
- [Supported page metadata](https://docs.htmlcsstoimage.com/getting-started/og-images/supported-parameters/)
- [Caching and refresh behavior](https://docs.htmlcsstoimage.com/guides/debugging/og-image-caching/)
- [Platform and framework guides](https://docs.htmlcsstoimage.com/guides/og-images/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, HTML metadata snippets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [After successful operations, reports the configuration name, management id, public domain_id, enabled state, rendering mode, refresh interval, and an example image URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
