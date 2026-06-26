## Description: <br>
Access cloud storage (S3, GCS, Azure Blob) through a Pilot bridge agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to move files between agents and cloud storage through a Pilot bridge when direct storage access is unavailable or undesirable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge may run as a public long-running agent with cloud credentials and no documented access controls. <br>
Mitigation: Use dedicated least-privilege cloud credentials, keep the daemon private unless public access is required, and stop the bridge when the task is complete. <br>
Risk: Requests can target cloud buckets, prefixes, object paths, and actions that affect stored data. <br>
Mitigation: Restrict allowed buckets and prefixes, verify allowed senders, and validate requested actions and paths before transferring or exposing files. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot daemon, and cloud provider credentials for the bridge agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
