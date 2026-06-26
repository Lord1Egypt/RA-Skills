## Description: <br>
Instruction-only workflow for formatting, editing, and creating Google Docs using the existing gog skill/CLI while relying on gog for all Google Docs and Drive operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastiangansca](https://clawhub.ai/user/sebastiangansca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and document authors use this skill to create formatted Google Docs from Markdown, update placeholders or sections, make small edits, and verify the result through gog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Docs write operations can overwrite or delete document content, especially clears, full rewrites, large replacements, or edits to shared work documents. <br>
Mitigation: Confirm the target document and intended change before writing, inspect or export the document first, and prefer bounded replacements or a backup copy for full rewrites. <br>
Risk: The workflow depends on a separate gog tool with access to Google Docs, and temporary exports can contain sensitive document content. <br>
Mitigation: Use only a trusted, authenticated gog setup for the intended Google account, review document IDs before changes, and remove temporary exports when no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; delegates Google Docs and Drive operations to gog.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
