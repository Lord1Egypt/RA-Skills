## Description: <br>
HPC/AI job status query skill that fetches job status information by jobId from a specific API endpoint and parses the jobState field from the JSON response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bylikai](https://clawhub.ai/user/bylikai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and HPC/AI users can query a numeric job ID to check whether a computing job is pending, running, completed, failed, cancelled, or timed out. The skill is useful for monitoring job progress and returning status details from the configured job-status API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends job IDs to www.aicnic.cn over plain HTTP and may display detailed job metadata. <br>
Mitigation: Use only when job IDs and returned metadata are safe to expose; avoid confidential workloads unless this exposure is acceptable. <br>
Risk: The installer can install an unpinned dependency and replace an existing local skill directory. <br>
Mitigation: Review the installer before running it and install in a controlled environment with dependency and backup expectations confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bylikai/job-status) <br>
- [Job status API endpoint](http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON response or concise text/table status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success, jobId, status, message, timestamp, and optional job metadata or error details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
