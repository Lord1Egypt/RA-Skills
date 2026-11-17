## Description:

Infer clean, production-ready schemas from messy sample data and generate Pydantic, Zod, TypeScript, JSON Schema, or Go representations with inferred types, nullability, optional fields, validation hints, and confidence notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn pasted sample data from APIs, CSVs, JSON, plain text, or LLM outputs into reviewed schema definitions and type models across common Python, TypeScript, JSON Schema, and Go formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill for general schema or type-generation requests.

Mitigation: Confirm the user wants schema inference before analyzing unrelated data or code.

Risk: Sample data may contain secrets, regulated data, or sensitive business information.

Mitigation: Use sanitized examples and avoid pasting credentials or regulated records unless analysis of that content is explicitly approved.

Risk: Generated schemas can overfit limited samples or misclassify ambiguous fields.

Mitigation: Review the confidence notes, optionality, nullability, enum choices, and semantic type assumptions before adopting generated schemas.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-schema-sleuth)
- [Canlah AI Homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown report with tables, confidence notes, and generated code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Pydantic v2 models, Zod schemas, TypeScript interfaces, JSON Schema Draft 7 documents, Go structs, and optional parser code.]

## Skill Version(s):

1.0.3 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
