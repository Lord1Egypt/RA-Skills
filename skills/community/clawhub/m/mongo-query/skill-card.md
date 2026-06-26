## Description: <br>
Query MongoDB databases for debugging and troubleshooting, including listing databases and collections, running JSON queries, checking connectivity, and connecting directly or through Kubernetes port-forwarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peintune](https://clawhub.ai/user/peintune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect MongoDB state during debugging and troubleshooting. It helps an authorized agent list databases and collections, run bounded MongoDB queries, and connect through direct hosts or Kubernetes services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs credential-bearing MongoDB connection strings, and the security summary warns against storing full connection strings in project notes or source control. <br>
Mitigation: Use a least-privilege, preferably read-only database account; provide credentials only at runtime; and keep full connection strings out of TOOLS.md and version-controlled files. <br>
Risk: Kubernetes port-forward mode can connect the agent to the wrong service or namespace if the active context is incorrect. <br>
Mitigation: Confirm the Kubernetes context, namespace, and service name before running port-forward mode, especially against production clusters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peintune/mongo-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON returned from MongoDB queries, with Markdown guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MongoDB URI; --json returns raw JSON; the default query limit is 10.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
