## Description:

Integration architect for multi-app monorepos \u2014 shared contracts, API-first design with OpenAPI, cross-app auth, auto-generated SDKs, and full MCP server scaffolding per app

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and implement interoperability across multi-app monorepos by creating shared contracts, OpenAPI specifications, generated SDKs, cross-app authentication, and MCP server scaffolding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose and generate broad repository changes across packages, applications, MCP servers, and workspace configuration.

Mitigation: Require a dry-run plan with exact paths before execution, review each generated package or spec incrementally, and verify builds before proceeding.

Risk: Generated MCP tools and cross-app SDK code can reference service tokens, API keys, and event data.

Mitigation: Review generated MCP tools before exposing service tokens, keep credential access in environment variables, and avoid exposing service tokens to client-side code.

Risk: Webhook scaffolding may be under-scoped if reusable secrets or broad payloads are used.

Mitigation: Harden webhook delivery with approved HTTPS destinations, minimal payloads, and HMAC-style signatures instead of sending reusable secrets.

Risk: Unpinned npx tooling can change generated output or introduce unexpected behavior.

Mitigation: Pin npx tooling versions before running generated commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold or modify TypeScript monorepo files, OpenAPI specs, SDK code, auth utilities, MCP server files, and workspace configuration.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
