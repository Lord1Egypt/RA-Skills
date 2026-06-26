## Description: <br>
Add OAuth 2.0 PKCE authentication to a remote MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucaperret](https://clawhub.ai/user/lucaperret) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building remote MCP servers use this skill to add OAuth discovery, dynamic client registration, PKCE authorization, token exchange, refresh flow, and token-protected tool access for user-specific data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample OAuth flow is under-scoped for production use and could lead to weak OAuth protections if copied without hardening. <br>
Mitigation: Require exact redirect URI registration and validation, validate client_id, bind authorization codes to client_id, redirect_uri, and code_challenge, and verify code_verifier during token exchange. <br>
Risk: Token and Redis handling may expose sensitive OAuth tokens if the examples are deployed without stronger operational controls. <br>
Mitigation: Use encrypted token storage where available, least-privilege scopes, no secret logging, revocation support, and short practical TTLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lucaperret/mcp-oauth) <br>
- [Publisher profile](https://clawhub.ai/user/lucaperret) <br>
- [Skill homepage](https://github.com/lucaperret/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; generated code samples require security review before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
