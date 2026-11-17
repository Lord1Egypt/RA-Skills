## Description:

Search and read WaiverFile data through your OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with an OOMOL-connected WaiverFile account can retrieve site details, forms, upcoming events, and signed waivers by identifier, reference, or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded CLI code that was not assessed in the bundled artifact.

Mitigation: Review and approve the CLI installation separately before using the skill.

Risk: The connected service can process waiver requests and manage connected account credentials.

Mitigation: Confirm that OOMOL may process your waiver requests and manage the connected credentials.

Risk: Automatic skill synchronization can change installed agent skills without clear user control.

Mitigation: Review the CLI's automatic skill synchronization and disable it if unwanted.

## Reference(s):

- [WaiverFile skill listing](https://clawhub.ai/oomol/skills/oo-waiverfile)
- [WaiverFile homepage](https://www.waiverfile.com)
- [WaiverFile API documentation](https://api.waiverfile.com/swagger/ui/index)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only actions; payload fields depend on the live action schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
