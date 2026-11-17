## Description:

Automates Jenkins build triggers for configured worker and user projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengzongxin](https://clawhub.ai/user/chengzongxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to trigger Jenkins builds for configured worker and user projects and report build status details back to the requester.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger Jenkins CI builds.

Mitigation: Use it only with an intended Jenkins instance and require explicit confirmation before triggering any build.

Risk: The artifact includes plaintext administrator credentials.

Mitigation: Remove or rotate the published credentials and prefer a least-privilege Jenkins user or token.

Risk: Browser automation may act through an existing logged-in Jenkins session.

Mitigation: Confirm the target Jenkins job and session before clicking Build Now or using an equivalent API call.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengzongxin/skills/jenkins-build)
- [Publisher profile](https://clawhub.ai/user/chengzongxin)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports build number, current status, estimated time when available, and a Jenkins page link.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
