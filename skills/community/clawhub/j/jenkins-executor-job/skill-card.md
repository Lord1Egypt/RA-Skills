## Description:

Jenkins Executor Skill lets an agent list Jenkins jobs, trigger builds, check build status, retrieve build logs, and stop running builds for CI/CD and operations workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack084015](https://clawhub.ai/user/jack084015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release engineers, and operations teams use this skill to let an agent interact with Jenkins jobs for build orchestration, monitoring, log review, and stopping active builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jenkins credentials may be handled unsafely if real tokens are placed in packaged configuration.

Mitigation: Use environment-specific secrets management, keep real credentials out of config.json, and issue a least-privilege Jenkins API token.

Risk: Build trigger and stop actions can affect high-impact CI/CD or release jobs.

Mitigation: Restrict the token to approved jobs and add explicit approvals or job allowlists before granting access to production deploy or release jobs.

Risk: Jenkins API access over insecure transport can expose credentials or build data.

Mitigation: Require HTTPS for Jenkins connections and review the target Jenkins URL before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jack084015/skills/jenkins-executor-job)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [JSON-like tool responses with job metadata, build status, log excerpts, and operation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Build log output is limited to a recent excerpt by the artifact implementation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
