## Description:

Guides an agent in using olares-cli cluster to inspect and operate the per-user Kubernetes runtime view for Olares pods, workloads, application spaces, jobs, cronjobs, nodes, and middleware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olares](https://clawhub.ai/user/olares)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to translate Olares cluster-runtime questions into safe olares-cli cluster reads, log inspection, status checks, and confirmed mutations on pods, workloads, jobs, and cronjobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Middleware password output can expose administrator credentials when password display is explicitly requested.

Mitigation: Keep redaction defaults, require clear user intent before showing passwords, and avoid shared terminals, transcripts, logs, CI jobs, or files for password output.

Risk: Cluster mutation commands can change runtime state, and scripted confirmation bypasses can make those changes easier to trigger.

Mitigation: Confirm user intent before destructive verbs and treat server authorization responses as authoritative.

## Reference(s):

- [Olares Cluster Skill Definition](SKILL.md)
- [Olares Cluster Application Reference](references/olares-cluster-application.md)
- [Olares Cluster CronJob Reference](references/olares-cluster-cronjob.md)
- [Olares Cluster Job Reference](references/olares-cluster-job.md)
- [Olares Cluster Middleware Reference](references/olares-cluster-middleware.md)
- [Olares Cluster Pod Reference](references/olares-cluster-pod.md)
- [Olares Cluster Workload Reference](references/olares-cluster-workload.md)
- [ClawHub Skill Page](https://clawhub.ai/olares/skills/olares-cluster)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include table, JSON, or YAML command-output handling guidance depending on the olares-cli cluster verb.]

## Skill Version(s):

4.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
