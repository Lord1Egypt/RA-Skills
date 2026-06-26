## Description: <br>
Creates Harvard-style CVs, resumes, and cover letters as .docx files from user-provided background and application details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[midnightstudioai](https://clawhub.ai/user/midnightstudioai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job applicants and career-support agents use this skill to collect resume or cover-letter inputs, apply Harvard Office of Career Services formatting guidance, and generate submission-ready .docx documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated resumes and cover letters may contain personal contact, education, and employment details. <br>
Mitigation: Review generated files before sharing, store them only where appropriate, and delete local copies when they are no longer needed. <br>
Risk: The skill may install or rely on the Node.js docx package to create .docx files. <br>
Mitigation: Prefer a trusted or preinstalled docx dependency and confirm the package source before allowing installation in controlled environments. <br>
Risk: Incorrect dates, titles, or achievements in job-application documents can misrepresent the applicant. <br>
Mitigation: Use only user-provided facts and have the user verify all dates, titles, credentials, and wording before submission. <br>


## Reference(s): <br>
- [Harvard Office of Career Services](https://ocs.fas.harvard.edu) <br>
- [Harvard Resume and Cover Letter Rules](harvard-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance plus generated .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local resume and cover-letter documents; output should be reviewed for accuracy and privacy before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
