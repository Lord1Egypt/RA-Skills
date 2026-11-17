## Description:

Post to LinkedIn, comment, like, search organizations, and manage profiles via Pipedream OAuth integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect a LinkedIn account through Pipedream OAuth, publish personal or organization posts, engage with posts, search organizations, and inspect LinkedIn profile or organization access details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real LinkedIn actions, including publishing, liking, commenting, and deleting content.

Mitigation: Require explicit user confirmation or dry-run review before any posting, engagement, or deletion action is executed.

Risk: Hard-coded user, organization, member, and auth-provision identifiers may route actions through the wrong account.

Mitigation: Replace bundled identifiers with protected user-specific configuration before use and avoid committing account-specific values.

Risk: Organization posting uses a direct helper workaround for LinkedIn organization posts.

Mitigation: Verify organization admin access and OAuth status before using the helper, and keep credentials in the pdauth configuration rather than source files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/g9pedro/skills/linkedin-pipedream)
- [Pipedream MCP](https://mcp.pipedream.com)
- [LinkedIn API Docs](https://learn.microsoft.com/en-us/linkedin/marketing/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pdauth commands and an optional Node.js helper for organization posting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
