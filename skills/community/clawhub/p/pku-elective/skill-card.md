## Description: <br>
Elective helps agents work with a Rust CLI for PKU course selection, including login and session handling, course browsing, CAPTCHA configuration, and auto-enrollment automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when maintaining or using the PKU elective CLI, debugging course-selection commands, configuring CAPTCHA recognition, or guiding auto-enrollment workflows. It is not intended for general course schedule questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward accessing stored PKU credentials and persisted elective sessions. <br>
Mitigation: Confirm the account, credential source, session location, and consent before login or session-changing commands are used. <br>
Risk: Auto-enrollment workflows can act on course targets and run polling loops that affect a student's enrollment state. <br>
Mitigation: Confirm target course IDs, degree track, polling duration, stop conditions, and rollback or removal steps before launch. <br>
Risk: CAPTCHA backends may send CAPTCHA images or related data to external recognition services. <br>
Mitigation: Confirm the selected CAPTCHA backend and any service credentials before configuring or using automated recognition. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjsoj/pku-elective) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe login, CAPTCHA, session, and auto-enrollment actions that should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
