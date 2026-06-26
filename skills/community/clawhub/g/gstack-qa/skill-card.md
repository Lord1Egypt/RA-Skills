## Description: <br>
Systematically QA test a web application and fix bugs found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loocor](https://clawhub.ai/user/loocor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run structured QA on web applications, document issues with evidence, fix eligible bugs, re-verify changes, and produce ship-readiness reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can actively test a web application, submit forms, edit source code, and create git commits. <br>
Mitigation: Use it on a clean feature branch against staging or disposable test accounts, then review screenshots, reports, diffs, and commits before pushing or deploying. <br>
Risk: Browser sessions and authentication flows may expose sensitive accounts or production workflows if scoped poorly. <br>
Mitigation: Avoid production cookies, live destructive workflows, and privileged credentials; prefer test accounts and explicit target scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loocor/gstack-qa) <br>
- [Publisher profile](https://clawhub.ai/user/loocor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with screenshots, repro steps, health scores, fix summaries, commit references, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create QA report files, screenshots, code edits, and git commits when authorized by the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
