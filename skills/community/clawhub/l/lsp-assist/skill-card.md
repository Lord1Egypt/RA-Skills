## Description:

Language Server Protocol integration for OpenClaw agents that enables precise code navigation, including go-to-definition, references, hover information, diagnostics, and symbol search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgjq](https://clawhub.ai/user/zgjq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query local language servers for definitions, references, type hover information, diagnostics, and workspace symbols while navigating Python and TypeScript/JavaScript codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local daemon can expose project analysis results to other local processes when started without an authentication token.

Mitigation: Prefer one-shot mode, or start daemon mode with a strong bearer token on a single-user machine.

Risk: Startup and example command output can disclose bearer tokens if logs are shared.

Mitigation: Avoid logging or sharing daemon startup output and shell history that includes tokens.

Risk: Globally installed or latest-version language servers can change behavior unexpectedly.

Mitigation: Use pinned, project-local language-server installations where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zgjq/skills/lsp-assist)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [JSON responses with Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local language-server installations and project configuration for supported languages.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
