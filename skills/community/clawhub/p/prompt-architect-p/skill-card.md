## Description:

Transforms rough concepts into high-quality LLM prompts by analyzing user inputs, asking clarifying questions, selecting prompt engineering frameworks, and returning a polished prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and external users use this skill to turn rough ideas, documents, links, images, or task descriptions into structured prompts for LLMs. It guides clarification, framework selection, and final prompt packaging for tasks such as analysis, creative work, code generation, and data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts may ask models to show full reasoning or may be reused with sensitive documents without enough review.

Mitigation: Review generated prompts before reuse, especially for sensitive inputs, and prefer concise rationale requests instead of hidden or internal reasoning.

## Reference(s):

- [Prompt Engineering Frameworks](references/frameworks.md)
- [Prompt Quality Criteria](references/quality-criteria.md)
- [Prompt Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown response with clarifying questions, a copy-ready prompt in a code block, and a brief framework note.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final prompts may be produced in English or Arabic after the user selects a language.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
