## Description:

Chinese BaZi (Four Pillars of Destiny) analysis and AI partner matching for birth-chart based companion selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoezoecookie](https://clawhub.ai/user/zoezoecookie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this MCP server to analyze a birth date with Chinese BaZi methods and match the result to an AI companion persona. With explicit user confirmation, it can write the selected partner prompt into OpenClaw's persistent persona file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent persona changes can alter future OpenClaw behavior if caller-supplied prompt text is written to SOUL.md.

Mitigation: Show the exact partner type, prompt content, and destination before applying the prompt; proceed only after explicit user confirmation and keep the marked bazi-partner section removable.

Risk: Mutable source installation can change behavior between installs.

Mitigation: Prefer a pinned package or reviewed release rather than an unpinned git install command.

Risk: BaZi matching depends on accurate birth hour and correct L2 subtype reasoning, so missing or incorrect inputs can produce misleading matches.

Mitigation: Ask for the birth hour, warn when a fallback hour is used, and present the match as interpretive guidance rather than factual prediction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoezoecookie/skills/mcp-bazi-partner)
- [Project homepage](https://github.com/ZoezoeCookie/mcp-bazi-partner)
- [Project issues](https://github.com/ZoezoeCookie/mcp-bazi-partner/issues)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [JSON tool responses with concise Markdown-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw SOUL.md after explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
