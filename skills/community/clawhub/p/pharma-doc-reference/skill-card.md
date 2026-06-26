## Description: <br>
A pharmaceutical document reference library that provides document catalogs, content requirements, exemplar slots, and dependency topology for agent-assisted pharma document work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users in pharma medical affairs, market access, regulatory, compliance, and commercial teams use this skill to look up document types, content slots, exemplar availability, and document dependency relationships. When Universal Task OS is available, agents can use the reference material to structure pharma document planning and drafting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells the agent to automatically install and load Universal Task OS without a clear user approval step. <br>
Mitigation: Review and install Universal Task OS separately before document generation, or require explicit user approval before dependency installation. <br>
Risk: Enterprise templates may contain patient information, product secrets, or commercial confidential data. <br>
Mitigation: Only add enterprise templates after removing patient information, product secrets, and commercial confidential data. <br>


## Reference(s): <br>
- [Document Catalog](references/document-catalog.md) <br>
- [Content Requirements](references/content-requirements.md) <br>
- [Exemplars](references/exemplars.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/pharma-doc-reference) <br>
- [Publisher Profile](https://clawhub.ai/user/wangjiaocheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and structured reference guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pharma document catalogs, content slot lists, exemplar placeholders, and dependency topology as reference inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
