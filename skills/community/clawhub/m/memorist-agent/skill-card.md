## Description:

Memorist Agent helps families capture parents' and relatives' life stories through adaptive English or Chinese interviews over relay, WhatsApp, WeChat, Telegram, iMessage, or direct conversation, then organizes story fragments into memoir chapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinghaojia](https://clawhub.ai/user/yinghaojia)

### License/Terms of Use:

MIT

## Use Case:

Families and caregivers use Memorist Agent to interview parents, grandparents, and other relatives, preserve memories in English or Chinese, and compile collected story fragments into shareable memoir chapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive family stories and contact data.

Mitigation: Prefer relay mode for sensitive stories and confirm every narrator and recipient understands where messages and exports go.

Risk: Persistent auto-reply agents and messaging bindings can send replies through WhatsApp, iMessage, Telegram, or WeCom.

Mitigation: Review OpenClaw bindings after spawn or despawn and keep channel allowlists narrow before enabling auto-reply.

Risk: Voice features may install local speech tools from unpinned package sources.

Mitigation: Install speech tools only from trusted, pinned sources and review the install commands before running setup-stt.

Risk: Network-capable tools could expose private story context if enabled unnecessarily.

Mitigation: Keep web_search disabled unless it is explicitly needed for a user-approved workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinghaojia/skills/memorist-agent)
- [Project Homepage](https://github.com/jimmyclaw/memorist_agent-skill)
- [Support Issues](https://github.com/jimmyclaw/memorist_agent-skill/issues)
- [Interview Workflow](references/interview-workflow.md)
- [AI Interview Principles](references/interview-principles.md)
- [Compile, Export & Share](references/compile-export-share.md)
- [Media Requirements & Voice Note Handling](references/media-and-voice.md)
- [Spawn & Despawn Dedicated Narrator Agents](references/spawn-despawn.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and generated memoir export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local narrator records, story fragments, compiled chapters, exports, and messaging prompts or replies.]

## Skill Version(s):

0.1.0 (source: frontmatter, package.json, clawhub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
