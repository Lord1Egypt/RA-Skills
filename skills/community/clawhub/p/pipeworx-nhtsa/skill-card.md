## Description: <br>
Decode VINs and look up vehicle makes/models via the NHTSA Vehicle Product Information Catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and automotive workflows use this skill to decode VINs, browse registered vehicle makes, and look up models by make and year for insurance, parts, registration, and vehicle verification tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted VINs and make/model queries are sent to Pipeworx's disclosed NHTSA gateway. <br>
Mitigation: Avoid submitting sensitive or unnecessary vehicle identifiers, and review data handling expectations before using the skill in regulated or customer-facing workflows. <br>
Risk: The MCP configuration uses mcp-remote@latest, which may change between installs. <br>
Mitigation: Pin the mcp-remote package version when reproducible installs are required. <br>


## Reference(s): <br>
- [Pipeworx NHTSA pack homepage](https://pipeworx.io/packs/nhtsa) <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-nhtsa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces vehicle lookup guidance, MCP configuration, and examples for JSON-RPC tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
