## Description:

Detects shared stack membership and iterates a command across all PRs in base-to-tip order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining pull request review and fix commands use this skill to identify a dependent PR stack and coordinate the normal workflow across its PRs in base-to-tip order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted PR comments could redirect stack operations.

Mitigation: Review how comments affect the workflow and verify the target PR and intended operations before running it on a live repository.

Risk: The advertised stack-wide behavior may not match the behavior reported by scanners.

Mitigation: Check the behavior against the intended workflow and try it on a non-critical PR stack before relying on it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-stack-mode)
- [Project homepage listed in metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown instructions with inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release; artifact frontmatter lists 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
