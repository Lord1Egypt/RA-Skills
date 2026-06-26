## Description: <br>
Parses complex OpenAPI specs and generates Drift test cases from them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinrvaz](https://clawhub.ai/user/kevinrvaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to analyze OpenAPI 3.x endpoint schemas and produce Drift operations and datasets that cover polymorphic schemas, composed schemas, regex-constrained fields, and negative cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted OpenAPI files or remote $ref URLs could lead the agent to produce misleading or unsafe test guidance. <br>
Mitigation: Use trusted OpenAPI files and review any remote $ref URL before allowing the agent to rely on it. <br>
Risk: Generated Drift YAML may exercise real service behavior, including lifecycle hooks, write operations, delete operations, or authentication paths. <br>
Mitigation: Inspect generated Drift YAML before running it against real services, especially operations involving POST, DELETE, lifecycle hooks, or auth behavior. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kevinrvaz/openapi-parser) <br>
- [Schema Patterns Reference](references/schema-patterns.md) <br>
- [Drift Mapping Reference](references/drift-mapping.md) <br>
- [Example Repos Reference](references/example-repos.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis, Drift operations YAML, dataset YAML when needed, and gaps for intentionally excluded schema combinations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
