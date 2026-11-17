## Description:

Plugin Orchestration Protocol (POP) for Obsidian integration guides agents in orchestrating real-time multi-step Obsidian workflows over JSON-RPC WebSocket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toolate28](https://clawhub.ai/user/toolate28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and operate Obsidian automation pipelines that discover plugin actions, execute dependent steps, monitor progress, assess coherence, and handle pipeline failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can be used with broad authority over an Obsidian vault.

Mitigation: Require authentication enforcement, scope bridge permissions to the intended vault actions, and review requested operations before execution.

Risk: Pipeline steps may delete, export, call external AI tools, or run templates using sensitive vault content.

Mitigation: Require explicit approval for delete, export, external-AI, and template steps, and define redaction rules for vault content before those actions run.

Risk: Environment variables and ATOM tokens may be exposed or reused during orchestration.

Mitigation: Use an environment-variable allowlist and clear token handling rules, including redaction from logs and telemetry.

Risk: Host dependencies such as AutoFigure and Pandoc affect generated outputs and execution safety.

Mitigation: Pin and verify host dependencies before enabling pipelines that call figure generation or document export.

## Reference(s):

- [POP Protocol Specification](references/protocol-spec.md)
- [Pipeline Templates](references/pipeline-templates.md)
- [POP Plugin Catalog](references/plugin-catalog.md)
- [ClawHub Skill Page](https://clawhub.ai/toolate28/skills/pop-obsidian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC examples, TypeScript stubs, configuration details, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe Obsidian vault operations, bridge configuration, plugin actions, pipeline templates, and approval gates for risky steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
