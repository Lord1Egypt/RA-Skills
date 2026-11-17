## Description:

Guides users from vague intentions through clarifying questions into structured prompts that another AI agent can act on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wesley138cn](https://clawhub.ai/user/wesley138cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially Chinese-speaking AI beginners and creative or non-technical users, use this skill to clarify ideas, decisions, learning needs, and communication goals before asking an AI system for help. It produces a concise, structured prompt that preserves the user's context, constraints, concerns, and desired result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a legal, financial, career, or relationship authority when it asks questions about sensitive decisions.

Mitigation: Present outputs as prompt-drafting assistance and require users to consult qualified professionals for high-stakes decisions.

Risk: The bundled scenario loader can read valid JSON files outside the intended scenarios folder if exposed to arbitrary scenario names.

Mitigation: Restrict scenario names to bundled scenario identifiers or validate path containment before using the script in an API or service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wesley138cn/skills/intent-translator)
- [Skill documentation](artifact/SKILL.md)
- [User test records](artifact/tests/user_test_records.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style structured prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role, background, goals, constraints, concerns, action steps, and risk-prevention sections depending on the selected scenario.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
