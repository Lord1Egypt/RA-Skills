## Description: <br>
Paper Parse analyzes academic papers from a PDF attachment or URL and produces two Markdown reports: an in-depth researcher-focused analysis and a concise summary of the paper's core logic, findings, and value. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sterlingfrank1](https://clawhub.ai/user/Sterlingfrank1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and analysts use this skill to convert an academic paper into a dual-mode reading report that preserves methodology, findings, key data, theoretical contributions, and practical implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch or process paper PDFs from user-provided URLs or attachments. <br>
Mitigation: Use explicit prompts that name the intended PDF or URL, and avoid sensitive unpublished documents unless the runtime and storage are trusted. <br>
Risk: Shell-based PDF extraction can be sensitive to unsafe paths or URLs. <br>
Mitigation: Rely on the platform or shell wrapper to handle paths and URLs safely before extraction. <br>


## Reference(s): <br>
- [Part A report template](references/part-a-template.md) <br>
- [Part B report template](references/part-b-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Files, Shell commands] <br>
**Output Format:** [Markdown report file with a brief text handoff message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report contains Part A and Part B sections separated by a horizontal rule.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
