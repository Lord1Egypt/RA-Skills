## Description:

Operate Opsgenie alerts through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve alert details and manage Opsgenie alerts through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run a remote installer before the CLI release is verified.

Mitigation: Install a fixed, verified oo CLI release yourself and review its automatic skill-synchronization settings before enabling it.

Risk: The remote installers and server-side connector implementation have not been verified.

Mitigation: Review the setup path and confirm the connector behavior meets your security requirements before handling Opsgenie data.

## Reference(s):

- [Opsgenie API documentation](https://docs.opsgenie.com/docs/api-overview)
- [Opsgenie product page](https://www.atlassian.com/software/opsgenie)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads, CLI commands, and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation; closing alerts requires explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
