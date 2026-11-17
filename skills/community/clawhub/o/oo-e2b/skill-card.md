## Description:

Operate E2B sandboxes through an OOMOL-connected account with the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to list and inspect E2B sandboxes, create sandboxes, and delete them through an OOMOL-connected E2B account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unverified remote setup code and an unverified hosted connector.

Mitigation: Review and install a verified oo CLI release before use, and verify the connector before connecting an account.

Risk: CLI startup may automatically change other agent skills.

Mitigation: Set `OO_SKILLS_SYNC_DISABLED=1` to disable startup synchronization.

Risk: Creating or deleting sandboxes changes E2B state, and deletion is destructive.

Mitigation: Inspect the live action schema and confirm the exact payload and effect before create or delete actions.

## Reference(s):

- [E2B documentation](https://e2b.dev/docs)
- [E2B website](https://e2b.dev)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON responses with concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the live connector schema; state-changing actions require approval.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
