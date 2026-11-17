## Description:

Helps API developers and backend teams generate, improve, and validate OpenAPI or Swagger documentation for REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, backend teams, developer-experience teams, and maintainers use this skill to turn OpenAPI or Swagger documentation needs into practical plans, checklists, code changes, configuration, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation may activate the skill on general API or developer-experience requests.

Mitigation: Use explicit OpenAPI or Swagger prompts when possible, and confirm that the request is about REST API documentation before relying on the output.

Risk: Generated API documentation can be incomplete or misleading if it is not checked against the implementation.

Mitigation: Review generated documentation before applying it to a production service and validate it with the project's OpenAPI, schema, or integration checks.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Add Swagger/OpenAPI documentation](https://github.com/laugh-tales/starpass-backend/issues/37)
- [Add Swagger / OpenAPI documentation to the NestJS API](https://github.com/Afro-Pay/AfroPay-Stellar/issues/27)
- [Publish an OpenAPI specification and serve interactive docs](https://github.com/StellarGateLabs/StellarGate/issues/20)
- [OpenAPI interface specification article](https://segmentfault.com/a/1190000043968971)
- [Swagger Bearer token answer](https://segmentfault.com/q/1010000017381307/a-1020000017382712)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up work tailored to the user's API stack.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
