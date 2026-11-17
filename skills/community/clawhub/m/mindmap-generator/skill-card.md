## Description:

Generates visual mindmap images from conversations, goals, decisions, and daily priorities, delivered as PNG images viewable directly in Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parasharnagle](https://clawhub.ai/user/parasharnagle)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to turn conversations, goals, decisions, meeting notes, daily priorities, and weekly reviews into readable mindmaps with a short summary. It is most useful when information has hierarchy and at least three branches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive assistant context may be sent to a configured Telegram chat.

Mitigation: Use only with content suitable for that Telegram chat, verify the chat ID and bot token handling, and avoid sensitive meeting, calendar, memory, or business data unless the environment is trusted.

Risk: The renderer may use an unpinned Mermaid CLI through npx and browser rendering with weak isolation.

Mitigation: Prefer a pinned local Mermaid CLI install, disable runtime npx fetching, and run rendering in an isolated low-privilege environment.

Risk: Incorrect Telegram configuration can send the generated mindmap to the wrong chat or expose bot credentials.

Mitigation: Confirm the destination chat ID, keep the bot token in a protected environment variable, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parasharnagle/skills/mindmap-generator)
- [Publisher Profile](https://clawhub.ai/user/parasharnagle)
- [Mermaid Mindmap Syntax](references/mermaid_mindmap_syntax.md)
- [Mindmap Best Practices for AI Personal Assistants](references/mindmap_best_practices.md)
- [Mermaid Mindmap Documentation](https://mermaid.js.org/syntax/mindmap.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, image files, guidance]

**Output Format:** [Mermaid mindmap syntax, brief text summary, PNG image delivered through Telegram, and Unicode text-tree fallback when rendering fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, Mermaid CLI, curl, and a configured Telegram bot token and chat ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
