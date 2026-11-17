## Description: <br>
Helps agents process Chinese PDFs by extracting text, running OCR, analyzing layout, extracting tables, and chunking content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for single-file Chinese PDF parsing, OCR, table extraction, layout analysis, and structured result generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests read, write, and command-execution ability for local PDF processing. <br>
Mitigation: Install only for trusted PDF workflows, review requested commands and file paths, and keep execution scoped to intended PDF processing tasks. <br>
Risk: The input schema includes a callback URL, and the security summary flags weakly scoped callbacks. <br>
Mitigation: Use callback URLs only when the destination is expected and trusted, and avoid sending sensitive document contents to untrusted endpoints. <br>
Risk: The artifact includes generic modify/delete operation language that could lead to unintended file changes. <br>
Mitigation: Limit write access to a dedicated output directory and require review before modifying or deleting non-PDF data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pdf-processor-cn-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and bash snippets, YAML configuration examples, and JSON-style result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce extracted text, table data, execution logs, and saved output files when the agent has write access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
