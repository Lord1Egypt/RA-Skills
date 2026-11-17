## Description:

PR closeout automation for single-PR serial merges and multi-PR batch cleanup to reduce repetitive manual work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasilva](https://clawhub.ai/user/chinasilva)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to close out pull requests by checking PR status, waiting for CI, enabling appropriate merge modes, and reporting whether merges are complete, waiting, or blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to perform real pull-request merge operations in trusted repositories.

Mitigation: Require explicit merge confirmation, review PR state and CI results, and avoid using it on untrusted repositories or branches.

Risk: The skill prioritizes local scripts such as scripts/automerge, scripts/massageprs, and ensure-workflow-docs that may change repository behavior.

Mitigation: Inspect these scripts before execution and only run them when their behavior is understood and expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasilva/skills/peter-pr-ops)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include merge status, CI wait state, blocking reasons, and whether docs/SESSION-BOOTSTRAP.md was refreshed.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
