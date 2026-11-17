## Description:

Elective helps agents work with the PKU course-selection CLI, including login and session tasks, course selection commands, CAPTCHA solver configuration, and auto-enrollment automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when maintaining or operating the PKU elective CLI, especially for login, dual-degree session handling, CAPTCHA solver setup, course selection commands, and auto-enrollment loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of login flows, stored credentials, and session files for the PKU elective CLI.

Mitigation: Confirm the intended account, credential source, and session location before using auto-login or session management commands.

Risk: CAPTCHA images may be sent to external recognition services when non-manual CAPTCHA backends are configured.

Mitigation: Use the manual CAPTCHA backend when challenge images should not be shared with external OCR services.

Risk: Auto-enrollment guidance can trigger repeated polling and course-selection actions.

Mitigation: Review target courses, polling interval, and authorization before launching auto-enrollment.

Risk: Dual-degree course views can miss courses from the other program if the wrong session or command posture is used.

Mitigation: Specify the correct dual-degree mode during login and use the separate schedule-focused workflow for general timetable questions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjsoj/skills/pku-elective)
- [Publisher profile](https://clawhub.ai/user/wjsoj)
- [PKU elective system](https://elective.pku.edu.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration details, and code-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational cautions for credentials, session files, CAPTCHA backends, dual-degree logins, and auto-enrollment behavior.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
