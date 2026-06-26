## Description: <br>
Calls the Pincaimao Resume Diagnosis Assistant API to compare a candidate resume with a job description after the resume is uploaded and a cos_key is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and recruiting workflow agents use this skill to send a job description and uploaded resume reference to Pincaimao for resume diagnosis and match analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume files, job descriptions, and returned cos_key paths may contain sensitive personal or hiring data. <br>
Mitigation: Only provide files and job details intended for Pincaimao processing, treat cos_key values as sensitive, and avoid sharing credentials or unrelated confidential material. <br>
Risk: The scanner found no hidden code, unsafe persistence, credential handling, or malicious behavior, but benign scan results do not remove all operational risk. <br>
Mitigation: Review the skill text before use and avoid granting sensitive files, credentials, or account access unless that is required for the resume diagnosis workflow. <br>


## Reference(s): <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [Pincaimao API endpoint](https://api.pincaimao.com) <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-resume-diagnosis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown or raw API response text, with shell command examples for API invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can summarize the API answer for readability or return the raw answer when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
