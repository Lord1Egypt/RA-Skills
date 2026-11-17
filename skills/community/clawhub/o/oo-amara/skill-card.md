## Description:

Use Amara through an OOMOL-connected account to read, create, update, and delete Amara data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Amara videos, subtitles, teams, languages, and activity use this skill to retrieve information or carry out requested changes through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency can change other agents’ installed skills, an effect the skill does not explain.

Mitigation: Review the CLI’s installation effects first. Prefer a reviewed, preinstalled CLI, or set OO_SKILLS_SYNC_DISABLED=1 when only Amara access is needed.

Risk: Actions performed through the connected account can change or delete Amara data.

Mitigation: Check the connected account’s permissions and retain the required approvals for changes.

## Reference(s):

- [Amara API documentation](https://apidocs.amara.org/)
- [Amara](https://amara.org)
- [Amara skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-amara)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text]

**Output Format:** [oo CLI commands with JSON payloads and Amara action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the selected Amara operation.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
