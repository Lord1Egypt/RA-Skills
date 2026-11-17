## Description:

Use this skill to read, create, and update data in StackAI through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers with an OOMOL-connected StackAI account use this skill to inspect action schemas, run deployed flows, and retrieve metadata for previous runs through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code, and local changes may occur without separate approval.

Mitigation: Review the setup, install a CLI version you have verified, and approve its local changes separately.

Risk: Using the integration requires trusting OOMOL with submitted data and the StackAI connection; the hosted implementation remains unverified.

Mitigation: Review the integration and its data handling before connecting an account or submitting sensitive data.

## Reference(s):

- [StackAI API documentation](https://docs.stackai.com/)
- [oo CLI command reference and environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and normalized JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The run_flow action changes StackAI state and requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
