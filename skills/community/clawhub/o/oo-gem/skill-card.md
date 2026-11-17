## Description:

Use a connected Gem account to search and read candidates, projects, sequences, users, and custom fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and operators use the skill to search and read candidate, project, sequence, user, and custom-field data in their connected Gem account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installer could execute remote code whose full contents were unavailable for review.

Mitigation: Review the installer and prefer a separately verified, pinned CLI installation.

Risk: CLI setup may automatically synchronize skills and make broader agent changes.

Mitigation: Decide whether automatic skill synchronization is acceptable before enabling the skill.

Risk: Recruiting data is accessed through the connected Gem account and OOMOL service.

Mitigation: Use a read-only Gem connection and confirm OOMOL is approved to process that data.

## Reference(s):

- [Gem](https://www.gem.com)
- [Gem API reference](https://api.gem.com/v0/reference)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-gem)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON data from Gem actions, with concise text or tables for summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields and records depend on the selected Gem read action.]

## Skill Version(s):

1.0.4 (source: skill frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
