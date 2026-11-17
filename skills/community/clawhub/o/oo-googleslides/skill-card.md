## Description:

Helps agents read, create, update, and delete Google Slides data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can retrieve presentation content, create or copy presentations, preview pages, and make approved changes through Google Slides. The skill is intended for requests involving Google Slides presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that setup does not sufficiently control broader software and persistent agent changes; the installer contents and exact installed release were not verified.

Mitigation: Review and verify the oo CLI installation separately. Consider setting OO_SKILLS_SYNC_DISABLED=1 to suppress startup skill writes.

Risk: The workflow uses Google permissions and presentation data entrusted to OOMOL.

Mitigation: Review the requested Google permissions and the data shared with the connected service, and retain the skill's approval gates for presentation changes.

## Reference(s):

- [Google Slides](https://workspace.google.com/products/slides/)
- [Google Slides API reference](https://developers.google.com/workspace/slides/api/reference/rest)
- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Google Slides on ClawHub](https://clawhub.ai/oomol/skills/oo-googleslides)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the action schema; presentation changes require approval.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
