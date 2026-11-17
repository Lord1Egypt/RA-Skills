## Description:

Give your agent a searchable knowledge brain - semantic search, topic synthesis, and action tracking across your saved YouTube videos, articles, Reddit threads, X posts, and PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drewautomates](https://clawhub.ai/user/drewautomates)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent search, summarize, synthesize, and track action items across content saved in a Noverload knowledge library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the latest Noverload MCP npm package, so behavior can change when the package updates.

Mitigation: Pin a reviewed package version and update deliberately after review.

Risk: The skill uses a saved Noverload access token.

Mitigation: Store the token with restrictive local permissions and revoke or rotate it when no longer needed.

Risk: The skill can save URLs, add tags, mark swipe files, and complete action items if read-only mode is disabled.

Mitigation: Keep the default read-only mode unless write access is explicitly required.

## Reference(s):

- [Noverload OpenClaw Integration](https://noverload.com/openclaw)
- [Noverload MCP Documentation](https://noverload.com/docs/mcp)
- [Noverload Skill on ClawHub](https://clawhub.ai/drewautomates/skills/noverload)
- [Publisher Profile](https://clawhub.ai/user/drewautomates)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands]

**Output Format:** [Markdown or plain text responses, with JSON configuration snippets and shell commands where setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can retrieve and summarize saved content, synthesize topics, extract frameworks, track actions, browse the library, and optionally save or update content when read-only mode is disabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact Version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
