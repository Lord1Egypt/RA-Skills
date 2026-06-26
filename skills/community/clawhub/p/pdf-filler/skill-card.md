## Description: <br>
Extract and fill PDF AcroForm fields with a multi-backend fallback chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qubit999](https://clawhub.ai/user/qubit999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect PDF AcroForm field schemas and fill forms from JSON values. It is useful for one-off form completion, batch filling, and PDFs that need fallback handling across multiple PDF backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Completed PDFs may contain sensitive personal, legal, or business information and may be returned through the current chat or workspace attachment channel. <br>
Mitigation: Use the skill only with PDFs the user is comfortable having the agent process, keep outputs inside the workspace, and confirm the delivered filename and filled-field count. <br>
Risk: Checkboxes and radio buttons can be left unset or defaulted incorrectly if the agent omits uncertain fields. <br>
Mitigation: Extract the schema first, copy field names and option values exactly, explicitly set checkbox and radio values where possible, and review the fill summary for unset fields before relying on the PDF. <br>
Risk: The skill depends on the external oc-pdf-filler package and optional PDF backends such as pdfrw, PyMuPDF, and pdftk. <br>
Mitigation: Install only trusted package versions and verify available backends before processing PDFs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qubit999/pdf-filler) <br>
- [Project homepage](https://github.com/qubit999/oc-pdf-filler) <br>
- [Backend fallback chain](references/BACKENDS.md) <br>
- [Field type value contract](references/FIELD_TYPES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples; generated artifacts are schema JSON files and filled PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The fill command prints a JSON summary including backend choice, output path, filled fields, missing fields, failed fields, and unset checkbox or radio fields.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
