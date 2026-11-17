## Description:

Designs REST API endpoints and OpenAPI 3.0 specifications from raw JSON data, including endpoints, schemas, HTTP methods, status codes, and examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn user-provided JSON into REST endpoint designs and OpenAPI 3.0 schemas. It is suited for API contract drafting, not backend implementation or API client generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API contracts may suggest DELETE or update endpoints that do not match the user's real authorization, data model, or business rules.

Mitigation: Review mutating endpoints, validation rules, authorization assumptions, and schema details before using the generated OpenAPI specification.

Risk: Stale artifact files refer to the older user-provides-json name, which can confuse reviewers or downstream checks.

Mitigation: Publisher should update stale references and tests to the json-to-api name before relying on those files for release validation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjipeng977/skills/json-to-api)
- [Metadata Source: MiniMax-AI Skills](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with OpenAPI 3.0 YAML examples and REST endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Design suggestions are derived from user-provided JSON and should be reviewed before implementation.]

## Skill Version(s):

1.0.1 (source: server release evidence and changelog, released 2026-05-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
