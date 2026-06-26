## Description: <br>
Search npm packages. Use for finding Node.js/JavaScript packages, libraries, and tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to search and discover Node.js and JavaScript packages on npm from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submitted artifact references a helper command path, but the helper script itself was not included in the artifact evidence. <br>
Mitigation: Before installation or use, confirm whether scripts/npmsearch is supplied by the runtime or package manager and inspect it if available. <br>
Risk: The skill depends on external command-line tools that may be missing from the runtime environment. <br>
Mitigation: Verify that jq and npm-search-mcp-server are installed before invoking the npm search workflow. <br>


## Reference(s): <br>
- [NPM Search on ClawHub](https://clawhub.ai/TheSethRose/npm-search) <br>
- [TheSethRose ClawHub profile](https://clawhub.ai/user/TheSethRose) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces package-search guidance that depends on jq and npm-search-mcp-server being available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
