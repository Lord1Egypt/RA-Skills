## Description: <br>
Generates practical manual QA checklists from code changes, separating terminal-verifiable checks from steps that need human judgment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipefreitag](https://clawhub.ai/user/felipefreitag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to turn PRs, commits, branches, staged changes, or unstaged diffs into concrete QA steps. It helps separate checks an agent can run in the terminal from interactive, visual, authenticated, or real-device checks that need a human. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested agent-run QA steps could touch external services, databases, authenticated sessions, or production-like data when the underlying code change involves them. <br>
Mitigation: Review proposed commands before approving execution and avoid production credentials, irreversible operations, or sensitive targets unless explicitly authorized. <br>
Risk: A generated QA checklist can miss behavior outside the reviewed diff or misclassify checks that require human judgment. <br>
Mitigation: Use the checklist as review guidance and keep human verification for interactive, visual, authenticated, email, mobile, and real-device flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/felipefreitag/manual-qa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown numbered checklist with labels for agent-testable and human-testable steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pass/fail results for agent-run steps when the user approves execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
