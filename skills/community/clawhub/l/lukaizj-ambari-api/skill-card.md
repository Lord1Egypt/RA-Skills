## Description:

Manage Hadoop clusters via Ambari REST API, including service start, stop, and restart operations, component operations, and cluster monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukaizj](https://clawhub.ai/user/lukaizj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cluster administrators use this skill to manage Ambari-backed Hadoop clusters, inspect cluster state, and prepare commands for service or component operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live Ambari service and component start, stop, and restart operations that may disrupt production clusters.

Mitigation: Review commands before execution, use least-privilege Ambari credentials, and treat service changes as administrative actions that require operational approval.

Risk: Cluster credentials may be supplied on the command line and stored in a plaintext local configuration file.

Mitigation: Avoid real passwords on the command line, protect or replace the local config file with an approved secret-management process, and rotate credentials after testing.

Risk: The helper client disables TLS certificate verification by default.

Mitigation: Enable certificate verification or configure a trusted CA bundle before connecting to production Ambari servers.

## Reference(s):

- [API Endpoints](references/api-endpoints.md)
- [Examples](references/examples.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ambari REST operation guidance, helper-script commands, status output interpretation, and configuration steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
