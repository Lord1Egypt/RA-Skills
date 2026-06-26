## Description: <br>
Generate structured execution plans for medical and molecular biology protocols such as RNA extraction, reverse transcription, qPCR, cell culture, CRISPR, or other healthcare/biomedical procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengbingrock](https://clawhub.ai/user/mengbingrock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and biomedical laboratory practitioners use this skill to turn a protocol task or supplied steps into protocol options or a structured execution plan for molecular biology and healthcare workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read protocol-like Markdown or Word files from the project root and use web searches for protocol references. <br>
Mitigation: Run it in a dedicated folder and remove patient data, confidential protocol details, or unpublished proprietary information before use. <br>
Risk: Generated biomedical procedures may be incomplete, unsuitable, or unsafe if treated as authoritative instructions. <br>
Mitigation: Have qualified personnel verify plans against official SOPs, safety rules, SDS and EHS requirements, and required institutional approvals before execution. <br>
Risk: Supplementary web references may be inaccurate or inappropriate for the user's lab context. <br>
Mitigation: Prefer manufacturer protocols, peer-reviewed literature, NIH or CDC guidance, and university SOPs, and review every cited source before relying on it. <br>


## Reference(s): <br>
- [Protocol Planning Guide](references/protocol-planning-guide.md) <br>
- [Medical and Healthcare Domain Knowledge](references/medical-domain-knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown protocol options or execution plans with checklists, timelines, troubleshooting tables, safety notes, and references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include web references and local protocol context when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
