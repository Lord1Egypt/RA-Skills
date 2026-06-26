## Description: <br>
Helps an agent use olares-cli cluster to inspect and manage Olares ControlHub cluster resources such as pods, workloads, applications, jobs, cronjobs, nodes, namespaces, and middleware. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olares](https://clawhub.ai/user/olares) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Olares cluster runtime state, tail logs, review Kubernetes-style resource YAML, and perform confirmed maintenance actions through olares-cli cluster. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide destructive cluster actions such as deleting pods, restarting workloads, scaling workloads to zero, suspending cronjobs, or rerunning jobs. <br>
Mitigation: Confirm user intent before destructive actions, review generated commands before execution, and avoid --yes unless deliberately scripting. <br>
Risk: Middleware inventory can expose sensitive credentials when --show-passwords is used. <br>
Mitigation: Use the redacted default output and only request --show-passwords when the destination will not be logged, stored, or shared. <br>
Risk: The active Olares profile determines what the agent can see and change. <br>
Mitigation: Check the active profile and surface server authorization errors rather than assuming local cached context is authoritative. <br>


## Reference(s): <br>
- [cluster pod](references/olares-cluster-pod.md) <br>
- [cluster workload](references/olares-cluster-workload.md) <br>
- [cluster application](references/olares-cluster-application.md) <br>
- [cluster job](references/olares-cluster-job.md) <br>
- [cluster cronjob](references/olares-cluster-cronjob.md) <br>
- [cluster middleware](references/olares-cluster-middleware.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include table, JSON, YAML, or log-output interpretation from olares-cli cluster commands.] <br>

## Skill Version(s): <br>
4.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
