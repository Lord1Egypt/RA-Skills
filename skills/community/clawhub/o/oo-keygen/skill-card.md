## Description:

Use the oo CLI to inspect and manage Keygen resources through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Keygen accounts and manage licenses, users, machines, products, policies, and related resources. It can also validate license keys and IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says check-ins and heartbeats are treated as harmless reads even though they can change state.

Mitigation: Correct the action classifications and require user authorization before check-ins or heartbeat actions, including starting and maintaining heartbeat monitoring.

Risk: The hosted connector implementation and remote CLI installer have not been audited.

Mitigation: Use a suitably restricted Keygen account, understand that OOMOL handles its credentials and requests, and review and verify the CLI installation and bundled skill changes.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Keygen](https://keygen.sh)
- [Keygen API documentation](https://keygen.sh/docs/api/)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance, Text]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific JSON inputs and Keygen response data]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
