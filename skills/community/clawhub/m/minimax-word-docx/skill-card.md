## Description: <br>
MiniMax Word guides agents in generating professional .docx documents with the .NET OpenXML SDK while preserving headers, footers, tables of contents, tracked changes, complex tables, and styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, document authors, and business users use this skill to guide an agent in producing deliverable Word documents for reports, contracts, academic papers, project proposals, and news releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed artifact is instruction-only and does not bundle the .NET OpenXML SDK or document-generation code. <br>
Mitigation: Confirm the agent environment has the required Word/OpenXML tooling before relying on the skill for production documents. <br>
Risk: Complex document formatting may vary by generator implementation or document viewer. <br>
Mitigation: Open and validate generated .docx files in Microsoft Word or WPS before formal submission. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smseow001/minimax-word-docx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with optional code snippets and .docx file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Document output quality depends on the agent environment and available .NET OpenXML tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
