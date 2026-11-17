## Description:

Provides guidance for using a local PCO CLI to access and manage Planning Center Services data such as plans, teams, songs, media, and scheduled people.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubyrunsstuff](https://clawhub.ai/user/rubyrunsstuff)

### License/Terms of Use:


## Use Case:

Agents assisting church operations staff can use this skill to plan services, inspect Planning Center Services records, and prepare CLI commands for common workflows. It is intended for authenticated Planning Center Services usage, including read workflows and carefully reviewed API changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a local TypeScript CLI file whose source is not included in the artifact.

Mitigation: Review the external CLI source before use and pin it to a trusted commit or release.

Risk: Authenticated raw API commands can create, update, or delete Planning Center data.

Mitigation: Use least-privilege Planning Center credentials, verify endpoints and request data, and do not allow untrusted input to choose mutation or deletion commands.

## Reference(s):

- [Planning Center Services API documentation](https://developer.planning.center/docs/#/apps/services)
- [ClawHub skill page](https://clawhub.ai/rubyrunsstuff/skills/pco)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Planning Center Services CLI commands and workflow guidance; command execution should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
