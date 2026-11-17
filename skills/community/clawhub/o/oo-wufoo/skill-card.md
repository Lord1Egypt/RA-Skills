## Description:

Use this skill to read, create, and update Wufoo data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents managing Wufoo forms use this skill to inspect forms and entries, retrieve form fields, and submit new entries through a connected Wufoo account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote installers and bundled-skill synchronization can introduce broader agent changes that the skill does not explain.

Mitigation: Review and install a verified CLI release separately, and decide whether to allow its automatic bundled-skill synchronization.

Risk: Submitting an entry changes Wufoo data.

Mitigation: Review the exact submission payload and confirm its effect before approving the action.

## Reference(s):

- [Wufoo API documentation](https://wufoo.github.io/docs/)
- [Wufoo homepage](https://www.wufoo.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Wufoo skill release](https://clawhub.ai/oomol/skills/oo-wufoo)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Wufoo data]

**Output Format:** [Shell commands with JSON input and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing submissions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
