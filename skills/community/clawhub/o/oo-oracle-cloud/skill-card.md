## Description:

Manage Oracle Cloud Infrastructure resources through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect OCI tenancy, networking, compute, and monitoring resources, and to manage supported resources through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs an external installer whose behavior has not been audited.

Mitigation: Review the installation behavior and use a fixed CLI release before installing.

Risk: A potentially disruptive instance_action may be misclassified.

Mitigation: Require explicit approval and verify the target and effect before running instance_action.

## Reference(s):

- [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/)
- [OCI API documentation](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/usingapi.htm)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-oracle-cloud)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Natural language with oo CLI commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read OCI data or change cloud resources; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
