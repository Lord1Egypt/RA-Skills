## Description:

Helps agents connect to Grabbit's hosted screenshot service to capture webpages and return hosted image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[braingrid](https://clawhub.ai/user/braingrid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users connect Grabbit to capture webpage screenshots, check deployed interfaces, and share hosted image links without running a local browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Page URLs and screenshot contents are sent to a hosted service.

Mitigation: Only capture pages whose URLs and contents may be shared with Grabbit.

Risk: API keys can be exposed if mishandled.

Mitigation: Prefer OAuth where supported or store API keys securely.

Risk: The optional npx installer can fetch changing dependencies.

Mitigation: Avoid it or pin the installer for stricter supply-chain control.

## Reference(s):

- [Grabbit screenshot API documentation](https://grabbit.live/screenshot-api)
- [Grabbit homepage](https://grabbit.live)
- [Grabbit MCP server](https://mcp.grabbit.live)
- [ClawHub skill release](https://clawhub.ai/braingrid/skills/grabbit-screenshots)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with hosted screenshot URLs and optional configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshot capture requires access to Grabbit's hosted service and authentication.]

## Skill Version(s):

1.0.1 (source: ClawHub release; skill metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
