## Description: <br>
Designs REST or GraphQL APIs, creates OpenAPI specifications, and plans API architecture for resource modeling, versioning, pagination, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API architects use this skill to design developer-friendly REST and GraphQL APIs, including resource models, endpoint contracts, OpenAPI 3.1 specifications, authentication flows, error catalogs, pagination patterns, and versioning plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication error examples could expose token diagnostics or permission details if copied directly into public API responses. <br>
Mitigation: Use generic public 401 and 403 responses, and keep token diagnostics or permission details in logs or privileged tooling. <br>
Risk: Generated API specifications and design guidance may be incomplete or incorrect for a specific product, data model, or compliance context. <br>
Mitigation: Review generated API contracts with engineering, security, and product owners before implementation or publication. <br>


## Reference(s): <br>
- [REST Design Patterns](references/rest-patterns.md) <br>
- [API Versioning Strategies](references/versioning.md) <br>
- [Pagination Patterns](references/pagination.md) <br>
- [API Error Handling](references/error-handling.md) <br>
- [OpenAPI 3.1 Specification](references/openapi.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with OpenAPI YAML or JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include resource definitions, endpoint specifications, authentication and authorization flows, error response catalogs, pagination and filtering patterns, and versioning guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
