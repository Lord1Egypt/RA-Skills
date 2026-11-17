## Description:

Turn long videos (podcasts, webinars, streams) into vertical 9:16 clips with subtitles, re-cut them, and publish them to TikTok, Instagram Reels and YouTube Shorts via the OpenShorts API or MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutonby](https://clawhub.ai/user/mutonby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and publishing teams use this skill to guide agents through clipping long-form videos, restyling subtitles, re-cutting clips, and posting or scheduling shorts through OpenShorts. It is useful when an agent needs to choose safe API options, handle quota or quality responses, and request confirmation before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional unpinned `uvx openshorts` shortcut may execute remote package code with access to local environment variables.

Mitigation: Prefer the MCP or REST integration paths, or pin and verify the CLI package before allowing an agent to run it.

Risk: OpenShorts and Gemini credentials may be exposed if stored outside trusted secret storage.

Mitigation: Store API keys only in the host agent's approved secret storage and avoid echoing keys into logs, prompts, or shell history.

Risk: Publishing clips to TikTok, Instagram, or YouTube is public and can be hard to reverse.

Mitigation: Require explicit user approval for target platforms, captions, and scheduling before any publish action.

## Reference(s):

- [OpenShorts MCP documentation](https://www.openshorts.app/mcp)
- [OpenShorts hosted MCP endpoint](https://mcp.openshorts.app/mcp)
- [OpenShorts API documentation](https://api.openshorts.app/docs)
- [OpenShorts HTTP reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/mutonby/skills/openshorts)
- [Upload-Post](https://www.upload-post.com/)

## Skill Output:

**Output Type(s):** [guidance, markdown, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline JSON, HTTP, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenShorts REST or MCP call plans, polling guidance, webhook handling notes, and publishing confirmation prompts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
