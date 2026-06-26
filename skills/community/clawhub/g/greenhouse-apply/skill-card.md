## Description: <br>
Submit job applications on Greenhouse by filling text fields, setting dropdowns, selecting phone country, uploading a resume, entering an email verification code, and submitting the form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buildingbrien](https://clawhub.ai/user/buildingbrien) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job applicants use this skill to automate Greenhouse application forms while reviewing every field before submission. It is intended for jobs the user intentionally wants to apply to and requires user-provided contact details, resume path, and custom answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive applicant data, including resumes, contact details, and custom application answers. <br>
Mitigation: Review every field before submission and provide only the resume path and answers intended for the current application. <br>
Risk: Email verification code handling can expose one-time codes or use stale codes. <br>
Mitigation: Manually supply the current code when possible, or limit email access to the relevant message for the current application. <br>
Risk: Using the skill on unintended jobs could submit applications the user did not mean to send. <br>
Mitigation: Use it only for a specific Greenhouse job the user intentionally wants to apply to and confirm the target job page before submission. <br>


## Reference(s): <br>
- [Greenhouse Field Mapping Reference](references/field-mapping.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/buildingbrien/greenhouse-apply) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code] <br>
**Output Format:** [Markdown guidance with browser automation steps and JavaScript evaluation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a browser automation tool, a local resume file path, user-supplied application answers, and access to the current email verification code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
