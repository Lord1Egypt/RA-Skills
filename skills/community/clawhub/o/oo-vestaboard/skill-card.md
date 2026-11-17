## Description:

Connects to Vestaboard to read the current message and transition settings, send messages, and update transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use an agent to check what their Vestaboard displays and adjust its message or transition settings through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute changing online code and may introduce broader agent changes without a clear request.

Mitigation: Review and approve CLI installation separately, and consider setting OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

## Reference(s):

- [Vestaboard Read-Write API documentation](https://docs.vestaboard.com/docs/read-write-api/introduction)
- [Vestaboard](https://www.vestaboard.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Vestaboard skill release page](https://clawhub.ai/oomol/skills/oo-vestaboard)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command and JSON examples; connector responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include read operations and changes to the Vestaboard message or transition settings.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
