## Description: <br>
Integration architect for multi-app monorepos -- shared contracts, API-first design with OpenAPI, cross-app auth, auto-generated SDKs, and full MCP server scaffolding per app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement interoperability across multi-application monorepos. It helps design shared TypeScript contracts, OpenAPI specifications, generated SDKs, cross-app authentication, and MCP server scaffolding while adapting to pnpm, yarn, or npm workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may modify monorepo files and scaffold network-capable auth, SDK, MCP, and webhook code. <br>
Mitigation: Review the agent's plan and diffs before accepting changes, and inspect generated code before running or deploying it. <br>
Risk: Generated integrations may reference service tokens or environment variables. <br>
Mitigation: Use least-privilege service tokens, do not place secrets in generated files, and keep credential values outside generated source. <br>
Risk: Generated authentication, MCP, or webhook code can affect inter-application access control. <br>
Mitigation: Validate auth flows, webhook secrets, and MCP tool behavior before enabling the generated integration in a deployed environment. <br>


## Reference(s): <br>
- [Interop Forge ClawHub page](https://clawhub.ai/guifav/interop-forge) <br>
- [Artifact-declared project homepage](https://github.com/guifav/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify repository files when the agent applies the generated integration plan.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
