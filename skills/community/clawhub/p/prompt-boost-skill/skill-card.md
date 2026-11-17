## Description:

嘴替 Skill is a universal query preprocessor that turns vague or conversational user requests into clarified, structured query plans and rewritten prompts for downstream agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longsasasasasa](https://clawhub.ai/user/longsasasasasa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to clarify underspecified requests, identify the task domain, fill blocking input slots, and hand off a professionalized prompt and JSON payload to a downstream model or agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to process every user query and persist activation rules into AGENTS.md or SOUL.md.

Mitigation: Limit activation to explicit prompt-refinement requests, make configuration edits optional, and require reviewable diffs plus rollback steps before installation.

Risk: The skill can record user query patterns and preferences as a learning profile.

Mitigation: Require clear user consent, retention controls, and an opt-out path before storing profile history.

Risk: The artifact is primarily Chinese-language and may alter non-Chinese user intent if language preference is not preserved.

Mitigation: Confirm the user's preferred language and preserve it in clarification questions, query plans, and rewritten prompts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/longsasasasasa/skills/prompt-boost-skill)
- [Activation Guide](references/activation-guide.md)
- [Output Contract](references/output-contract.md)
- [Risk Guardrails](references/risk-guardrails.md)
- [Learning Profile](references/learning-profile.md)
- [Data Analysis Domain](references/domains/data-analysis.md)
- [Technical Support Domain](references/domains/tech-support.md)
- [Marketing Domain](references/domains/marketing.md)
- [Product Manager Domain](references/domains/product-manager.md)
- [Supply Chain Domain](references/domains/supply-chain.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance, configuration]

**Output Format:** [Markdown sections with a structured Query Plan and JSON handoff payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may ask up to three clarifying questions per round, then emits either a clarification response or an approved rewritten prompt for downstream use.]

## Skill Version(s):

2.1.1 (source: server evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
