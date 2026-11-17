## Description:

Helps backend and platform teams generate, improve, and validate OpenAPI or Swagger documentation for REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, backend teams, platform teams, and developer-experience maintainers use this skill to turn REST API details into practical OpenAPI or Swagger documentation workflows, checklists, examples, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers and implicit invocation may cause the skill to respond to adjacent API documentation requests where the user did not intend to use it.

Mitigation: Prefer explicit invocation with $openapi-docs-generator for OpenAPI or Swagger tasks when precision matters.

Risk: Generated API documentation guidance may omit project-specific endpoint behavior, authentication rules, or validation requirements.

Mitigation: Review generated documentation against the service implementation and run the included verification steps before publishing.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/openapi-docs-generator-234446)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with checklists, code snippets, configuration examples, and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, limits, validation notes, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
