## Description: <br>
Analyzes OpenAPI or Swagger specifications to produce a structured audit covering API design, security, schemas, CRUD coverage, test strategy, risk scoring, and improvement planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Prathameshppawar](https://clawhub.ai/user/Prathameshppawar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Backend engineers, CTOs, and technical founders use this skill to review OpenAPI or Swagger specifications before production release and to plan security, validation, CRUD, and automated testing improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch and inspect API specification URLs supplied by the user, which can expose private or unpublished API details if used in an unrestricted environment. <br>
Mitigation: Use only authorized specifications, avoid private intranet URLs unless the agent environment is sandboxed and approved, and provide raw JSON or YAML when URL access is unnecessary. <br>
Risk: Audit findings are limited to what is explicitly defined in the OpenAPI or Swagger specification and may not reflect implementation behavior outside the spec. <br>
Mitigation: Review the report against the running service, source code, and production controls before acting on security or readiness recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Prathameshppawar/openapi-deep-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes factual observations, clearly marked inferences, scored readiness dimensions, and prioritized recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
