## Description:

Personality Distiller turns a name, vague requirement, web link, existing skill, or local corpus into a complete agent persona file pack through research, framework extraction, and templated persona writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Agent builders and workspace users use this skill to distill people, thinking frameworks, web content, existing skills, or local writing into a structured persona for an agent. It produces the six persona files needed to shape identity, behavior, relationship model, tools, and proactive rhythms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite persistent workspace persona and behavior files.

Mitigation: Back up existing persona files before use and review the complete generated diff before accepting the replacement.

Risk: Private local sources or tokenized URLs used for distillation can expose sensitive context.

Mitigation: Restrict local analysis to explicitly chosen non-sensitive paths and avoid private or tokenized URLs unless the workspace is approved for that data.

Risk: Generated AGENTS.md safety rules and HEARTBEAT.md proactive behavior can affect future agent conduct.

Mitigation: Manually inspect generated safety boundaries and proactive routines before deployment.

## Reference(s):

- [Personality Distiller ClawHub page](https://clawhub.ai/openlark/skills/personality-distiller)
- [Thinking Frameworks Catalog](references/frameworks.md)
- [Persona Dimensions & Mapping Guide](references/persona-dimensions.md)
- [Deep Research Guide for Persona Distillation](references/research-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown persona files plus a concise summary card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes SOUL.md, IDENTITY.md, USER.md, AGENTS.md, TOOLS.md, and HEARTBEAT.md in the workspace root.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
