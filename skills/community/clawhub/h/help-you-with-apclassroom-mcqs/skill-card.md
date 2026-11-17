## Description:

AP Classroom Agent helps an agent control a logged-in Chrome browser to inspect AP Classroom courses and assignments, capture questions, select answers, advance through quizzes, and submit work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogerhyj](https://clawhub.ai/user/rogerhyj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to operate AP Classroom in an already-authenticated browser, including course selection, assignment review, question capture, answer selection, navigation, and quiz submission. Because it can affect live coursework, use should be authorized and reviewed before any submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act as the logged-in College Board user and submit real coursework.

Mitigation: Run only in an isolated browser profile, verify the page, course, and assignment before use, and avoid submission scripts unless explicit human review and confirmation checks are added.

Risk: The skill can capture assignment screenshots and question content from an authenticated session.

Mitigation: Keep generated screenshots and state files local, delete them when no longer needed, and avoid sharing files that contain coursework or account context.

Risk: Answer selection and navigation depend on page state and selectors, so actions may affect the wrong answer, question, or assignment.

Mitigation: Review the current page and generated screenshots before advancing or submitting, and confirm every target action manually in high-stakes workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogerhyj/skills/help-you-with-apclassroom-mcqs)
- [Publisher profile](https://clawhub.ai/user/rogerhyj)
- [AP Classroom](https://apclassroom.collegeboard.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell and Node.js command examples, JavaScript automation scripts, and local screenshot or JSON state files created during use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connects to an existing Chrome session on localhost port 9223; scripts may save screenshots and local course or homework state files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
