## Description:

Helps API developers, backend teams, and maintainers generate, improve, and validate OpenAPI or Swagger documentation for REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn API context into OpenAPI or Swagger documentation, reusable workflows, implementation support, checklists, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad API-documentation wording because implicit invocation is enabled.

Mitigation: Confirm that the active request is about OpenAPI, Swagger, REST API documentation, or related developer-experience work before relying on the skill output.

Risk: Generated OpenAPI specifications, examples, or code changes may be incomplete or inaccurate for the target service.

Mitigation: Review generated artifacts against the live API behavior, schemas, authentication requirements, and project tests before publishing or applying changes.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/openapi-docs-generator-100317)
- [Investigate and evolve a capability-driven XBuilder Admin Console](https://github.com/goplus/builder/issues/3361)
- [Documentation: Get all movie translations](https://github.com/trakt/trakt-api/issues/869)
- [[SERVER] Implement API Documentation with Redoc](https://github.com/Arenax-gaming/ArenaX/issues/663)
- [Swagger Bearer token discussion](https://segmentfault.com/q/1010000017381307/a-1020000017382712)
- [OpenAPI interface specification article](https://segmentfault.com/a/1190000043968971)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be tailored to the user's API context and reviewed before applying generated specifications or code changes.]

## Skill Version(s):

0.20260729.110214 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
