## Description: <br>
Helps API developers and platform teams generate, improve, and validate OpenAPI or Swagger documentation for REST APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, backend teams, developer-experience teams, and maintainers use this skill to plan, generate, improve, and validate OpenAPI or Swagger documentation for REST APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for general API or documentation requests because its trigger wording is broad. <br>
Mitigation: Use a more specific skill for unrelated backend work, or explicitly ask the agent not to use this skill when OpenAPI or Swagger documentation is not the task. <br>
Risk: Generated API documentation guidance may be incomplete or misleading if the available API routes, schemas, authentication rules, or examples are incomplete. <br>
Mitigation: Review the generated OpenAPI or Swagger material against the actual service implementation and run any available schema validation, linting, or documentation preview checks before publishing. <br>


## Reference(s): <br>
- [Requirement Plan](artifact/references/requirement-plan.md) <br>
- [ClawHub skill page](https://clawhub.ai/kyro-ma/openapi-docs-generator-130446) <br>
- [Add Swagger/OpenAPI documentation](https://github.com/laugh-tales/starpass-backend/issues/37) <br>
- [Add Swagger/OpenAPI documentation to the NestJS API](https://github.com/Afro-Pay/AfroPay-Stellar/issues/27) <br>
- [Publish an OpenAPI specification and serve interactive docs](https://github.com/StellarGateLabs/StellarGate/issues/20) <br>
- [OpenAPI interface specification article](https://segmentfault.com/a/1190000043968971) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions, limits, and follow-up risks when needed] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
