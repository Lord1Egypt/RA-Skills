## Description: <br>
Generates a Mermaid architecture diagram showing high-level component relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand, document, and review high-level component relationships in a codebase by producing a Mermaid architecture diagram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram generation may include sensitive or unnecessary repository structure when run over a broad private codebase. <br>
Mitigation: Provide a narrow scope for private or large repositories and review the generated Mermaid content before rendering. <br>
Risk: Generated architecture diagrams may omit relationships or simplify components in ways that mislead reviewers. <br>
Mitigation: Use the diagram as a review aid and compare it against the codebase before relying on it for documentation or PR decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-cartograph-architecture-diagram) <br>
- [Cartograph homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Mermaid flowchart code and a brief text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mermaid flowcharts summarize high-level component relationships and should usually be limited to 15-20 nodes.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
