## Description:

Create, schedule, and manage platform-specific social media posts, with writing guidance and support for local media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posteyai](https://clawhub.ai/user/posteyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can draft and adapt posts for their connected social accounts, review platform rules and drafts, and manage publishing workflows through Postey. Local media workflows can prepare uploads for those workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-selection flaws could upload media under the wrong identity.

Mitigation: Use a release that fixes local-config trust and project-local OAuth selection; verify the active identity, and avoid repository-supplied credentials and --local OAuth.

Risk: Remote-video downloads have incomplete private-network protections.

Mitigation: Use a release with downloader destination checks and isolate remote-video processing from private networks, especially for untrusted links.

Risk: Publishing or scheduling without explicit approval could post unreviewed content.

Mitigation: Keep the documented approval step and obtain the user's approval for the content and timing before publishing or scheduling.

## Reference(s):

- [Postey product site](https://postey.ai)
- [Postey skill release](https://clawhub.ai/posteyai/skills/postey)
- [MCP authentication guide](references/mcp-authentication.md)
- [MCP workflow guide](references/mcp-workflows.md)
- [Routing guide](routing-guide.md)
- [Platform archetypes](references/platform-archetypes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Platform-specific social post drafts, captions, and workflow guidance in text or Markdown, with shell commands for local media tasks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is adapted to requested platforms and their current rules; publishing and scheduling require user approval.]

## Skill Version(s):

3.2.3 (source: release evidence, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
