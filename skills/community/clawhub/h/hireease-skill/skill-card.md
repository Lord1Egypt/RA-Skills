## Description: <br>
Tailor a client resume for a matching new job, generate a PDF from the tailored LaTeX, and record the application in the HireEase portal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibrahimsaleem](https://clawhub.ai/user/ibrahimsaleem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate HireEase resume tailoring, PDF generation, and application recording for a selected client and job posting. It supports either user-provided job details or agent-assisted job selection when browsing is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send HireEase credentials to a user-provided base URL. <br>
Mitigation: Use only a trusted HireEase base URL, ideally an official allowlisted domain, and prefer scoped or rotatable credentials. <br>
Risk: The skill can create or use a public Google Drive resume link. <br>
Mitigation: Review the Google account, Drive sharing settings, and public resume link before recording a real application. <br>
Risk: The skill can submit or record a real job application in HireEase. <br>
Mitigation: Confirm the selected job, tailored PDF, application fields, and submission intent before allowing the final application record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibrahimsaleem/hireease-skill) <br>
- [HireEase primary base URL](https://hireease.me) <br>
- [HireEase alternate base URL](https://hireease-s33h.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with saved LaTeX and PDF file paths, application details, and warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save tailored LaTeX and generated PDF files under scripts/output/ and may record an application when the user confirms real submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
