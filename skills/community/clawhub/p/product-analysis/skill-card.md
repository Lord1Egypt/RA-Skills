## Description: <br>
Product Analysis guides agents through structured product requirements analysis across fast, standard, and iteration workflows, producing Mermaid process diagrams, functional architecture, tracking plans, PRDs, and development tickets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghy1993](https://clawhub.ai/user/zhanghy1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, developers, and cross-functional product teams use this skill to convert feature requests, uploaded PRDs, or iteration briefs into structured product analysis, diagrams, implementation-ready specifications, and handoff documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PRDs, tracking plans, tickets, and diagrams may persist sensitive product requirements or implementation details as workspace files. <br>
Mitigation: Verify the output directory before use, avoid including highly sensitive requirements unless workspace retention is acceptable, and review generated files before sharing. <br>
Risk: Analytics and tracking-plan sections may raise privacy, consent, retention, or data-minimization concerns. <br>
Mitigation: Review tracking outputs with the appropriate privacy or compliance stakeholders before handing them to engineering. <br>
Risk: Generated product analysis can contain incorrect assumptions or incomplete requirements if source inputs are ambiguous. <br>
Mitigation: Use the built-in confirmation steps, quality checks, and product or engineering review before treating outputs as implementation requirements. <br>


## Reference(s): <br>
- [ClawHub product-analysis release page](https://clawhub.ai/zhanghy1993/product-analysis) <br>
- [Analysis Frameworks](references/analysis-frameworks.md) <br>
- [Flowchart Standards](references/flowchart-standards.md) <br>
- [Architecture Patterns](references/architecture-patterns.md) <br>
- [Exception Checklist](references/exception-checklist.md) <br>
- [Draw.io Standards](references/drawio-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents with Mermaid diagrams, optional Draw.io files, and inline shell commands for local validation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are saved to a per-run output directory; local scripts may validate Mermaid syntax, MECE structure, and document quality.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter declares v6.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
