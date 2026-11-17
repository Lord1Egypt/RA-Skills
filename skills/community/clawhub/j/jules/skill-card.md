## Description:

Manage and automate coding tasks with Jules, Google's autonomous AI coding agent CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate repository work to Jules, monitor remote sessions, review generated patches, and apply or synchronize changes through the Jules CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-changing Jules commands can apply generated patches to a local checkout.

Mitigation: Review the patch first, confirm the session and repository, and apply changes from a clean branch or disposable checkout when practical.

Risk: Teleport can clone or synchronize repository state and apply a session patch automatically.

Mitigation: Use teleport only for the intended session, and verify the target repository before accepting the resulting workspace changes.

## Reference(s):

- [Jules CLI Reference](references/cli-reference.md)
- [ClawHub skill page](https://clawhub.ai/wei840222/skills/jules)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the jules CLI binary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
