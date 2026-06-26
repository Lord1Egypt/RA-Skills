## Description: <br>
Turn any OpenAPI or Swagger API into CLI commands, search endpoints with BM25, check parameters, and execute API calls without an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vakovalskii](https://clawhub.ai/user/vakovalskii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure ocli profiles, search OpenAPI or Swagger endpoints, inspect command parameters, and execute API calls from shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authenticated control over arbitrary APIs configured in ocli profiles. <br>
Mitigation: Use least-privilege tokens, prefer test or read-only profiles for exploration, and scope profiles to the APIs the agent is intended to use. <br>
Risk: Untrusted OpenAPI specs or base URLs can steer the agent toward unsafe or unintended API calls. <br>
Mitigation: Use trusted OpenAPI specs and base URLs, and refresh profiles only from sources the operator has reviewed. <br>
Risk: Commands that create, update, delete, publish, or otherwise change remote data can have real side effects. <br>
Mitigation: Require explicit human approval before state-changing API commands are executed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vakovalskii/ocli-api) <br>
- [Publisher profile](https://clawhub.ai/user/vakovalskii) <br>
- [openapi-to-cli project documentation](https://github.com/EvilFreelancer/openapi-to-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON response handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ocli binary and trusted OpenAPI or Swagger specs; API effects depend on configured profiles and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
