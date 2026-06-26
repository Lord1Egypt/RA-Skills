## Description: <br>
Automates triggering Jenkins build jobs for worker and user application packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzongxin](https://clawhub.ai/user/chengzongxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release operators use this skill to open or trigger local Jenkins jobs for configured worker and user projects and report the build status link back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documented admin-style Jenkins credentials may be valid and could allow excessive access. <br>
Mitigation: Remove the documented admin/admin credential if it is valid, rotate it, and use a least-privilege Jenkins token or account. <br>
Risk: The skill can start Jenkins CI jobs through an authenticated browser session without a clear confirmation step. <br>
Mitigation: Require explicit user confirmation of the target Jenkins job before triggering any build. <br>
Risk: The skill is intended for a local Jenkins instance and may trigger the wrong environment if reused broadly. <br>
Mitigation: Install and run it only for the intended local Jenkins instance and confirm the Jenkins URL before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengzongxin/jenkins-build) <br>
- [Publisher profile](https://clawhub.ai/user/chengzongxin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with Jenkins build status details and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include build number, queue or execution status, estimated time when available, and a Jenkins page link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
