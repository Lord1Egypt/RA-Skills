## Description: <br>
Extracts text and slide information from user-provided PPTX PowerPoint files using local shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingqiu2180](https://clawhub.ai/user/jingqiu2180) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect PPTX files, count slides, and extract slide text into a structured summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local shell commands read user-provided PowerPoint files and may produce incomplete or misleading text when files are malformed or structurally complex. <br>
Mitigation: Run the commands only on intended .pptx files from trusted paths and review the extracted text before relying on it. <br>
Risk: The workflow strips slide XML to text and does not preserve images, charts, formatting, complex tables, or legacy .ppt content. <br>
Mitigation: Treat the result as a text-only aid and use a dedicated presentation parser when non-text content or formatting fidelity matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets and plain-text extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only extraction for .pptx files; images, charts, formatting, complex tables, and legacy .ppt files are not covered.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
