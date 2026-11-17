## Description:

Search and read data from an Amilia organization through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Amilia account use this skill to retrieve programs, activities, and related organization details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded installer code whose contents were not verified.

Mitigation: Review and install a fixed CLI version yourself before enabling the skill.

Risk: The linked CLI may make persistent changes that are not fully described here.

Mitigation: Review the CLI's setup and synchronization behavior; set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization if needed.

Risk: The skill uses whichever Amilia account is connected.

Mitigation: Connect only the Amilia account you intend to use.

## Reference(s):

- [Amilia](https://www.amilia.com/)
- [Amilia API documentation](https://app.amilia.com/apidocs/Index.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON request payloads and Amilia data returned through oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only program and activity lookups.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
