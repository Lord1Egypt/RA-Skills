## Description: <br>
Invoice Scan extracts structured invoice and receipt data from images, scanned documents, and PDFs, validates arithmetic and document type, and exports results as JSON, CSV, or Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-muddle](https://clawhub.ai/user/mr-muddle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and finance operations teams use this skill to extract invoice fields, classify financial documents, validate totals, and prepare structured outputs for review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CLI mode sends full invoice images and extracted financial details, including potentially sensitive business and personal data, to Anthropic. <br>
Mitigation: Use agent-native mode when external processing is not approved; use CLI mode only after organizational approval for Anthropic processing. <br>
Risk: CLI mode depends on user-provided API credentials and npm dependencies. <br>
Mitigation: Use dedicated API credentials with appropriate limits and review the npm dependencies before installation in regulated or confidential environments. <br>


## Reference(s): <br>
- [Canonical Invoice Schema](references/canonical-schema.md) <br>
- [Validation Rules](references/validation-rules.md) <br>
- [Anthropic API endpoint (CLI mode)](https://api.anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, Excel, files, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional JSON, CSV, and Excel exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-native mode can format local exports; CLI mode requires an Anthropic API key and can save outputs to files.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
