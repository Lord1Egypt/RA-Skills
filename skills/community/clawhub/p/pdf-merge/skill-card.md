## Description: <br>
Merges multiple PDF files locally, with optional compression and metadata editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-handling users use this skill to merge local PDFs, optionally reduce output size, and set document metadata from a Node.js CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool writes directly to the selected output path and may overwrite an existing file. <br>
Mitigation: Review the output path before running and use a new filename or backup when preserving existing files matters. <br>
Risk: The skill requires Node.js and the pdf-lib npm package. <br>
Mitigation: Install dependencies from trusted package sources and apply the user's normal dependency review process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fly3094/pdf-merge) <br>
- [pdf-lib package](https://www.npmjs.com/package/pdf-lib) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF file output with console status text and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to the specified output path; may overwrite an existing file.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
