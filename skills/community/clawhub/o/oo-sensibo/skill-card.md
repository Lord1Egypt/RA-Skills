## Description:

Use Sensibo to read device details and AC states, list linked devices, and update AC state through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a Sensibo-connected account can ask an agent to inspect linked devices and their current or previous AC states, or change an AC state when they confirm the exact action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup executes a downloaded CLI installer that the security review says remains unverified.

Mitigation: Review and approve the CLI installation separately before running it.

Risk: The CLI may make automatic changes to other agents' skills during installation or synchronization.

Mitigation: Review those changes and disable skill synchronization if they are unwanted.

Risk: Changing an AC state affects the user's Sensibo device.

Mitigation: Confirm the exact action payload and effect with the user before running it.

## Reference(s):

- [Sensibo homepage](https://home.sensibo.com)
- [Sensibo API documentation](https://support.sensibo.com/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing AC actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
