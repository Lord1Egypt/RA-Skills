## Description:

Apply Oliver's stable persona, values, decision models, communication style, and evidence standards when reasoning about risk, responsibility, authority, open source, technology, learning, collaboration, or public communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamliuxiaozhen](https://clawhub.ai/user/iamliuxiaozhen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this persona skill to apply Oliver's evidence-oriented decision models and communication style to software engineering, open-source, risk, responsibility, and public-communication scenarios. It should be used for judgment patterns grounded in the bundled references, not for unsupported opinion invention or superficial style imitation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer an agent toward a third-party persona's evidence-heavy decision style and Chinese-first communication preference even when that framing is not desired.

Mitigation: Review the persona references before deployment and use the skill only when that judgment style and communication preference are appropriate.

Risk: The persona references define known and unknown boundaries; using the skill outside those boundaries can produce unsupported opinions.

Mitigation: Keep outputs grounded in the bundled references, preserve Unknown where evidence is missing, and ask for clarification when a scenario falls outside the documented persona scope.

## Reference(s):

- [Olive Skill README](README.md)
- [Identity](references/identity.md)
- [Values](references/values.md)
- [Decision Models](references/decision-models.md)
- [Voice](references/voice.md)
- [Knowledge Sources](references/knowledge-sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Natural-language responses, Markdown, and task-specific code or command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish confirmed facts, strong inferences, and unknowns when uncertainty matters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
