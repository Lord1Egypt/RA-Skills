## Description:

mumo helps an agent run multi-model deliberation through mumo's MCP server for architecture, design, security-sensitive review, and other decisions where independent perspectives are valuable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericatmumo](https://clawhub.ai/user/ericatmumo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to ask an OpenClaw agent to convene a multi-model panel for design review, contested technical decisions, red-team analysis, uncertainty expansion, and synthesis of model perspectives before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review prompts and included specifications may be sent to mumo and external model providers.

Mitigation: Minimize excerpts, redact secrets, and ask before transmitting auth flows, tokens, payment logic, customer data, or unreleased security findings.

Risk: Public session-sharing can expose sensitive deliberation content.

Mitigation: Review session contents before sharing and avoid public links for sessions containing confidential or security-sensitive material.

Risk: Panel consensus and individual model responses are advisory and can still be wrong.

Mitigation: Verify recommendations with tests, source checks, and user review before changing code, configuration, or operational plans.

## Reference(s):

- [mumo product](https://mumo.chat)
- [mumo MCP documentation](https://mumo.chat/docs/mcp)
- [mumo REST API documentation](https://mumo.chat/docs/api)
- [mumo OpenClaw install guide](https://mumo.chat/install/openclaw)
- [ClawHub mumo listing](https://clawhub.ai/ericatmumo/skills/mumo)
- [Claim Maps](references/claim-maps.md)
- [Model Selection](references/model-selection.md)
- [Operating Notes](references/operating-notes.md)
- [Snippets](references/snippets.md)
- [Synthesis](references/synthesis.md)
- [Takeaway](references/takeaway.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and MCP tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full model responses, typed cross-model reactions, claim-map links, snippets, and optional round takeaways returned by the mumo service.]

## Skill Version(s):

0.6.2 (source: server release metadata and changelog, released 2026-09-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
