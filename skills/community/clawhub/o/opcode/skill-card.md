## Description:

Opcode is a zero-token execution layer for AI agents that defines persistent, scheduled, deterministic DAG workflows over MCP SSE tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rendis](https://clawhub.ai/user/rendis)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Opcode to define reusable workflow templates, run persistent workflows, inspect status and history, send signals, and visualize workflow DAGs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful shell, filesystem, network, secret, and persistent scheduling capabilities can be exposed with weak default scoping.

Mitigation: Review before installing; run Opcode as a low-privilege user; bind it to localhost or a protected endpoint; set strict filesystem and network allowlists; and disable or tightly restrict shell.exec for untrusted workflows.

Risk: Stored secrets depend on OPCODE_VAULT_KEY protection.

Mitigation: Protect and rotate OPCODE_VAULT_KEY, use a secrets manager or environment variable, and avoid storing the vault key in plaintext configuration.

Risk: Unattended self-updates or unpinned installs can change runtime behavior without review.

Mitigation: Pin production installs, review updates before rollout, and avoid unattended self-update workflows.

## Reference(s):

- [Opcode repository](https://github.com/rendis/opcode)
- [Operations & Configuration](references/operations.md)
- [Workflow Schema Reference](references/workflow-schema.md)
- [Built-in Actions Reference](references/actions.md)
- [Expressions & Interpolation Reference](references/expressions.md)
- [Workflow Patterns](references/patterns.md)
- [Error Handling Reference](references/error-handling.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow definitions, MCP tool-call payloads, configuration snippets, and DAG diagrams in ASCII, Mermaid, or image formats.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
