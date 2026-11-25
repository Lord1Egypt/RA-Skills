## Description:

Runs a multi-model deliberation across models from different labs (Claude, GPT, Gemini, Grok, DeepSeek, Kimi, and more) via mumo's MCP server, returning full responses plus typed cross-model reactions. Use when independent perspectives are needed on architecture/product decisions, design and plan review before implementation, pre-launch pressure tests, tradeoffs with multiple defensible framings, or explicit user requests for a mumo panel. Especially valuable for pre-implementation review of anything touching auth, security, tokens, payments, data exposure, or migrations. Requires a mumo platform API key (mmo_live_*) registered with `openclaw mcp set mumo`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericatmumo](https://clawhub.ai/user/ericatmumo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use the skill to gather independent model perspectives on architecture, design, launch, and other high-impact decisions, then review areas of agreement and disagreement before choosing a course of action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision context provided to the skill may be shared with participating external model providers; safeguards for sensitive decisions are not fully clear.

Mitigation: Do not include secrets or sensitive information unless sharing it is appropriate and authorized. Review the context before submitting it to a panel.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ericatmumo/skills/mumo)
- [mumo product](https://mumo.chat)
- [mumo MCP documentation](https://mumo.chat/docs/mcp)
- [mumo API documentation](https://mumo.chat/docs/api)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Reading reactions](artifact/references/reading-reactions.md)
- [Writing reactions](artifact/references/writing-reactions.md)
- [Synthesis](artifact/references/synthesis.md)
- [Model selection](artifact/references/model-selection.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Text and Markdown containing model responses, typed reactions, and a synthesized summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response length and detail vary with the deliberation and participating models.]

## Skill Version(s):

0.9.1 (source: CHANGELOG, released 2026-11-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
