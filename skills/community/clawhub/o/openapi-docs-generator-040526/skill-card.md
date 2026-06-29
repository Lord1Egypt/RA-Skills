## Description: <br>
Generate, repair, and validate OpenAPI or Swagger documentation for REST APIs from routes, handlers, schemas, examples, and observed behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, backend engineers, platform teams, SDK maintainers, and developer-experience teams use this skill to create or repair OpenAPI and Swagger documentation so it matches REST API implementations. It helps inventory routes and schemas, draft reusable spec components, add safe examples, validate the result with standard tooling, and call out implementation/spec drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad OpenAPI, Swagger, REST API, API docs, schema, SDK, and contract-testing trigger terms may activate the skill during general API-documentation conversations. <br>
Mitigation: Use the skill for OpenAPI or Swagger documentation tasks and confirm scope before applying generated recommendations. <br>
Risk: Generated API specs or examples may accidentally include secrets, customer data, or private endpoint details. <br>
Mitigation: Review and redact generated specs, examples, and endpoint details before publishing or committing them. <br>
Risk: Incomplete route, schema, or example inputs can produce an OpenAPI document that still differs from the implementation. <br>
Mitigation: Validate the spec with an OpenAPI parser or linter and explicitly track contract mismatches that require code or documentation changes. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [Bring OpenAPI Documentation In Sync With Live Express Routes](https://github.com/StellarYield-Labs/StellarYield/issues/5) <br>
- [OpenAPI interface specification overview](https://segmentfault.com/a/1190000043968971) <br>
- [OpenAPI specification: RESTful API design](https://blog.csdn.net/2501_94476825/article/details/159013081?ops_request_misc=elastic_search_misc&request_id=c1819a0438ce4a15b39cf91b146e97e0&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-4-159013081-null-null.142^v102^pc_search_result_base8&utm_term=OpenAPI%20%E6%96%87%E6%A1%A3) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with OpenAPI YAML or JSON fragments and validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint gap analysis, realistic examples, contract-mismatch notes, and follow-up tasks for SDK generation, docs publishing, or CI enforcement.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
