## Description:

V2EX (v2ex.com). Use this skill for ANY V2EX request — reading, creating, updating, and deleting data. Whenever a task involves V2EX, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External V2EX users can use the skill to read topics, nodes, replies, notifications, and account details, and to perform supported account changes through their connected V2EX account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may make persistent changes to skills in other agent applications without clearly explaining their scope.

Mitigation: Review the CLI release before installation and decide whether startup synchronization is acceptable; set OO_SKILLS_SYNC_DISABLED=1 to disable it.

Risk: The remote installer and hosted service behavior have not been independently audited.

Mitigation: Review and install a verified CLI release separately before use.

Risk: Actions operate through the connected V2EX account, and some actions change or delete account data.

Mitigation: Inspect the live action schema, confirm the exact payload and effect for writes, and explicitly approve the target of destructive actions.

## Reference(s):

- [V2EX API documentation](https://v2ex.com/help/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [V2EX](https://www.v2ex.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands]

**Output Format:** [JSON connector responses and text summaries, with oo CLI commands for actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live connector schema; write actions require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
