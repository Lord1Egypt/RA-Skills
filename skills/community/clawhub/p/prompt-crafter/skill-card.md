## Description:

Build effective prompts for ChatGPT, Claude, Gemini, or other LLMs using RACE, Chain-of-Thought, Constraint-Stacking, and Few-Shot patterns, with examples, troubleshooting, and production safety guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crispyangles](https://clawhub.ai/user/crispyangles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and teams use this skill to choose and apply prompt frameworks for writing, analysis, coding, creative work, and production prompt hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example prompts may shape model style, reasoning behavior, or output constraints in ways users did not intend.

Mitigation: Review selected examples before reuse and adapt role, constraints, refusal paths, output caps, and required formats to the deployment context.

Risk: Prompt guidance can still produce incorrect, misleading, or overconfident model outputs if users omit uncertainty handling.

Mitigation: Use the skill's production safety guidance to include refusal paths, exact output formats, adversarial tests, and prompt versioning.

## Reference(s):

- [Prompt Frameworks - Extended Examples](references/frameworks.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, Code, Configuration]

**Output Format:** [Markdown guidance with prompt examples, decision logic, troubleshooting tables, and copyable text or code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tool execution, external service calls, credentials, or generated files are required by the skill itself.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
