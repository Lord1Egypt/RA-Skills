## Description:

Recruitee (recruitee.com). Use this skill for ANY Recruitee request — reading, creating, and updating data. Whenever a task involves Recruitee, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and recruiting operations teams can use the skill to search candidates, read and list offers, and create candidates in Recruitee through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a downloaded CLI installer whose contents were not verified in the supplied evidence.

Mitigation: Review and install a verified CLI release separately before using this skill.

Risk: Startup skill synchronization may change other installed agent skills without sufficient disclosure.

Mitigation: Consider disabling startup synchronization with OO_SKILLS_SYNC_DISABLED=1, as documented in the CLI reference.

Risk: Recruitment data is processed through OOMOL, and creating a candidate changes Recruitee state.

Mitigation: Confirm that OOMOL may process the data and retain the skill's approval control for the exact candidate payload and effect.

## Reference(s):

- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)
- [Recruitee API documentation](https://docs.recruitee.com/reference/getting-started)
- [Recruitee](https://recruitee.com)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Recruitee data or create a candidate; state-changing actions require user confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
