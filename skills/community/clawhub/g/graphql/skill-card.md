## Description: <br>
Design GraphQL schemas and resolvers with proper performance, security, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a concise GraphQL reference for schema design, resolver behavior, pagination, client cache behavior, performance pitfalls, and production security controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GraphQL guidance can be misapplied to a production API with different schema, authorization, performance, or client-cache constraints. <br>
Mitigation: Review each recommendation against the target API design, data model, threat model, and operational limits before implementation. <br>
Risk: Unbounded GraphQL queries, missing complexity controls, or overly detailed errors can create denial-of-service and information-disclosure exposure. <br>
Mitigation: Use query depth and complexity limits, timeouts, rate limits based on cost, protected or disabled production introspection, and sanitized error responses. <br>


## Reference(s): <br>
- [ClawHub GraphQL Skill](https://clawhub.ai/ivangdavila/graphql) <br>
- [Schema Design Traps](artifact/schema.md) <br>
- [Security Traps](artifact/security.md) <br>
- [Performance Traps](artifact/performance.md) <br>
- [Client-Side Traps](artifact/client.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with inline GraphQL and implementation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference aid; produces recommendations for human review rather than executing code or changing files.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
