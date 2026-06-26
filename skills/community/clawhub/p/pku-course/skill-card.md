## Description: <br>
Course helps agents work on the Rust CLI for PKU Teaching Platform (Beida Teaching Network/Blackboard Learn), including authentication, Blackboard content browsing, downloads, video listings, assignment handling, and submission workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when maintaining or operating the PKU Blackboard CLI for course files, recordings, announcements, assignments, authentication, and homework submission. It explicitly excludes course schedule and weekly timetable questions, which should use the treehole skill instead. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential use and saved Blackboard sessions are sensitive. <br>
Mitigation: Install only for PKU Blackboard CLI work, confirm the intended account before login, and know how to log out or remove the saved session from ~/.config/info/course/. <br>
Risk: Coursework actions such as assignment submission or file selection can affect a user's academic work. <br>
Mitigation: Confirm the course, assignment, submission target, and local file paths before running login, download, or submit commands. <br>


## Reference(s): <br>
- [ClawHub Course Skill](https://clawhub.ai/wjsoj/pku-course) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide account login, session management, file downloads, and assignment submission through the PKU Blackboard CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
