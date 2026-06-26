## Description: <br>
Focused on multi-agent collaboration and communication scenarios, helping users build and manage complex distributed agent systems to achieve task decomposition, parallel processing, and collaborative work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design multi-agent system architectures, decompose work across agents, define communication protocols, and plan distributed collaboration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can read local design inputs and write generated architecture or configuration files to a selected output directory. <br>
Mitigation: Review input and output paths before running scripts, and run them only in an intended workspace. <br>
Risk: Configuration templates include placeholder security fields that users may be tempted to replace with real credentials. <br>
Mitigation: Use placeholders, environment references, or a secrets manager instead of embedding real secrets in generated or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/multi-agent-collaboration-communication) <br>
- [Multi-Agent System Architecture Patterns](references/architecture_patterns.md) <br>
- [Task Decomposition Strategies](references/task_decomposition.md) <br>
- [Agent Communication Protocol Design](references/communication_protocols.md) <br>
- [Workflow Templates](references/workflow_templates.md) <br>
- [Multi-Agent System Design Proposal Template](assets/templates/system-design-template.md) <br>
- [Agent Configuration File Template](assets/templates/agent-config-template.yaml) <br>
- [Intelligent Code Review System Example](assets/examples/code-review-system.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, JSON, Python, shell command, and plain-text diagram examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce design documents, architecture diagrams, agent role definitions, communication specifications, workflow code, and configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
