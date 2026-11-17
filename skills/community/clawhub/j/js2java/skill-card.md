## Description:

js2java translates JavaScript business logic or natural-language backend requests into complete Spring Boot Java code with explanatory comments, syntax comparison tables, and learning questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancer07](https://clawhub.ai/user/lancer07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and front-end engineers use this skill to convert JavaScript business logic or backend feature requests into Spring Boot-style Java implementations. It is intended for learning and rapid scaffolding of DTOs, entities, repositories, services, controllers, exceptions, validation, and Java syntax explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication example promotes unsafe plaintext password storage and raw-password lookup patterns.

Mitigation: Review generated login, registration, and account code before use, and replace raw password storage or findByEmailAndPassword flows with PasswordEncoder-based hash-and-verify authentication.

Risk: Generated Spring Boot scaffolding is intended as learning/reference material and may not be production-ready.

Mitigation: Review generated code for architecture, security, validation, and operational requirements before using it in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lancer07/skills/js2java)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown with Java code blocks, comparison tables, and learning questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are verbose and use Chinese instructional text by default.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
