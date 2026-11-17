## Description:

Adds run-scoped identity tokens and two-stage approval to operational ontology workflows, allowing agents to propose and validate actions while reserving commits for human tokens, with object-level marking and clearance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renlimin](https://clawhub.ai/user/renlimin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating agent workflows with proposal gates can use this skill to require verifiable run-scoped identities, keep agent actions at validation until a human commits them, and apply object-level access checks. It also supports decision fingerprint auditing and controlled MCP tool exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some referenced files were unavailable to the security scan, so its benign verdict has medium confidence and does not establish the behavior of those files.

Mitigation: Review and scan the unavailable referenced files before relying on them in your deployment.

Risk: Exposure of the signing secret could allow forged identity tokens.

Mitigation: Protect the secret using the documented restricted file permissions, and keep it out of logs, Markdown, and Git.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/renlimin/skills/ontology-identity-gate)
- [Publisher profile](https://clawhub.ai/user/renlimin)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python code examples and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover run-scoped identity, proposal and review flows, and object-level access checks.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
