## Description:

Enables agents to manage KoboToolbox projects, submissions, and exports through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and KoboToolbox users use this skill to inspect assets and submissions, create or deploy projects, export data, and manage submission validation or deletion through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can lead to installation of unverified CLI software; the remote installer and hosted connector implementation were not verified.

Mitigation: Review installation separately and prefer a pinned, verified CLI release. Check automatic skill synchronization, connect only the intended KoboToolbox account and data, and follow the documented confirmation steps for writes and deletions.

## Reference(s):

- [KoboToolbox](https://www.kobotoolbox.org)
- [KoboToolbox API documentation](https://support.kobotoolbox.org/api.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON payloads, shell commands, and structured connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected KoboToolbox account and selected action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
