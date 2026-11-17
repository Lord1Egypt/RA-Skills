## Description:

Chargebee (chargebee.com). Use this skill for ANY Chargebee request — reading, creating, and updating data. Whenever a task involves Chargebee, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to read Chargebee customer, invoice, item price, and subscription data, and to create customer records through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to run a remote installer whose contents and release side effects could not be verified; connected Chargebee actions can also create customer records.

Mitigation: Use a preinstalled, independently verified CLI. Review and explicitly approve any installation, disable automatic skill synchronization if desired, connect only the intended Chargebee account, and confirm customer creation before running it.

## Reference(s):

- [Chargebee API documentation](https://apidocs.chargebee.com/docs/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Chargebee](https://www.chargebee.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, API calls]

**Output Format:** [Markdown instructions with shell command examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers Chargebee reads and customer creation; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
