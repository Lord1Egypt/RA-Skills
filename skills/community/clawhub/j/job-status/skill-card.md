## Description:

Queries HPC/AI job status by jobId from a configured API endpoint and returns the jobState from the JSON response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bylikai](https://clawhub.ai/user/bylikai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and HPC/AI users use this skill to check the current status of submitted jobs and monitor whether jobs are pending, running, completed, failed, or otherwise blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job IDs and detailed job metadata are sent and received over plaintext HTTP.

Mitigation: Use an HTTPS endpoint or a trusted private network path before using the skill with confidential workloads.

Risk: The executable scripts do not enforce the numeric jobId validation described in metadata.

Mitigation: Add jobId validation in the Python and Bash entry points before constructing or sending requests.

Risk: Returned details can include operational metadata such as user IDs, commands, working directories, resource usage, and exit status.

Mitigation: Limit use to job IDs and environments where those returned details are acceptable to expose to the agent and its logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bylikai/skills/job-status)
- [Publisher profile](https://clawhub.ai/user/bylikai)
- [Configured job status API endpoint](http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON or concise text/table job-status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include returned job metadata such as status, timestamps, HPC ID, resource fields, command, workDir, and exit status when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
