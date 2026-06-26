## Description: <br>
Convert PDF to Markdown using local processing. No external API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifei68801](https://clawhub.ai/user/lifei68801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users can use this skill to convert local PDF documents into clean Markdown without sending document content to an external API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing PDFs with a local parser can expose users to risks from files they do not trust. <br>
Mitigation: Install pdfplumber from a trusted source and run the converter only on PDFs you are comfortable processing locally. <br>
Risk: Providing an output path writes extracted Markdown content to that location. <br>
Mitigation: Choose the output path deliberately and review the generated Markdown before relying on or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lifei68801/pdf2md-clean) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown text printed to stdout or written to a .md file, with setup and usage commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and pdfplumber; reads a local PDF and optionally writes a Markdown output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
