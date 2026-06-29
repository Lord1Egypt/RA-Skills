## Description: <br>
Generates OpenAPI 3.0/Swagger API documentation from provided code, URLs, OpenAPI files, or interface descriptions, with SDK examples, mock server examples, and test cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn API code, endpoint URLs, OpenAPI files, or natural-language interface descriptions into publishable API documentation and implementation examples. It is suited for REST, GraphQL, and WebSocket documentation workflows that need consistent schemas, authentication notes, examples, mocks, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SDK, curl, mock server, or test examples can appear runnable and may include live API URLs, token placeholders, or state-changing POST, PUT, or DELETE calls. <br>
Mitigation: Review generated commands and code before execution, replace credentials and base URLs with non-production values, and test against sandbox services first. <br>
Risk: Generated examples that include authentication tokens or secrets could be copied into logs, documentation, or shared code. <br>
Mitigation: Use placeholder credentials in generated documentation and remove or redact sensitive values before publishing or committing outputs. <br>


## Reference(s): <br>
- [Detailed API Documentation Generator Reference](artifact/references/details.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/qqyougitcom/mimo-api-doc-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown, OpenAPI YAML, HTML, source code, shell command examples, and mock/test configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary documentation language is Chinese; code examples use English comments where specified by the skill.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata; SKILL.md frontmatter says 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
