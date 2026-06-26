## Description: <br>
Generate professional PDF documents from structured JSON data for styled titles, tables, lists, highlights, images, and page breaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flexrox](https://clawhub.ai/user/flexrox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn structured JSON content into styled PDF reports with text, headings, callouts, lists, tables, images, and page breaks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted JSON can point image sections at sensitive local file paths. <br>
Mitigation: Use trusted JSON inputs and review image paths before generating PDFs. <br>


## Reference(s): <br>
- [PDF Generator Schema Reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [PDF file generated from JSON input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to the CLI --output path, data.output path, or output.pdf by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
