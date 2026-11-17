## Description:

Use the OOMOL-connected Honeybadger account to report check-ins, deployments, events, and exceptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to report Honeybadger check-ins, deployments, events, and exceptions through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can run a remote CLI installer without clear user approval, and the external installer implementation is unverified.

Mitigation: Review and authorize the CLI installation separately before running the installer.

Risk: OOMOL processes Honeybadger payloads and holds the connected API key.

Mitigation: Confirm that OOMOL may handle the Honeybadger payloads and connected credential before enabling the connection.

Risk: Write actions change Honeybadger state.

Mitigation: Keep the required confirmation and review the exact payload and effect before each write action.

## Reference(s):

- [Honeybadger API documentation](https://docs.honeybadger.io/api/)
- [Honeybadger](https://www.honeybadger.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [Shell commands with JSON request payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation of the exact payload and effect before execution.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
