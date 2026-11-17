## Description:

Use timeBuzzer through a connected OOMOL account to read, create, update, or delete activities and inspect users, layers, and tiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can inspect timeBuzzer account data and manage activities through their connected OOMOL account. The skill supports read operations as well as creating, updating, and deleting activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI code that has not been verified.

Mitigation: Verify the CLI through a trusted source before installing it, and review or disable automatic skill synchronization.

Risk: Creating, updating, or deleting activities changes account data.

Mitigation: Keep the skill's confirmation step and review the exact action and payload before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-timebuzzer)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [timeBuzzer API documentation](https://my.timebuzzer.com/doc/)
- [timeBuzzer](https://timebuzzer.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payload examples; connector responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change or remove data require user confirmation; fetch the live action schema before constructing a request.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
