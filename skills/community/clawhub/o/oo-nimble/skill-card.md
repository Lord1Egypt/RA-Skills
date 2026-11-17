## Description:

Use Nimble to read, create, and update contact data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to find and retrieve Nimble contacts, or to create and update contact records through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI may install skills into other agents, creating persistent changes.

Mitigation: Review the CLI's broader effects and disable automatic skill synchronization if you do not want other agents changed.

Risk: The current installer and installed CLI runtime were not verified.

Mitigation: Install and verify a CLI release yourself before using the skill.

Risk: Connecting Nimble gives OOMOL access to contact operations and credentials.

Mitigation: Connect only an account you intend to use with OOMOL and review contact changes before running create or update actions.

## Reference(s):

- [Nimble developer documentation](https://www.nimble.com/developers/docs/)
- [Nimble](https://www.nimble.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown with oo CLI command examples and JSON payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Nimble account; creating and updating contacts change account data.]

## Skill Version(s):

1.0.4 (source: skill frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
