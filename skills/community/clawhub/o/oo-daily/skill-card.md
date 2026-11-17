## Description:

Manage Daily rooms and meeting tokens through the oo CLI, including reading room and domain settings and creating, updating, or deleting resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage Daily through an OOMOL-connected account: inspect domain and room settings, list rooms, create meeting tokens, and create, update, or delete rooms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute remote installation code without asking first.

Mitigation: Install the oo CLI yourself from a verified release and approve any installer before it runs; check whether setup adds or updates other skills, and connect only the intended Daily account.

## Reference(s):

- [Daily API documentation](https://docs.daily.co/)
- [Daily](https://www.daily.co/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Configuration guidance]

**Output Format:** [Shell commands with JSON payloads and brief guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read actions and Daily changes; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
