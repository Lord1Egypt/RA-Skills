## Description:

Publish or schedule social posts, inspect delivery, and manage automatic crossposting through a connected PostOnce MCP server. Use when the user wants to send content to their PostOnce accounts or configure a PostOnce workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niyonx](https://clawhub.ai/user/niyonx)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People using PostOnce through an agent can connect their authorized social accounts to draft, publish, or schedule posts, inspect delivery results, and configure recurring crossposting when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can make content public on the selected social accounts.

Mitigation: Confirm the intended accounts and content; use a draft when the user wants review before publication.

Risk: Media uploaded for publishing is publicly accessible.

Mitigation: Upload only media intended to be publicly accessible.

Risk: An active crossposting workflow can distribute future content automatically.

Mitigation: Enable recurring crossposting only when requested, and revoke the connected app when access is no longer needed.

## Reference(s):

- [PostOnce OpenClaw integration and setup](https://postonce.to/integrations/openclaw)
- [PostOnce API documentation](https://docs.postonce.to)
- [PostOnce plans](https://postonce.to/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, Post status reports]

**Output Format:** [Natural-language responses, social post text, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report returned post or draft IDs, delivery status, and destination outcomes.]

## Skill Version(s):

0.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
