## Description: <br>
Automatically downloads student homework from QQ email, extracts ZIP submissions, grades code against assignment templates with AI, and generates an Excel grade report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaouuu](https://clawhub.ai/user/yaouuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to collect homework submitted as QQ email ZIP attachments, match submissions to an assignment template, produce AI-generated scores and comments, and export the results to Excel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a QQ mailbox and downloads unread ZIP attachments. <br>
Mitigation: Use a dedicated mailbox or app-specific authorization code and limit the mailbox to homework submissions intended for grading. <br>
Risk: Downloaded homework archives are untrusted input and may contain unsafe paths or unexpected files. <br>
Mitigation: Run the skill in an isolated working directory and only use a revised or reviewed version that validates ZIP contents and sanitizes filenames before extraction. <br>
Risk: Student submissions and reference answers are sent to an external AI provider for grading. <br>
Mitigation: Confirm that sharing this data with the AI provider is allowed by the course, institution, and applicable privacy requirements before use. <br>
Risk: The artifact contains local code execution behavior for grading Python files. <br>
Mitigation: Remove or sandbox local code execution before using the skill with untrusted student submissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yaouuu/homework-gader-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yaouuu) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, API Calls] <br>
**Output Format:** [JSON response containing the generated Excel file path, with an .xlsx report written to disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires assignment_id, QQ email account, QQ email authorization code, assignment templates, and an AI provider API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
