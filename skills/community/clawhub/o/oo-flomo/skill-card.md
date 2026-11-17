## Description:

flomo (flomoapp.com). Use this skill for ANY flomo request — reading, creating, updating, and deleting data. Whenever a task involves flomo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents with a connected flomo account can search and read memos, retrieve review and tagging guidance, manage tags, and create or update memos through the OOMOL-connected flomo service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency can persistently change other installed agent skills, and this effect is not explained in the skill artifact.

Mitigation: Review the CLI's broader effects and install a reviewed release separately. Set OO_SKILLS_SYNC_DISABLED=1 before running if automatic skill changes are unwanted; see the CLI controls reference.

Risk: Use requires trust in OOMOL for connected flomo data; remote installers and the hosted service implementation were not verified.

Mitigation: Review the CLI and its installation source, and assess OOMOL's handling of connected flomo data before connecting the account.

## Reference(s):

- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [flomo](https://flomoapp.com)
- [flomo API documentation](https://help.flomoapp.com/advance/api.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Text or Markdown responses; oo CLI commands with JSON input and returned data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved flomo content, action results, and command guidance.]

## Skill Version(s):

1.0.7 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
