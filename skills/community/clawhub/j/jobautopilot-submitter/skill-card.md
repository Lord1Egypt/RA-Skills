## Description: <br>
Automatically fills and submits job applications by opening application pages, filling multi-step forms, uploading tailored resume and cover letter files, confirming submission, and updating the local job tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerronl](https://clawhub.ai/user/jerronl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to automate filling and submitting approved job applications from a local tracker, including resume uploads, cover letter fields, work history, education, dropdowns, and EEOC-style questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read configured resume and application files that contain sensitive personal data. <br>
Mitigation: Restrict resume and upload directories before use, and review configured file paths before allowing uploads. <br>
Risk: The skill can upload local files and submit job application forms through browser automation. <br>
Mitigation: Run only on application pages the user has approved, review generated actions before execution, and verify successful submission on the target site. <br>
Risk: The skill may answer language, work authorization, demographic, or EEOC-style questions using configured values or defaults. <br>
Mitigation: Provide explicit current answers for sensitive application questions instead of relying on defaults. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jerronl/jobautopilot-submitter) <br>
- [Publisher Profile](https://clawhub.ai/user/jerronl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status updates with generated shell commands and tracker edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser automation, local environment variables, local resume files, and local tracker state.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata; artifact frontmatter reports 1.3.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
