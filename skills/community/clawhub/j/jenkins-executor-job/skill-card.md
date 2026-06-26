## Description: <br>
Manages the Jenkins job lifecycle by listing jobs, triggering builds, checking build status, retrieving build logs, and stopping running builds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack084015](https://clawhub.ai/user/jack084015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to let an agent inspect Jenkins jobs, start parameterized or non-parameterized builds, monitor their status, read console logs, and stop selected running builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to start and stop Jenkins builds. <br>
Mitigation: Use a dedicated least-privilege Jenkins API token and require human approval before triggering or stopping builds. <br>
Risk: The skill can retrieve build logs that may contain secrets or internal operational details. <br>
Mitigation: Treat returned logs as sensitive and limit the Jenkins account to approved jobs and environments. <br>
Risk: The skill connects directly to Jenkins using configured credentials. <br>
Mitigation: Prefer HTTPS Jenkins endpoints and store credentials outside the skill artifact using the deployment platform's secret management. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack084015/jenkins-executor-job) <br>
- [Publisher profile](https://clawhub.ai/user/jack084015) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration] <br>
**Output Format:** [JSON responses from Jenkins job, build, status, log, and stop operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Build log output is truncated to the last 3000 characters by the skill implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
