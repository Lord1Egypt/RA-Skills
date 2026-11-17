## Description: <br>
Parses academic paper PDFs to extract titles, abstracts, section structure, references, figures, and related structured information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, students, and individual knowledge workers use this skill to guide an agent through single-paper PDF parsing, metadata extraction, section analysis, and reference extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for local exec and write authority while processing PDF files. <br>
Mitigation: Review proposed commands before execution, use explicit file paths, and run it only in workspaces where PDF parsing and file writes are intended. <br>
Risk: PDF content and extracted results may include sensitive research or personal information. <br>
Mitigation: Avoid sensitive PDFs unless necessary, keep outputs in approved locations, and review generated files before sharing or relying on them. <br>
Risk: Optional callback behavior can send parsing results to an external destination. <br>
Mitigation: Provide a callback URL only when the destination is trusted and sending results there is intentional. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/paper-parse-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON/YAML examples, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local PDF reads, Python package installation, result file writes, and optional callback delivery.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
