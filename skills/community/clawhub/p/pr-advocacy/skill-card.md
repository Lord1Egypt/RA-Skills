## Description: <br>
Actively monitors, responds to, and drives pull request reviews to completion with real-time tracking list synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linux2010](https://clawhub.ai/user/Linux2010) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and maintainers use this skill to monitor pull requests, respond to reviewer feedback, address CI failures, and keep PR tracking records current until merge or closure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to actively manage PR review work, including branch changes, commits, comments, PR edits, and tracking-file writes. <br>
Mitigation: Restrict use to specific repositories and PRs, and require confirmation before commits, pushes, comments, PR edits, or tracking-file writes. <br>
Risk: The skill references a hard-coded local memory path for PR tracking data. <br>
Mitigation: Replace or disable the hard-coded path before use unless PR metadata should be stored there. <br>
Risk: Broad automated monitoring and persistence can record PR metadata outside the intended workspace. <br>
Mitigation: Review the configured storage location and retention expectations before deployment. <br>


## Reference(s): <br>
- [PR Advocacy on ClawHub](https://clawhub.ai/Linux2010/pr-advocacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, status procedures, and response templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose PR branch changes, review responses, commits, and tracking-file updates depending on agent permissions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
