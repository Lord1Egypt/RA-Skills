## Description: <br>
Interact with Jenkins CI/CD servers through the REST API to trigger builds, inspect status and console output, manage jobs, and monitor nodes and queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoway](https://clawhub.ai/user/guoway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to inspect Jenkins jobs, trigger or stop builds, view logs, and monitor build infrastructure from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Triggering or stopping Jenkins builds can make real operational changes to CI/CD pipelines. <br>
Mitigation: Use a Jenkins account scoped to the intended jobs and confirm job names and build numbers before acting, especially for production deployments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON] <br>
**Output Format:** [JSON responses and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JENKINS_URL, JENKINS_USER, and JENKINS_API_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
