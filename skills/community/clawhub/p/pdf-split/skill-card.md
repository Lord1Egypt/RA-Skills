## Description: <br>
Splits PDF files locally into single pages or selected page ranges, with support for batch processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to split local PDF files into page-level or range-based outputs without uploading the source documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads PDF files from user-specified paths and writes split PDFs to a chosen output directory. <br>
Mitigation: Run it only on PDFs and output paths you intend to process, and review the output directory and filename prefix before execution. <br>
Risk: The skill depends on the pdf-lib npm package to parse and write PDFs. <br>
Mitigation: Install dependencies from trusted npm sources and apply normal dependency review before use. <br>


## Reference(s): <br>
- [PDF Split on ClawHub](https://clawhub.ai/fly3094/pdf-split) <br>
- [pdf-lib npm package](https://www.npmjs.com/package/pdf-lib) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes split PDF files to a user-selected output directory; requires Node.js and the pdf-lib npm package.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
