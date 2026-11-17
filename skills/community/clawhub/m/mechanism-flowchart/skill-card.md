## Description:

Generates Mermaid flowchart code and visual representations of medical mechanisms, pathophysiology, and drug action pathways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and medical content authors use this skill to turn mechanism descriptions into Mermaid diagrams for pathophysiology, disease pathway, drug action, presentation, and publication figure workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path uses unnecessary unpinned dependencies.

Mitigation: Remove unnecessary dependencies or pin and verify packages before installation.

Risk: Mermaid output generated from untrusted text can carry rendering risk.

Mitigation: Treat generated Mermaid as untrusted content and render it with a restrictive Mermaid security configuration.

Risk: The activation scope is broader than the stated medical diagram purpose.

Mitigation: Invoke the skill only for documented medical mechanism and pathophysiology diagram tasks, and confirm scope before execution.

Risk: Stress and boundary scenarios showed weaker consistency in the audit evidence.

Mitigation: Use fixed output sections for assumptions, constraints, risks, unresolved items, and fallback behavior when inputs are incomplete or complex.

## Reference(s):

- [Mechanism Flowchart Guidelines](artifact/references/guidelines.md)
- [Mermaid Documentation](https://mermaid.js.org/intro/)
- [Mermaid Flowchart Syntax](https://mermaid.js.org/syntax/flowchart.html)
- [Mermaid Live Editor](https://mermaid.live/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Mermaid code blocks and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams require a Mermaid renderer for visualization; complex mechanisms may need manual refinement.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
