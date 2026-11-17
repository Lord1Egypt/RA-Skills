## Description:

Verify deployments are healthy after release by checking endpoints, comparing response schemas, validating metrics, running smoke tests, verifying database migrations, and producing a deployment confidence report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment engineers use this skill immediately after a release to check service health, response shape, version alignment, recent errors, migration status, resource utilization, and deployment confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default endpoint discovery can contact unintended services when environment variables or local compose files contain broad service URLs.

Mitigation: Review target endpoints before execution and prefer an explicit .deploy-verify.json configuration for scoped checks.

Risk: Docker and systemd log checks can read host-wide operational logs if run from a privileged or shared host.

Mitigation: Run from a least-privileged environment scoped to the deployment being checked and limit Docker or journal access to relevant services.

Risk: Authenticated production requests may expose sensitive destinations or token use if headers are configured carelessly.

Mitigation: Use only reviewed endpoints and headers, avoid unnecessary authenticated requests, and confirm token handling before running production checks.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-readable text, JSON summaries, Markdown reports, Slack-formatted updates, and inline shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a deployment confidence score and recommendations such as keep, monitor, or consider rollback.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
