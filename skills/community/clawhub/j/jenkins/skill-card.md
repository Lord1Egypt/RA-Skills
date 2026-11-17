## Description:

Interact with Jenkins CI/CD server via REST API. Use when you need to trigger builds, check build status, view console output, manage jobs, or monitor Jenkins nodes and queue. Supports deployment to different Jenkins instances via environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoway](https://clawhub.ai/user/guoway)

### License/Terms of Use:


## Use Case:

Developers and CI/CD operators use this skill to inspect Jenkins jobs, trigger or stop builds, check build status, retrieve console output, and monitor queue or node state across Jenkins instances configured by environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger or stop Jenkins builds using real Jenkins credentials, including potentially high-impact deployment or production jobs.

Mitigation: Use a narrowly scoped Jenkins service account and require human approval before triggering or stopping production or deployment jobs.

Risk: Build parameters and console output can expose secrets or sensitive operational details.

Mitigation: Avoid passing secrets as build parameters, restrict log access, and review console output before sharing it outside the authorized team.

Risk: Credentials and API requests could be exposed if Jenkins is configured over an insecure endpoint.

Mitigation: Configure JENKINS_URL with HTTPS and store JENKINS_USER and JENKINS_API_TOKEN only in approved secret-management mechanisms.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JENKINS_URL, JENKINS_USER, and JENKINS_API_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
