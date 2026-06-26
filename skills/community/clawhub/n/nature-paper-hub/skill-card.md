## Description: <br>
Full-pipeline Nature-series journal writing assistant covering journal selection, literature review, manuscript drafting, figure generation, citation verification, pre-submission audit, cover letters, and reviewer responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1bai](https://clawhub.ai/user/yang1bai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, graduate students, and scientific writing teams use this agent to plan, draft, verify, format, and export manuscripts for Nature-series journals. It also supports figure planning, citation checks, bilingual paper reading, and reviewer-response drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, claims, references, paper identifiers, or private manuscript context may be sent to external literature, citation, or web services. <br>
Mitigation: Avoid confidential manuscripts, unpublished work, private PDFs, and sensitive reference lists unless external-search steps are disabled or the inputs are sanitized. <br>
Risk: The bundled literature index is reported by the security evidence as contaminated. <br>
Mitigation: Review or replace the bundled papers index before relying on it for manuscript positioning, citation recommendations, or evidence grounding. <br>
Risk: The security verdict is suspicious, even though the evidence does not identify overt malicious behavior. <br>
Mitigation: Review the skill and generated outputs before deployment, especially before installing dependencies or running export scripts. <br>


## Reference(s): <br>
- [Nature Paper Hub on ClawHub](https://clawhub.ai/yang1bai/nature-paper-hub) <br>
- [Publisher profile](https://clawhub.ai/user/yang1bai) <br>
- [Nature Portfolio author guidelines](https://www.nature.com/authors) <br>
- [CrossRef Works API](https://api.crossref.org/works) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and optional generated LaTeX, Word, PPTX, BibTeX, RIS, ENW, Zotero RDF, PDF, PNG, and SVG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external literature, citation, and web services when the user requests literature review, citation verification, or paper retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
