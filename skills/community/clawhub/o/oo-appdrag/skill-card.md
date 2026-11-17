## Description:

AppDrag (appdrag.com). Use this skill for ANY AppDrag request — reading, creating, and updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AppDrag users use the skill to read, create, and update AppDrag data through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run remote installer code and add persistent agent skills without clear user control.

Mitigation: Verify the CLI release before installing, and review or disable automatic additions of other agent skills.

Risk: AppDrag writes can change account data.

Mitigation: Connect an account with only the needed permissions and retain confirmation for each write.

## Reference(s):

- [AppDrag](https://appdrag.com)
- [AppDrag API documentation](https://support.appdrag.com/doc/Interacting-with-my-API-Functions)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the live action schema; write actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
