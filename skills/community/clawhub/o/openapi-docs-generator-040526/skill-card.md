## Description:

Generate, repair, and validate OpenAPI or Swagger documentation for REST APIs from routes, handlers, schemas, examples, and observed behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or repair OpenAPI and Swagger documentation from REST API implementation details. It helps backend, platform, SDK, and developer-experience teams identify documentation gaps, produce spec fragments, add realistic examples, and run validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger metadata could invoke the skill outside API documentation work.

Mitigation: Use it only for OpenAPI, Swagger, REST API documentation, schema, SDK, or contract-testing tasks.

Risk: API examples could accidentally include secrets, customer data, or live credentials.

Mitigation: Redact sensitive values and use realistic placeholder data before including examples in generated or patched specs.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with OpenAPI YAML or JSON snippets and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include new or patched OpenAPI fragments, endpoint gap analysis, realistic examples, and follow-up tasks for SDK generation, publishing, or CI enforcement.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
