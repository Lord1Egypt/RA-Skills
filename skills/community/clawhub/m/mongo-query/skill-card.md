## Description:

MongoDB Query helps agents inspect MongoDB databases for troubleshooting by listing databases and collections, running JSON queries, and checking connectivity over direct or Kubernetes service connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peintune](https://clawhub.ai/user/peintune)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to troubleshoot MongoDB deployments by asking an agent to list databases or collections, run targeted read queries, and return formatted results. It is intended for environments where users can provide approved MongoDB credentials and, when needed, Kubernetes namespace context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MongoDB connection strings can contain credentials, and the security evidence warns against storing passwords in TOOLS.md or command history.

Mitigation: Use least-privilege MongoDB credentials from a protected secret source, and avoid recording credentials in repository files, prompts, or shell history.

Risk: Kubernetes service-name connections can create port-forwards to services reachable by the active kubectl context.

Mitigation: Confirm the cluster context and namespace before use, restrict kubectl access to required services, and close port-forwards after the query completes.

Risk: Troubleshooting queries may return sensitive database records.

Mitigation: Query only approved databases and collections, keep result limits low, and avoid sharing returned records outside the authorized troubleshooting workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peintune/skills/mongo-query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command examples; query results are plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query output is limited by a configurable result limit, with a default of 10 documents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
