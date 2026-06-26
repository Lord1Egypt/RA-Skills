## Description: <br>
AP Classroom Agent automates AP Classroom course selection, assignment lookup, question navigation, answer selection, and quiz submission through a logged-in Chrome session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogerhyj](https://clawhub.ai/user/rogerhyj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to control a logged-in AP Classroom browser session, inspect coursework, select answers, and submit assignments. It is intended for Windows users with Chrome remote debugging and Node.js/Playwright available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act inside a logged-in College Board session, including selecting answers and submitting coursework. <br>
Mitigation: Use it only where automation is explicitly allowed by school and College Board policies, and manually review every action before submission. <br>
Risk: Chrome remote debugging on port 9223 can expose an authenticated browser session to local automation. <br>
Mitigation: Use a separate Chrome profile for this workflow and close the remote debugging browser session when finished. <br>
Risk: The artifact saves course data and screenshots locally, which may include sensitive educational content or account context. <br>
Mitigation: Inspect generated JSON and PNG files after use, delete files that are no longer needed, and avoid sharing the working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogerhyj/help-you-with-apclassroom-mcqs) <br>
- [Publisher profile](https://clawhub.ai/user/rogerhyj) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact release notes](artifact/RELEASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Console text, JSON state files, PNG screenshots, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Chrome remote debugging session on port 9223 and writes local course, homework, and screenshot artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata and package.json report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
