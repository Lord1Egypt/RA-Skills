## Description: <br>
Audits local GraphQL SDL or introspection JSON to surface N+1 hotspots, depth-limit gaps, deprecated field use, naming issues, circular references, missing pagination, and broad scalar types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API engineers use this skill to review GraphQL schemas for security, performance, and maintainability issues before deployment or during schema reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may list and read local GraphQL schema files and may inspect JavaScript or TypeScript source when checking depth-limit settings. <br>
Mitigation: Run it from the intended project directory, provide a target path when possible, and review the generated recommendations before applying changes. <br>
Risk: Optional schema-fetch or package-install examples can interact with project endpoints or install dependencies. <br>
Mitigation: Use those examples only with trusted endpoints and projects, and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-graphql-schema-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown report with issue tables, code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prioritized findings, resolver-level fix suggestions, and query complexity budget recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release and metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
