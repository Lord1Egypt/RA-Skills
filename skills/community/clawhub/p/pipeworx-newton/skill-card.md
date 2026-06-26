## Description: <br>
Symbolic math solver for simplifying, differentiating, integrating, and factoring expressions through the Newton API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and students can use this skill to ask an agent for exact symbolic math operations such as simplification, derivatives, integrals, and polynomial factoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Math expressions are sent to Pipeworx's remote Newton service. <br>
Mitigation: Avoid submitting private formulas, proprietary research, regulated data, or secrets. <br>
Risk: The optional setup uses npx to run mcp-remote at install or runtime. <br>
Mitigation: Review and trust that dependency path separately before enabling the MCP server. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-newton) <br>
- [Pipeworx Newton homepage](https://pipeworx.io/packs/newton) <br>
- [Pipeworx Newton MCP endpoint](https://gateway.pipeworx.io/newton/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON symbolic math results, with Markdown setup guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote Newton MCP/API service and requires curl for direct API examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
