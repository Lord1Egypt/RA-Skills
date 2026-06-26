## Description: <br>
Manage Hadoop clusters via Ambari REST API, including service start, stop, restart, component operations, and cluster monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cluster operators use this skill to manage Ambari-backed Hadoop clusters, inspect services and hosts, and generate commands or code for service and component operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Ambari credentials in plaintext under the local skill directory. <br>
Mitigation: Use least-privilege Ambari accounts, restrict config file permissions, avoid production credentials in examples or shell history, and replace plaintext storage with a secret manager where possible. <br>
Risk: The skill can make authenticated changes to Hadoop services and components, including disruptive start, stop, and restart operations. <br>
Mitigation: Review generated commands before execution, verify target cluster, service, component, and host names, and monitor Ambari request status during changes. <br>
Risk: TLS certificate verification is disabled by default in the included client behavior. <br>
Mitigation: Review the TLS verification default before real cluster use and configure trusted CA certificates for production environments. <br>


## Reference(s): <br>
- [API Endpoints](references/api-endpoints.md) <br>
- [Examples](references/examples.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Release Page](https://clawhub.ai/lukaizj/lukaizj-ambari-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe Ambari REST API calls and local configuration steps for authenticated cluster operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
