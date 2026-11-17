## Description:

Use the connected BlazeMeter Service Virtualization account to read and update service mock templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to retrieve, list, and update BlazeMeter Service Virtualization service mock templates through their connected OOMOL account. Read operations return service data, while updates require confirmation of the exact payload and effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructs users to execute a remote CLI installer that was not verified.

Mitigation: Review the installer and explicitly approve CLI installation and any bundled skill changes before setup.

Risk: Connecting BlazeMeter through OOMOL entrusts it with credentials and connector requests.

Mitigation: Connect only the intended account and review the requested action and payload; preserve the required confirmation before template updates.

## Reference(s):

- [BlazeMeter Service Virtualization](https://www.blazemeter.com/)
- [BlazeMeter API Documentation](https://help.blazemeter.com/apidocs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-blaze-meter-service-virtualization)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON action results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action; updates require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
