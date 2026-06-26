## Description: <br>
Fetch schedule, grades, and infractions from the Magister school portal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghuron](https://clawhub.ai/user/ghuron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query a Magister school portal account for student lists, schedules, grades, and absences using user-provided credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Magister credentials and can retrieve sensitive student records such as grades, schedules, and absences. <br>
Mitigation: Install and use it only for accounts and student records you are authorized to access, and store MAGISTER credentials securely outside shared prompts, logs, and repositories. <br>
Risk: Command output may expose grades, absences, schedules, or records for multiple students when parent credentials are used. <br>
Mitigation: Review outputs before sharing them and redact student-specific records that are not needed for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ghuron/magister) <br>
- [Publisher Profile](https://clawhub.ai/user/ghuron) <br>
- [Magister Portal](https://magister.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-shaped command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and MAGISTER_HOST, MAGISTER_USER, and MAGISTER_PASSWORD environment variables; command output may contain sensitive student records.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
