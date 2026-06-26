## Description: <br>
Writes, expands, and reviews Chinese product requirements documents (PRDs) with strict section numbering and detailed micro-interaction coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kira2red](https://clawhub.ai/user/kira2red) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and product teams use this skill to draft, expand, and review Chinese PRDs from raw requirements, sketches, or existing documents. It focuses on business rules, interaction states, edge cases, and supporting PlantUML or Mermaid diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram workflows can create or overwrite local diagram files. <br>
Mitigation: Keep generated PRDs and diagram artifacts under version control and review file changes before accepting them. <br>
Risk: The referenced manual PlantUML helper is a local Python command. <br>
Mitigation: Inspect the helper before running it and execute it only in a trusted workspace. <br>
Risk: The Mermaid HTML template loads JavaScript from a CDN. <br>
Mitigation: Open generated HTML only when external CDN loading is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kira2red/kira-product-monster-prd) <br>
- [Flow template](references/flow-template.html) <br>
- [Mermaid runtime CDN](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PlantUML, Mermaid HTML, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite local PRD diagram files when the diagram workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
