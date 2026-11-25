## Description:

Runs a multi-model deliberation across models from different labs (Claude, GPT, Gemini, Grok, DeepSeek, Kimi, and more) via mumo's MCP server, returning full responses plus typed cross-model reactions. Use when independent perspectives are needed on architecture/product decisions, design and plan review before implementation, pre-launch pressure tests, tradeoffs with multiple defensible framings, or explicit user requests for a mumo panel. Especially valuable for pre-implementation review of anything touching auth, security, tokens, payments, data exposure, or migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericatmumo](https://clawhub.ai/user/ericatmumo)

### License/Terms of Use:

MIT

## Use Case:

Hermes Agent users use this skill to gather independent model perspectives on architecture and product decisions, design and plan reviews, pre-launch pressure tests, and other high-regret choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and other supplied content may be sent to external model providers.

Mitigation: Avoid submitting secrets or confidential information unless you understand and accept that disclosure.

## Reference(s):

- [mumo MCP documentation](https://mumo.chat/docs/mcp)
- [mumo REST API documentation](https://mumo.chat/docs/api)
- [mumo for Hermes install guide](https://mumo.chat/install/hermes)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Text with full model responses and typed cross-model reactions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a takeaway when requested.]

## Skill Version(s):

0.10.1 (source: SKILL.md frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
