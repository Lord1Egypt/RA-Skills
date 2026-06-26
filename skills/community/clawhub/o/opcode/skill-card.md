## Description: <br>
Opcode lets AI agents define persistent workflow templates and run them over an SSE daemon with DAG execution, scheduling, built-in actions, interpolation, reasoning steps, and a secret vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rendis](https://clawhub.ai/user/rendis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use Opcode to define reusable workflow templates, execute and monitor long-running or scheduled agent workflows, resolve human-in-the-loop decisions, and visualize workflow DAGs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opcode installs a persistent local automation daemon with broad shell, filesystem, network, scheduling, and secret-handling authority. <br>
Mitigation: Install only when that authority is intended, pin and review the upstream Go package, and run the daemon as a low-privilege OS user. <br>
Risk: The SSE endpoint and optional web panel expose workflow control over the configured listener. <br>
Mitigation: Bind the service to localhost or protect it with authentication and network controls before use beyond a local trusted environment. <br>
Risk: Default filesystem and network controls are permissive, and shell execution can run local commands. <br>
Mitigation: Configure filesystem deny/read/write restrictions, use network proxy or firewall controls, and audit scheduled workflows and stored history regularly. <br>
Risk: Vault keys protect stored secrets and should be treated as highly sensitive. <br>
Mitigation: Avoid command-line vault keys, use environment variables or a secrets manager, and treat OPCODE_VAULT_KEY as equivalent to access to stored secrets. <br>


## Reference(s): <br>
- [Opcode ClawHub Page](https://clawhub.ai/rendis/opcode) <br>
- [Opcode Repository](https://github.com/rendis/opcode) <br>
- [Operations & Configuration](references/operations.md) <br>
- [Built-in Actions Reference](references/actions.md) <br>
- [Workflow Schema Reference](references/workflow-schema.md) <br>
- [Expressions & Interpolation Reference](references/expressions.md) <br>
- [Workflow Patterns](references/patterns.md) <br>
- [Error Handling Reference](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, JSON, Markdown, Code] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, configuration snippets, and diagram outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tool responses may include workflow status JSON, ASCII or Mermaid DAG diagrams, and base64-encoded PNG diagrams.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence; artifact frontmatter reports 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
